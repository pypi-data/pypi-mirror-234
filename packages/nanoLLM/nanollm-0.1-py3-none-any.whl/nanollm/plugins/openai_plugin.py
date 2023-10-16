import requests
import os
import openai
import click
try:
    from pydantic import field_validator, Field  # type: ignore
except ImportError:
    from pydantic.fields import Field
    from pydantic.class_validators import validator as field_validator  # type: ignore [no-redef]
from typing import Optional, Union, List
from tango.nanoLLM.nanollm.plugin_spec import hookimpl
from tango.nanoLLM.nanollm.models import Model, Options 

class OpenAIPlugin:
    name = "openai_chat_model"
    OPENAI_API_CHAT_URL = "https://api.openai.com/v1/chat/completions"
    HEADERS = {
        "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }
    
    @hookimpl
    def register_models(self, register):
        # For this plugin, loading is essentially ensuring we have an API key.
        # You can add more logic here if needed.
        if not os.environ.get('OPENAI_API_KEY'):
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        register(Chat("gpt-3.5-turbo"), aliases=("3.5", "chatgpt"))
        register(Chat("gpt-3.5-turbo-16k"), aliases=("chatgpt-16k", "3.5-16k"))
        register(Chat("gpt-4"), aliases=("4", "gpt4"))
        register(Chat("gpt-4-32k"), aliases=("4-32k",))
        register(
            Completion("gpt-3.5-turbo-instruct", default_max_tokens=256),
            aliases=("3.5-instruct", "chatgpt-instruct"),
    )

    def predict(self, prompt: str) -> str:

        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 150
        }
        response = requests.post(self.OPENAI_API_CHAT_URL, headers=self.HEADERS, json=payload)

        if response.status_code != 200:
            return f"Error {response.status_code}: {response.json().get('error', {}).get('message', 'Unknown error')}"

        response_content = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        return response_content

class Chat(Model):
    needs_key = "openai"
    key_env_var = "OPENAI_API_KEY"
    can_stream: bool = True

    default_max_tokens = None

    class ModelOptions(Options):
        temperature: Optional[float] = Field(
            description=(
                "What sampling temperature to use, between 0 and 2. Higher values like "
                "0.8 will make the output more random, while lower values like 0.2 will "
                "make it more focused and deterministic."
            ),
            ge=0,
            le=2,
            default=None,
        )
        max_tokens: Optional[int] = Field(
            description="Maximum number of tokens to generate.", default=None
        )
        top_p: Optional[float] = Field(
            description=(
                "An alternative to sampling with temperature, called nucleus sampling, "
                "where the model considers the results of the tokens with top_p "
                "probability mass. So 0.1 means only the tokens comprising the top "
                "10% probability mass are considered. Recommended to use top_p or "
                "temperature but not both."
            ),
            ge=0,
            le=1,
            default=None,
        )
        frequency_penalty: Optional[float] = Field(
            description=(
                "Number between -2.0 and 2.0. Positive values penalize new tokens based "
                "on their existing frequency in the text so far, decreasing the model's "
                "likelihood to repeat the same line verbatim."
            ),
            ge=-2,
            le=2,
            default=None,
        )
        presence_penalty: Optional[float] = Field(
            description=(
                "Number between -2.0 and 2.0. Positive values penalize new tokens based "
                "on whether they appear in the text so far, increasing the model's "
                "likelihood to talk about new topics."
            ),
            ge=-2,
            le=2,
            default=None,
        )
        stop: Optional[str] = Field(
            description=("A string where the API will stop generating further tokens."),
            default=None,
        )
        logit_bias: Optional[Union[dict, str]] = Field(
            description=(
                "Modify the likelihood of specified tokens appearing in the completion. "
                'Pass a JSON string like \'{"1712":-100, "892":-100, "1489":-100}\''
            ),
            default=None,
        )

        @field_validator("logit_bias")
        def validate_logit_bias(cls, logit_bias):
            if logit_bias is None:
                return None

            if isinstance(logit_bias, str):
                try:
                    logit_bias = json.loads(logit_bias)
                except json.JSONDecodeError:
                    raise ValueError("Invalid JSON in logit_bias string")

            validated_logit_bias = {}
            for key, value in logit_bias.items():
                try:
                    int_key = int(key)
                    int_value = int(value)
                    if -100 <= int_value <= 100:
                        validated_logit_bias[int_key] = int_value
                    else:
                        raise ValueError("Value must be between -100 and 100")
                except ValueError:
                    raise ValueError("Invalid key-value pair in logit_bias dictionary")

            return validated_logit_bias

    def __init__(
        self,
        model_id,
        key=None,
        model_name=None,
        api_base=None,
        api_type=None,
        api_version=None,
        api_engine=None,
        headers=None,
    ):
        self.model_id = model_id
        self.key = key
        self.model_name = model_name
        self.api_base = api_base
        self.api_type = api_type
        self.api_version = api_version
        self.api_engine = api_engine
        self.headers = headers

    def __str__(self):
        return "OpenAI Chat: {}".format(self.model_id)

    def execute(self, prompt, stream=None, response=None, conversation=None):
        messages = []
        current_system = None
        if conversation is not None:
            for prev_response in conversation.responses:
                if (
                    prev_response.prompt.system
                    and prev_response.prompt.system != current_system
                ):
                    messages.append(
                        {"role": "system", "content": prev_response.prompt.system}
                    )
                    current_system = prev_response.prompt.system
                messages.append(
                    {"role": "user", "content": prev_response.prompt.prompt}
                )
                messages.append({"role": "assistant", "content": prev_response.text()})
        if prompt.system and prompt.system != current_system:
            messages.append({"role": "system", "content": prompt.system})
        messages.append({"role": "user", "content": prompt.prompt})
        response._prompt_json = {"messages": messages}
        kwargs = self.build_kwargs(prompt)
        if stream:
            completion = openai.ChatCompletion.create(
                model=self.model_name or self.model_id,
                messages=messages,
                stream=True,
                **kwargs,
            )
            chunks = []
            for chunk in completion:
                chunks.append(chunk)
                content = chunk["choices"][0].get("delta", {}).get("content")
                if content is not None:
                    yield content
            response.response_json = combine_chunks(chunks)
        else:
            completion = openai.ChatCompletion.create(
                model=self.model_name or self.model_id,
                messages=messages,
                stream=False,
                **kwargs,
            )
            response.response_json = completion.to_dict_recursive()
            yield completion.choices[0].message.content

    def build_kwargs(self, prompt):
        kwargs = dict(not_nulls(prompt.options))
        if "max_tokens" not in kwargs and self.default_max_tokens is not None:
            kwargs["max_tokens"] = self.default_max_tokens
        if self.api_base:
            kwargs["api_base"] = self.api_base
        if self.api_type:
            kwargs["api_type"] = self.api_type
        if self.api_version:
            kwargs["api_version"] = self.api_version
        if self.api_engine:
            kwargs["engine"] = self.api_engine
        if self.needs_key:
            if self.key:
                kwargs["api_key"] = self.key
        else:
            # OpenAI-compatible models don't need a key, but the
            # openai client library requires one
            kwargs["api_key"] = "DUMMY_KEY"
        if self.headers:
            kwargs["headers"] = self.headers
        return kwargs


