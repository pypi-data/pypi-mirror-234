import pluggy
import json
import os
from pathlib import Path
from typing import List, Set, Optional, Dict
from tango.nanoLLM.nanollm.plugin_spec import NanoLLMSpec, hookimpl
from tango.nanoLLM.nanollm.models import Model, ModelWithAliases, UnknownModelError
from nanollm import user_dir

class NanoLLMPluginManager:
    """Manages plugins for nanoLLM."""
    
    def __init__(self):
        self.pm = pluggy.PluginManager("nanoLLM")
        self.pm.add_hookspecs(NanoLLMSpec)
        self.pm.load_setuptools_entrypoints("nanoLLM")
        # Load models and aliases from disk with DummyModels
        self.models_and_aliases: Dict[str, ModelWithAliases] = ModelWithAliases.load_dummy_models_with_aliases() 
        self.default_model = None
        self.config:Dict = self.load_config()
    
    def load_config(self):
        config_path = user_dir() / "config.json"
        if config_path.exists():
            return json.loads(config_path.read_text())
        else:
            return {
                "default_model": None,
            }
    
    def set_default_model(self, model_id_or_alias) -> str:
        """Set the default model."""
        # Check if the model exists
        model = self.get_model_by_model_id_or_alias(model_id_or_alias)
        if model:
            self.config['default_model'] = model.model_id
            with open(user_dir() / "config.json", "w") as f:
                json.dump(self.config, f, indent=2)
            return model.model_id
        else:
            raise ValueError(f"No {model_id_or_alias} found.")

    def get_default_model(self):
        return self.config['default_model']

    def register_model_alias(self, model: Model, aliases: Set[str]=set()):
        """Register a model along with its aliases."""
        if model.model_id in self.models_and_aliases:
            self.models_and_aliases[model.model_id].aliases.update(aliases)
        else:
            model_with_aliases = ModelWithAliases(model=model, aliases=aliases)
            self.models_and_aliases[model.model_id] = model_with_aliases
        # Update dummy model with registered model
        self.models_and_aliases[model.model_id].model = model
        # Save the model with aliases to disk
        self.models_and_aliases[model.model_id].log_model_with_aliases()
    
    def set_model_alias(self, model_id_or_alias, alias):
        if model_id_or_alias in self.models_and_aliases:
            self.models_and_aliases[model_id_or_alias].aliases.add(alias)
        else:
            model = self.get_model_by_model_id_or_alias(model_id_or_alias)
            if model:
                self.register_model_alias(model, {alias})
            else:
                raise UnknownModelError(f"Model {model_id_or_alias} not found.")
        # Save the model with aliases to disk
        self.models_and_aliases[model_id_or_alias].log_model_with_aliases()

    def register_plugin(self, plugin, plugin_name):
        """Register a plugin."""
        self.pm.register(plugin, plugin_name)
        # Now, let's ask the plugin to load its models
        #plugin.register_models(self.register_model_alias)
    
    def get_model_by_model_id_or_alias(self, model_id_or_alias) -> Optional[Model]:
        """Retrieve a model by its name or alias."""
        if model_id_or_alias in self.models_and_aliases:
            return self.models_and_aliases[model_id_or_alias].model
        for model_with_aliases in self.models_and_aliases.values():
            if model_with_aliases.model.model_id == model_id_or_alias or model_id_or_alias in model_with_aliases.aliases:
                return model_with_aliases.model
        return None
    
    def list_models(self) -> List[Model]:
        return [model_with_aliases.model for model_with_aliases in self.models_and_aliases]

    # This method will allow plugins to register commands
    def hook(self):
        return self.pm.hook
"""
def get_models_with_aliases(pm) -> List["ModelWithAliases"]:
    model_aliases = []

    # Include aliases from aliases.json
    aliases_path = user_dir() / "aliases.json"
    extra_model_aliases: Dict[str, list] = {}
    if aliases_path.exists():
        configured_aliases = json.loads(aliases_path.read_text())
        for alias, model_id in configured_aliases.items():
            extra_model_aliases.setdefault(model_id, []).append(alias)

    def register(model, aliases=None):
        alias_list = list(aliases or [])
        if model.model_id in extra_model_aliases:
            alias_list.extend(extra_model_aliases[model.model_id])
        model_aliases.append(ModelWithAliases(model, alias_list))

    pm.hook().register_models(register=register)

    return model_aliases
"""