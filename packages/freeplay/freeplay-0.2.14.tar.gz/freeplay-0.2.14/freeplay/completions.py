from dataclasses import dataclass
from typing import Optional, Any

from .llm_parameters import LLMParameters

ChatMessage = dict[str, str]
OpenAIFunctionCall = dict[str, str]


@dataclass
class CompletionResponse:
    content: str
    is_complete: bool
    openai_function_call: Optional[OpenAIFunctionCall] = None

@dataclass
class ChatCompletionResponse:
    content: str
    is_complete: bool
    message_history: list[ChatMessage]


@dataclass
class PromptTemplateWithMetadata:
    project_version_id: str
    prompt_template_id: str
    name: str
    content: str
    flavor_name: Optional[str]
    params: Optional[dict[str, Any]]

    def get_params(self) -> LLMParameters:
        return LLMParameters.empty() if self.params is None else LLMParameters(self.params)


@dataclass
class PromptTemplates:
    templates: list[PromptTemplateWithMetadata]


@dataclass
class CompletionChunk:
    text: str
    is_complete: bool
    openai_function_call: Optional[OpenAIFunctionCall] = None
