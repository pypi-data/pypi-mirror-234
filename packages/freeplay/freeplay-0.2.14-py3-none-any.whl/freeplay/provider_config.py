from dataclasses import dataclass
from typing import Optional

from .errors import APIKeyMissingError


@dataclass
class OpenAIConfig:
    api_key: str
    api_base: Optional[str]

    def __init__(self, api_key: str, api_base: Optional[str] = None) -> None:
        self.api_key = api_key
        self.api_base = api_base

    def validate(self) -> None:
        if not self.api_key or not self.api_key.strip():
            raise APIKeyMissingError("OpenAI API key not set. It must be set to make calls to the service.")


@dataclass
class AnthropicConfig:
    api_key: str


@dataclass
class ProviderConfig:
    anthropic: Optional[AnthropicConfig] = None
    openai: Optional[OpenAIConfig] = None

    def validate(self) -> None:
        if self.anthropic is None and self.openai is None:
            APIKeyMissingError("At least one provider key must be set in ProviderConfig.")
        if self.openai is not None:
            self.openai.validate()

