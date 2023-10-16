import json
from abc import abstractmethod, ABC
from copy import copy
from typing import Optional, Generator, Any

import anthropic  # type: ignore
import openai

from .completions import CompletionChunk, PromptTemplateWithMetadata, CompletionResponse, ChatCompletionResponse, \
    ChatMessage
from .errors import APIKeyMissingError, FreeplayError
from .llm_parameters import LLMParameters
from .provider_config import ProviderConfig, OpenAIConfig, AnthropicConfig
from .utils import format_template_variables


class Flavor(ABC):
    @classmethod
    def get_by_name(cls, flavor_name: str) -> 'Flavor':
        match flavor_name:
            case OpenAIText.record_format_type:
                return OpenAIText()
            case OpenAIChat.record_format_type:
                return OpenAIChat()
            case AnthropicClaudeText.record_format_type:
                return AnthropicClaudeText()
            case _:
                raise FreeplayError(
                    'Configured flavor not found in SDK. Please update your SDK version or configure a different model in the Freeplay UI.')

    @property
    @abstractmethod
    def provider(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def record_format_type(self) -> str:
        raise NotImplementedError()

    @property
    def _model_params_with_defaults(self) -> LLMParameters:
        return LLMParameters.empty()

    @abstractmethod
    def format(self, prompt_template: PromptTemplateWithMetadata, variables: dict[str, str]) -> str:
        pass

    @abstractmethod
    def call_service(
            self,
            formatted_prompt: str,
            provider_config: ProviderConfig,
            llm_parameters: LLMParameters
    ) -> CompletionResponse:
        pass

    @abstractmethod
    def call_service_stream(
            self,
            formatted_prompt: str,
            provider_config: ProviderConfig,
            llm_parameters: LLMParameters
    ) -> Generator[CompletionChunk, None, None]:
        pass

    def get_model_params(self, llm_parameters: LLMParameters) -> LLMParameters:
        return self._model_params_with_defaults.merge_and_override(llm_parameters)


class ChatFlavor(Flavor, ABC):
    @abstractmethod
    def continue_chat(
            self,
            messages: list[ChatMessage],
            provider_config: ProviderConfig,
            llm_parameters: LLMParameters
    ) -> ChatCompletionResponse:
        pass

    @abstractmethod
    def continue_chat_stream(
            self,
            messages: list[ChatMessage],
            provider_config: ProviderConfig,
            llm_parameters: LLMParameters
    ) -> Generator[CompletionChunk, None, None]:
        pass


class OpenAI(Flavor, ABC):
    def configure_openai(self, openai_config: Optional[OpenAIConfig]) -> None:
        super().__init__()
        if not openai_config:
            raise APIKeyMissingError(
                "Missing OpenAI key. Use a ProviderConfig to specify keys prior to getting completion.")

        if openai_config.api_base:
            openai.api_base = openai_config.api_base

        if not openai_config.api_key or not openai_config.api_key.strip():
            raise APIKeyMissingError("OpenAI API key is not set. It must be set to make calls to the service.")

        openai.api_key = openai_config.api_key

    @property
    def provider(self) -> str:
        return "openai"


class OpenAIText(OpenAI):
    record_format_type = "openai_text"
    _model_params_with_defaults = LLMParameters({
        "model": "text-davinci-003"
    })

    def format(self, prompt_template: PromptTemplateWithMetadata, variables: dict[str, str]) -> str:
        return format_template_variables(prompt_template.content, variables)

    def call_service(
            self,
            formatted_prompt: str,
            provider_config: ProviderConfig,
            llm_parameters: LLMParameters
    ) -> CompletionResponse:
        completion = self.__call_openai(formatted_prompt, provider_config, llm_parameters, stream=False)
        return CompletionResponse(
            content=completion.choices[0].text,
            is_complete=completion.choices[0].finish_reason == "stop"
        )

    def call_service_stream(
            self,
            formatted_prompt: str,
            provider_config: ProviderConfig,
            llm_parameters: LLMParameters
    ) -> Generator[CompletionChunk, None, None]:
        completion = self.__call_openai(formatted_prompt, provider_config, llm_parameters, stream=True)

        for chunk in completion:
            yield CompletionChunk(
                text=chunk.choices[0].text,
                is_complete=chunk.choices[0].finish_reason == "stop"
            )

    def __call_openai(
            self,
            prompt: str,
            provider_config: ProviderConfig,
            llm_parameters: LLMParameters,
            stream: bool
    ) -> Any:
        self.configure_openai(provider_config.openai)
        return openai.Completion.create(
            prompt=prompt,
            stream=stream,
            **self.get_model_params(llm_parameters)
        )  # type: ignore


class OpenAIChat(OpenAI, ChatFlavor):
    record_format_type = "openai_chat"
    _model_params_with_defaults = LLMParameters({
        "model": "gpt-3.5-turbo"
    })

    def format(self, prompt_template: PromptTemplateWithMetadata, variables: dict[str, str]) -> str:
        # Extract messages JSON to enable formatting of individual content fields of each message. If we do not
        # extract the JSON, current variable interpolation will fail on JSON curly braces.
        messages_as_json: list[dict[str, str]] = json.loads(prompt_template.content)
        formatted_messages = [
            {
                "content": format_template_variables(message['content'], variables), "role": message['role']
            } for message in messages_as_json]
        return json.dumps(formatted_messages)

    def call_service(
            self,
            formatted_prompt: str,
            provider_config: ProviderConfig,
            llm_parameters: LLMParameters
    ) -> CompletionResponse:
        messages = json.loads(formatted_prompt)
        completion = self.__call_openai(messages, provider_config, llm_parameters, stream=False)
        return CompletionResponse(
            content=completion.choices[0].message.content or '',
            is_complete=completion.choices[0].finish_reason == 'stop',
            openai_function_call=completion.choices[0].message.get('function_call')
        )

    def call_service_stream(
            self,
            formatted_prompt: str,
            provider_config: ProviderConfig,
            llm_parameters: LLMParameters
    ) -> Generator[CompletionChunk, None, None]:
        messages = json.loads(formatted_prompt)
        completion_stream = self.__call_openai(messages, provider_config, llm_parameters, stream=True)
        for chunk in completion_stream:
            yield CompletionChunk(
                text=chunk.choices[0].delta.get('content') or '',
                is_complete=chunk.choices[0].finish_reason == 'stop',
                openai_function_call=chunk.choices[0].delta.get('function_call')
            )

    def continue_chat(
            self,
            messages: list[ChatMessage],
            provider_config: ProviderConfig,
            llm_parameters: LLMParameters
    ) -> ChatCompletionResponse:
        completion = self.__call_openai(messages, provider_config, llm_parameters, stream=False)

        message_history = copy(messages)
        message_history.append(completion.choices[0].message.to_dict())
        return ChatCompletionResponse(
            content=completion.choices[0].message.content,
            message_history=message_history,
            is_complete=completion.choices[0].finish_reason == "stop"
        )

    def continue_chat_stream(
            self,
            messages: list[ChatMessage],
            provider_config: ProviderConfig,
            llm_parameters: LLMParameters
    ) -> Generator[CompletionChunk, None, None]:
        completion_stream = self.__call_openai(messages, provider_config, llm_parameters, stream=True)
        for chunk in completion_stream:
            yield CompletionChunk(
                text=chunk.choices[0].delta.get('content', ''),
                is_complete=chunk.choices[0].finish_reason == "stop"
            )

    def __call_openai(
            self,
            messages: list[ChatMessage],
            provider_config: ProviderConfig,
            llm_parameters: LLMParameters,
            stream: bool
    ) -> Any:
        self.configure_openai(provider_config.openai)
        return openai.ChatCompletion.create(
            messages=messages,
            **self.get_model_params(llm_parameters),
            stream=stream
        )  # type: ignore


class AnthropicClaudeText(Flavor):
    record_format_type = "anthropic_text"
    _model_params_with_defaults = LLMParameters({
        "model": "claude-v1",
        "max_tokens_to_sample": 100
    })

    def __init__(self) -> None:
        self.client = None

    @property
    def provider(self) -> str:
        return "anthropic"

    def get_anthropic_client(self, anthropic_config: Optional[AnthropicConfig]) -> Any:
        if self.client:
            return self.client

        if not anthropic_config:
            raise APIKeyMissingError(
                "Missing Anthropic key. Use a ProviderConfig to specify keys prior to getting completion.")

        self.client = anthropic.Client(anthropic_config.api_key)
        return self.client

    def format(self, prompt_template: PromptTemplateWithMetadata, variables: dict[str, str]) -> str:
        interpolated_prompt = format_template_variables(prompt_template.content, variables)
        # Anthropic expects a specific Chat format "Human: $PROMPT_TEXT\n\nAssistant:". We add the wrapping for Text.
        chat_formatted_prompt = f"{anthropic.HUMAN_PROMPT} {interpolated_prompt} {anthropic.AI_PROMPT}"
        return chat_formatted_prompt

    def call_service(self, formatted_prompt: str, provider_config: ProviderConfig,
                     llm_parameters: LLMParameters) -> CompletionResponse:
        client = self.get_anthropic_client(provider_config.anthropic)
        anthropic_response = client.completion(
            prompt=formatted_prompt,
            **self.get_model_params(llm_parameters)
        )
        return CompletionResponse(
            content=anthropic_response['completion'],
            is_complete=anthropic_response['stop_reason'] == 'stop_sequence'
        )

    def call_service_stream(
            self,
            formatted_prompt: str,
            provider_config: ProviderConfig,
            llm_parameters: LLMParameters
    ) -> Generator[CompletionChunk, None, None]:
        client = self.get_anthropic_client(provider_config.anthropic)
        anthropic_response = client.completion_stream(
            prompt=formatted_prompt,
            **self.get_model_params(llm_parameters)
        )

        # Yield incremental text completions. Claude returns the full text output in every chunk.
        # We want to predictably return a stream like we do for OpenAI.
        prev_chunk = ''
        for chunk in anthropic_response:
            if len(prev_chunk) != 0:
                incremental_new_text = chunk['completion'].split(prev_chunk)[1]
            else:
                incremental_new_text = chunk['completion']

            prev_chunk = chunk['completion']
            yield CompletionChunk(
                text=incremental_new_text,
                is_complete=chunk['stop_reason'] == 'stop_sequence'
            )
