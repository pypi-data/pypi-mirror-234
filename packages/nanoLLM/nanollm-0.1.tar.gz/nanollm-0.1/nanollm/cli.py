import click
import os
import json
import sqlite_utils
from click_default_group import DefaultGroup
from tango.nanoLLM.nanollm.plugin_manager import NanoLLMPluginManager
from tango.nanoLLM.nanollm.plugin_utils import setup_plugin_manager
from tango.nanoLLM.nanollm.templates import Template, template_dir, load_template
from tango.nanoLLM.nanollm.models import Conversation, ModelWithAliases
from tango.nanoLLM.nanollm.sqlite_logging import logger, logs_db_path, logs_db_size
from nanollm import (
    user_dir,
    read_prompt
)


pm = NanoLLMPluginManager()
setup_plugin_manager(pm)

@click.group(
    cls=DefaultGroup,
    default="prompt",
    default_if_no_args=True
    )
def cli():
    pass

@cli.group(name="keys")
@click.pass_context
def keys(ctx):
    "Commands for managing keys"
    ctx.ensure_object(dict)
   
@keys.command("set")
@click.argument('key')
@click.argument('value', required=False)
@click.pass_context
def set_key(ctx, key, value):
    """Set a key-value pair in the context object."""
    ctx.obj[key] = value
    click.echo(f"Key '{key}' set to '{value}'")

@keys.command(name="get")
@click.argument('key')
@click.pass_context
def get_key(ctx, key):
    """Retrieve the value for a given key from the context object."""
    value = ctx.obj.get(key)
    if value is not None:
        click.echo(value)
    else:
        click.echo(f"No value set for key '{key}'")

@cli.command()
@click.argument('prompt', default="", required=True)
@click.option("-s", "--system", help="System prompt to use")
@click.option('--model-id', '--model', '-m', default=pm.get_default_model(), help='Model to use for prediction')
@click.option("--stream", is_flag=True, help="Do stream output")
@click.option("--template", "-t", default=None, help="Name of the template to use")
@click.option("--param", "-p", multiple=True, type=(str, str), help="Parameters for the template in the form -p key value")
@click.option( "options", "-o", "--option", type=(str, str), multiple=True, help="key/value options for the model")
@click.option("-n", "--no-log", is_flag=True, help="Don't log to database")
@click.option(
    "continue_latest",
    "-c",
    "--continue",
    is_flag=True,
    flag_value=-1,
    help="Continue the most recent conversation.",
)
@click.option(
    "conv_id",
    "--cid",
    "--conversation",
    help="Continue the conversation with the given ID.",
)
def prompt(model_id, prompt, system, stream, template, param, options, no_log, continue_latest, conv_id):
    """Get a response for the given input prompt."""

    if model_id:
        # Fetch the model by name
        model = pm.get_model_by_model_id_or_alias(model_id)
        if not model:
            click.echo(f"No model found with name: {model}")
            return

        prompt = read_prompt(prompt)

        # Determine which conversation to use
        if continue_latest or conv_id:
            if continue_latest:
                conversation = Conversation.get_latest()
                if not conversation:
                    click.echo("No previous conversation found. Starting a new one.")
                    conversation = model.conversation()
            else:
                conversation = Conversation.get_by_id(conv_id)
                if not conversation:
                    click.echo(f"No conversation found with ID {conv_id}. Starting a new one.")
                    conversation = model.conversation()
        else:
            conversation = model.conversation()

        should_stream = model.can_stream and stream
        prompt_method = model.prompt
        
        # If a template is provided, generate the prompt using the template
        if template:
            tmpl = load_template(template)
            if not tmpl:
                click.echo(f"No template found with name: {template}")
                return
            params_dict = dict(param)  # Convert tuple of key-value pairs into a dictionary
            prompt, system = tmpl.evaluate(prompt, params_dict)
        
        options_dict = dict(options)

        response = prompt_method(conversation, prompt, system, **options_dict)
        if should_stream:
            # Stream the response
            for chunk in response:
                click.echo(chunk)
        else:
            click.echo(response.text())

        # Log the conversation
        if not no_log:
            logger.info(f"Model: {model_id}, Prompt: {prompt}, Stream: {stream}", 
                        extra={"conversation": conversation.id})

    else:
        click.echo("No model specified.")
    

