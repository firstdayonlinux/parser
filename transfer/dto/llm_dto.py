from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from transfer.dto.base import BaseDTO


@dataclass(frozen=True)
class LlmDTO(BaseDTO):
    content: str
    llm_response: Optional[str]


@dataclass(frozen=True)
class CreatedLlmDTO(LlmDTO):
    id: UUID