class Completion(Chat):
    class ModelOptions(Chat.ModelOptions):
        logprobs: Optional[int] = Field(
            description="Include the log probabilities of most likely N per token",
            default=None,
            le=5,
        )

    def __init__(self, *args, default_max_tokens=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_max_tokens = default_max_tokens

    def __str__(self):
        return "OpenAI Completion: {}".format(self.model_id)

    def execute(self, prompt, stream, response, conversation=None):
        if prompt.system:
            raise NotImplementedError(
                "System prompts are not supported for OpenAI completion models"
            )
        messages = []
        if conversation is not None:
            for prev_response in conversation.responses:
                messages.append(prev_response.prompt.prompt)
                messages.append(prev_response.text())
        messages.append(prompt.prompt)
        response._prompt_json = {"messages": messages}
        kwargs = self.build_kwargs(prompt)
        if stream:
            completion = openai.Completion.create(
                model=self.model_name or self.model_id,
                prompt="\n".join(messages),
                stream=True,
                **kwargs,
            )
            chunks = []
            for chunk in completion:
                chunks.append(chunk)
                content = chunk["choices"][0].get("text") or ""
                if content is not None:
                    yield content
            response.response_json = combine_chunks(chunks)
        else:
            completion = openai.Completion.create(
                model=self.model_name or self.model_id,
                prompt="\n".join(messages),
                stream=False,
                **kwargs,
            )
            response.response_json = completion.to_dict_recursive()
            yield completion.choices[0]["text"]


def not_nulls(data) -> dict:
    return {key: value for key, value in data if value is not None}


def combine_chunks(chunks: List[dict]) -> dict:
    content = ""
    role = None
    finish_reason = None

    # If any of them have log probability, we're going to persist
    # those later on
    logprobs = []

    for item in chunks:
        for choice in item["choices"]:
            if (
                "logprobs" in choice
                and "text" in choice
                and isinstance(choice["logprobs"], dict)
                and "top_logprobs" in choice["logprobs"]
            ):
                logprobs.append(
                    {
                        "text": choice["text"],
                        "top_logprobs": choice["logprobs"]["top_logprobs"],
                    }
                )
            if "text" in choice and "delta" not in choice:
                content += choice["text"]
                continue
            if "role" in choice["delta"]:
                role = choice["delta"]["role"]
            if "content" in choice["delta"]:
                content += choice["delta"]["content"]
            if choice.get("finish_reason") is not None:
                finish_reason = choice["finish_reason"]

    # Imitations of the OpenAI API may be missing some of these fields
    combined = {
        "content": content,
        "role": role,
        "finish_reason": finish_reason,
    }
    if logprobs:
        combined["logprobs"] = logprobs
    for key in ("id", "object", "model", "created", "index"):
        if key in chunks[0]:
            combined[key] = chunks[0][key]

    return combined

PLUGIN_CLASS = OpenAIPlugin