from typing import List, Set, Optional, Iterator, Dict, Any
from dataclasses import dataclass, field
from pydantic import BaseModel
from sqlite_utils import Database
from abc import ABC, abstractmethod
from ulid import ULID
from datetime import datetime
import time
import json
from tango.configs.dbs_config import NANOLLM_DB

class ModelNotFoundError(Exception):
    pass

class UnknownModelError(KeyError):
    pass

@dataclass
class Prompt:
    prompt: str 
    model: "Model" 
    conversation: "Conversation" 
    id: str = field(default_factory=lambda: str(ULID()).lower())
    system: Optional[str] = None
    template: Optional[str] = None
    options: "Options" = field(default_factory=lambda: Options())

    def log_prompt(self):
        db = Database(NANOLLM_DB)
        db["prompts"].upsert({
            "id": self.id,
            "conversation_id": self.conversation.id,
            "timestamp": datetime.utcnow().isoformat(),
            "prompt": self.prompt,
            "system": self.system,
            "template": self.template
        }, pk="id")
    
    @classmethod
    def from_row(cls, row, conversation = None, model = None):
        if model is None:
            model = DummyModel.get_by_id(row["model_id"])
            if model is None:
                raise ModelNotFoundError(f"Model with ID {row['model_id']} not found.")
        if conversation is None:
            conversation = Conversation.get_by_id(row["conversation_id"])
            if conversation is None:
                raise ModelNotFoundError(f"Conversation with ID {row['conversation_id']} not found.")
        return cls(
            prompt=row["prompt"],
            model=model,
            conversation=conversation,
            system=row["system"],
            template=row["template"],
            id=row["id"]
        )
    @classmethod
    def get_by_id(cls, prompt_id, conversation= None, model = None):
        db = Database(NANOLLM_DB)
        prompt = db["prompts"].get(prompt_id)
        return cls.from_row(prompt, conversation, model) if prompt else None
@dataclass
class Conversation:
    model: "Model"
    id: str = field(default_factory=lambda: str(ULID()).lower())
    responses: List["Response"] = field(default_factory=list)

    def prompt(
        self,
        prompt: str = "",
        system: Optional[str] = None,
        stream: bool = True,
        **options
    ):
        return Response(
            Prompt(
                prompt=prompt,
                conversation=self,
                system=system,
                model=self.model,
                options=self.model.ModelOptions(**options),
            ),
            self.model,
            conversation=self,
            stream = stream
        )

    def start(self):
        db = Database(NANOLLM_DB)
        self.start_time = datetime.utcnow().isoformat()
        db["conversations"].upsert({
            "id": self.id,
            "start_time": self.start_time,
            "end_time": None,
            "model_id": self.model.model_id
        }, pk="id")

    def end(self):
        db = Database(NANOLLM_DB)
        self.end_time = datetime.utcnow().isoformat()
        db["conversations"].upsert({
            "id": self.id,
            "end_time": self.end_time
        }, pk="id")

    @classmethod
    def from_row(cls, row, model=None):
        if model is None:
            model = DummyModel.get_by_id(row["model_id"])
            if model is None:
                raise ModelNotFoundError(f"Model with ID {row['model_id']} not found.")
        return cls(
            model=model,
            id=row["id"])

    @classmethod
    def get_latest(cls):
        db = Database(NANOLLM_DB)
        rows = list(db["conversations"].rows_where(order_by="start_time"))
        latest_conv = rows[-1] if rows else None
        if latest_conv:
            conversation =  cls.from_row(latest_conv) 
            for response in db["responses"].rows_where( "conversation_id = ?", [conversation.id]):
              conversation.responses.append(Response.from_row(response, 
                                                              conversation=conversation, model=conversation.model))
            return conversation
        else:
            return None
    
    @classmethod
    def get_by_id(cls, conv_id, model=None):
        db = Database(NANOLLM_DB)
        conv = db["conversations"].get(conv_id)
        return cls.from_row(conv, model=model) if conv else None
    
