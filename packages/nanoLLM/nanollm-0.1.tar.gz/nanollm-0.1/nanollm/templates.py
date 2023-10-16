import pydantic
from pydantic import BaseModel
import string
from typing import Optional, Any, Dict, List, Tuple
import click
import yaml
from nanollm import user_dir
from sqlite_utils import Database
from tango.configs.dbs_config import NANOLLM_DB

def template_dir():
    path = user_dir() / "templates"
    path.mkdir(parents=True, exist_ok=True)
    return path

def load_template(name):
    path = template_dir() / f"{name}.yaml"
    if not path.exists():
        raise click.ClickException(f"Invalid template: {name}")
    try:
        loaded = yaml.safe_load(path.read_text())
    except yaml.YAMLError as ex:
        raise click.ClickException("Invalid YAML: {}".format(str(ex)))
    if isinstance(loaded, str):
        return Template(name=name, prompt=loaded)
    loaded["name"] = name
    try:
        return Template(**loaded)
    except pydantic.ValidationError as ex:
        msg = "A validation error occurred:\n"
        raise click.ClickException(msg)
    
class Template(BaseModel):
    name: str
    prompt: Optional[str] = None
    system: Optional[str] = None
    model: Optional[str] = None
    defaults: Optional[Dict[str, Any]] = None

    class Config:
        extra = "forbid"

    class MissingVariables(Exception):
        pass

    def evaluate(
        self, input: str, params: Optional[Dict[str, Any]] = None
    ) -> Tuple[str, Optional[str]]:
        params = params or {}
        params["input"] = input
        if self.defaults:
            for k, v in self.defaults.items():
                if k not in params:
                    params[k] = v

        # Extract placeholders from the template
        expected_params = set(self.extract_vars(string.Template(self.prompt or "")))
        if self.system:
            expected_params.update(self.extract_vars(string.Template(self.system)))
        
        # Check for unexpected parameters
        unexpected_params = set(params.keys()) - expected_params
        unexpected_params.discard("input")
        if unexpected_params:
            raise ValueError(f"Unexpected parameters: {', '.join(unexpected_params)}")
    
        prompt: Optional[str] = None
        system: Optional[str] = None
        if not self.prompt:
            system = self.interpolate(self.system, params)
            prompt = input
        elif self.system:
            prompt = self.interpolate(self.prompt, params)
            system = self.interpolate(self.system, params)
        else:
            prompt = self.interpolate(self.prompt, params)

        return prompt, system

    @classmethod
    def interpolate(cls, text: Optional[str], params: Dict[str, Any]) -> Optional[str]:
        if not text:
            return text
        # Confirm all variables in text are provided
        string_template = string.Template(text)
        vars = cls.extract_vars(string_template)
        missing = [p for p in vars if p not in params]
        if missing:
            raise cls.MissingVariables(
                "Missing variables: {}".format(", ".join(missing))
            )
        return string_template.substitute(**params)

    @staticmethod
    def extract_vars(string_template: string.Template) -> List[str]:
        return [
            match.group("named")
            for match in string_template.pattern.finditer(string_template.template)
        ]
    
    def log_template(self):
        db = Database(NANOLLM_DB)
        db["templates"].upsert(self.dict(), pk="name")
        