@cli.group(name="models")
def models():
    "Commands for managing models"

@models.command(name='set-default')
@click.argument('model_id_or_alias')
def set_default_model_cmd(model_id_or_alias):
    """Set the default model."""
    model_id = pm.set_default_model(model_id_or_alias)
    click.echo(f"Default model set to: {model_id}")

@models.command(name='default')
def get_default_model_cmd():
    """Get the default model."""
    model = pm.get_default_model()
    if model:
        click.echo(model)
    else:
        click.echo("No default model is set.")

@models.command(name="list")
def list_models():
    """List all registered models."""
    for model_id, model_with_alias in pm.models_and_aliases.items():
        click.echo(f"Model: {model_id}")
        if model_with_alias.aliases:
            click.echo(f"Aliases: {', '.join(model_with_alias.aliases)}")

@models.command(name="set-alias")
@click.argument('model_id_or_alias', required=True)
@click.argument('alias', required=True)
def set_model_alias(model_id_or_alias, alias):
    """Set an alias for a model."""
    pm.set_model_alias(model_id_or_alias, alias)

@cli.group(
    cls=DefaultGroup,
    default="list",
    default_if_no_args=True,
)
def template():
    """Commands for managing templates."""
    pass

@template.command()
@click.option('--name', required=True, help="Name of the template.")
@click.option('--prompt', required=False, help="Content for the prompt template.")
@click.option('--system', default="", help="Content for the system prompt template.")
def create(name, prompt, system):
    """Create a new template."""
    path = template_dir() / f"{name}.yaml"
    if path.exists():
        raise click.ClickException(f"Template named {name} already exists in {path}.")
    new_template = Template(name=name, prompt=prompt, system=system)
    new_template.log_template()
    with open(path, "w") as f:
        f.write(new_template.json())
    click.echo(f"Template {name} created successfully in {path}.")

@template.command()
def list():
    """List all available templates."""
    template_directory = template_dir()
    for template_file in template_directory.glob("*.yaml"):
        template_name = template_file.stem
        tmpl = load_template(template_name)
        click.echo(f"{template_name}  system:{tmpl.system or 'N/A'}, prompt:{tmpl.prompt or 'N/A'}")

@template.command(name="path")
def templates_path():
    "Output the path to the templates directory"
    click.echo(template_dir())

@template.command()
@click.option('--name', required=True, help="Name of the template to update.")
@click.option('--prompt', help="Updated content for the prompt template.")
@click.option('--system', help="Updated content for the system prompt template.")
def update(name, prompt, system):
    """Update an existing template."""
    path = template_dir() / f"{name}.yaml"
    if not path.exists():
        raise click.ClickException(f"Template named {name} does not exist.")
    loaded_template = load_template(name)
    if prompt:
        loaded_template.prompt = prompt
    if system:
        loaded_template.system = system
    with open(path, "w") as f:
        f.write(loaded_template.json())
    click.echo(f"Template {name} updated successfully.")

@template.command()
@click.option('--name', required=True, help="Name of the template to delete.")
def delete(name):
    """Delete a template."""
    path = template_dir() / f"{name}.yaml"
    if not path.exists():
        raise click.ClickException(f"Template named {name} does not exist.")
    os.remove(path)
    click.echo(f"Template {name} deleted successfully.")

@cli.group()
def logs():
    """Commands for managing logs."""
    pass

@logs.command(name="path")
def logs_path():
    "Output the path to the logs.db file"
    click.echo(logs_db_path())


@logs.command(name="status")
def logs_status():
    "Show current status of database logging"
    path = logs_db_path()
    if not path.exists():
        click.echo("No log database found at {}".format(path))
        return
    db = sqlite_utils.Database(path)
    click.echo("Found log database at {}".format(path))
    #click.echo("Number of conversations logged:\t{}".format(db["conversations"].count))
    #click.echo("Number of responses logged:\t{}".format(db["responses"].count))
    click.echo("Number of logs logged:\t{}".format(db["logs"].count))
    click.echo(
        "Database file size: \t\t{}".format(logs_db_size(path))
    )
    for log in db["logs"].rows:
        click.echo(log)
        break

if __name__ == "__main__":
    pm.hook().register_commands(cli=cli)
    cli()