class Response(ABC):
    def __init__(
        self,
        prompt: Prompt,
        model: "Model",
        conversation: Conversation,
        stream: bool,
    ):
        self.prompt = prompt
        self._prompt_json = None
        self.model = model
        self.stream = stream
        self._chunks: List[str] = []
        self._done = False
        self.response_json = None
        self.conversation = conversation

    def __iter__(self) -> Iterator[str]:
        self._start = time.monotonic()
        self._start_utcnow = datetime.utcnow()
        if self._done:
            return self._chunks
        for chunk in self.model.execute(
            self.prompt,
            stream=self.stream,
            response=self,
            conversation=self.conversation,
        ):
            yield chunk
            self._chunks.append(chunk)
        if self.conversation:
            self.conversation.responses.append(self)
        self._end = time.monotonic()
        self._done = True
        self.log_response()

    def _force(self):
        if not self._done:
            list(self)

    def text(self) -> str:
        self._force()
        return "".join(self._chunks)
    
    def result(self) -> str:
        return "".join(self._chunks)
    
    def json(self) -> Optional[Dict[str, Any]]:
        return self.response_json
    
    def duration_ms(self) -> int:
        return int((self._end - self._start) * 1000)

    def datetime_utc(self) -> str:
        return self._start_utcnow.isoformat()
    
    def log_response(self):
        db = Database(NANOLLM_DB)
        db["responses"].upsert({
            "id": str(ULID()).lower(),
            "prompt": self.prompt.prompt,
            "prompt_json": self._prompt_json,
            "system": self.prompt.system,
            "response": self.result(),
            "response_json": self.json(),
            "duraion_ms": self.duration_ms(),
            "start_datetime_utc": self.datetime_utc(),
            "timestamp": datetime.utcnow().isoformat(),
            "model_id": self.model.model_id,
            "prompt_id": self.prompt.id,
            "conversation_id": self.conversation.id,
            "start":self._start,
            "end": self._end,
        }, pk="id")

    @classmethod
    def from_row(cls, row, conversation = None, model = None):
        if model is None:
            model = DummyModel.get_by_id(row["model_id"])
            if model is None:
                raise ModelNotFoundError(f"Model with ID {row['model_id']} not found.")
        if conversation is None:
            conversation = Conversation.get_by_id(row["conversation_id"], model=model)
            if conversation is None:
                raise ModelNotFoundError(f"Conversation with ID {row['conversation_id']} not found.")
        prompt = Prompt.get_by_id(row["prompt_id"], conversation, model)
        if prompt is None:
            raise ModelNotFoundError(f"Prompt with ID {row['prompt_id']} not found.")
                 
        response = cls(
            model=model,
            prompt= prompt,
            conversation = conversation,
            stream=False,
        )
        response.id = row["id"]
        response._prompt_json = json.loads(row["prompt_json"] or "null")
        response.response_json = json.loads(row["response_json"] or "null")
        response._done = True
        response._chunks = [row["response"]]
        return response


class Options(BaseModel):
    # Note: using pydantic v1 style Configs,
    # these are also compatible with pydantic v2
    class Config:
        extra = "forbid"

        
class Model(ABC):
    model_id: str
    key: Optional[str] = None
    needs_key: Optional[str] = None
    key_env_var: Optional[str] = None
    can_stream: bool = False

    def __init__(self, model_id, key=None, needs_key=None, key_env_var=None, can_stream=False):
        self.model_id = model_id
        self.key = key
        self.needs_key = needs_key
        self.key_env_var = key_env_var
        self.can_stream = can_stream
        self._options: Dict[str, Any] = {}

    class ModelOptions(Options):
        pass

    @abstractmethod
    def execute(
        self,
        prompt: Prompt,
        stream: bool,
        response: Response,
        conversation: Optional[Conversation],
    ) -> Iterator[str]:
        """
        Execute a prompt and yield chunks of text, or yield a single big chunk.
        Any additional useful information about the execution should be assigned to the response.
        """
        pass

    def conversation(self):
        conv = Conversation(model=self)
        conv.start()  # Start and log the conversation
        return conv

    def prompt(self, conversation:Conversation, prompt_input: str, system: Optional[str] = None, stream: bool = True, **options):
        response = self.response(Prompt(prompt=prompt_input, system=system, conversation=conversation, model=self, 
                                        options=self.ModelOptions(**options)), conversation=conversation, stream=stream)
        response.prompt.log_prompt()  # Log the prompt
        return response

    def response(self, prompt: Prompt, conversation:Conversation, stream: bool = True) -> Response:
        resp = Response(prompt, self, conversation, stream)
        return resp

    def __str__(self) -> str:
        return "{}: {}".format(self.__class__.__name__, self.model_id)

    def __repr__(self):
        return "<Model '{}'>".format(self.model_id)


class DummyModel(Model):
    def execute(self, prompt: Prompt, stream: bool, response: Response, conversation: Conversation | None) -> Iterator[str]:
        yield "dummy response from dummy model"

    @classmethod
    def from_row(cls, row):
        # Return Model static information
        return cls(
            model_id=row["model_id"],
            key=row["key"],
            needs_key=row["needs_key"],
            key_env_var=row["key_env_var"],
            can_stream=row["can_stream"]
        )

    @classmethod
    def get_by_id(cls, model_id):
        db = Database(NANOLLM_DB)
        row = db["models"].get(model_id)
        return cls.from_row(row) if row else None

@dataclass
class ModelWithAliases:
    model: Model
    aliases: Set[str]

    @classmethod
    def from_row(cls, row):
        model = DummyModel.from_row(row)
        aliases = set(json.loads(row["aliases"]))
        return cls(model=model, aliases=aliases)

    @classmethod
    def load_dummy_models_with_aliases(cls):
        db = Database(NANOLLM_DB)
        rows = list(db["models"].rows)
        return {row['model_id']: cls.from_row(row) for row in rows}
    
    def log_model_with_aliases(self):
        db = Database(NANOLLM_DB)
        db["models"].upsert({
            "model_id": self.model.model_id,
            "key": self.model.key,
            "needs_key": self.model.needs_key,
            "key_env_var": self.model.key_env_var,
            "can_stream": self.model.can_stream,
            "aliases": json.dumps(list(self.aliases))
        }, pk="model_id")
    
