from dataclasses import dataclass, field
from typing import List, Dict, Union, Optional

@dataclass
class MethodArgs:
    methods: List[List[str]]

@dataclass
class Prompt:
    name: str
    template: List[str]

@dataclass
class Message:
    name: str
    format: str
    content: str

@dataclass
class MetaData:
    metric: List[str]
    topic: List[str]
    keywords: List[str]

@dataclass
class Information:
    name: str
    description: str

@dataclass
class PromptFragment:
    name: str
    type: str
    content: Union[str, Dict]
    callable: Optional[str] = field(default=None)
