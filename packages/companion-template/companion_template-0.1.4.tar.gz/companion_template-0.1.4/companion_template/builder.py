import toml
from typing import List, Dict
from dataclasses import asdict
from .template_types import *

@dataclass
class DeclarativeFeedConfig:
    information: Information
    meta_data: MetaData
    messages: List[Message]
    prompts: List[Prompt]
    prompt_fragments: List[PromptFragment]
    method_args: MethodArgs

@dataclass
class DeclarativeFeedBuilder:
    _prompt_fragments: List[PromptFragment] = field(default_factory=list)
    _prompts: List[Prompt] = field(default_factory=list)
    _messages: List[Message] = field(default_factory=list)
    _information: Optional[Information] = None
    _meta_data: Optional[MetaData] = None
    _method_args: Optional[MethodArgs] = None

    def add_prompt_fragment(self, prompt_fragment: PromptFragment):
        self._prompt_fragments.append(prompt_fragment)
        return self

    def add_prompt(self, prompt: Prompt):
        self._prompts.append(prompt)
        return self

    def add_message(self, message: Message):
        self._messages.append(message)
        return self

    def set_information(self, information: Information):
        self._information = information
        return self

    def set_meta_data(self, meta_data: MetaData):
        self._meta_data = meta_data
        return self

    def set_method_args(self, method_args: MethodArgs):
        self._method_args = method_args
        return self

    def _validate(self):
        # Check that necessary prompts exist for messages
        prompt_names = [prompt.name for prompt in self._prompts]
        for message in self._messages:
            if message.content not in prompt_names:
                raise ValueError(f"Missing prompt '{message.content}' for message '{message.name}'.")

        fragment_names = [fragment.name for fragment in self._prompt_fragments]
        for prompt in self._prompts:
            for template_item in prompt.template:
                if template_item not in fragment_names:
                    raise ValueError(f"Missing prompt fragment '{template_item}' for prompt '{prompt.name}'.")

    def build(self):
        self._validate()
        if not all([self._information, self._meta_data]):
            raise ValueError("Missing required fields for Config.")

        return DeclarativeFeedConfig(
            information=self._information,
            meta_data=self._meta_data,
            messages=self._messages,
            prompts=self._prompts,
            prompt_fragments=self._prompt_fragments,
            method_args=self._method_args
        )