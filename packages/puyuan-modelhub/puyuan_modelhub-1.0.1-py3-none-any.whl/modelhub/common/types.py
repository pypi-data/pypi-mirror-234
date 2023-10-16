from pydantic import BaseModel
from typing import Dict, Optional, Any, List


class GenerationParams(BaseModel):
    inputs: str
    parameters: Dict[str, Any] = {}


class TextGenerationStreamToken(BaseModel):
    id: int
    text: str
    logprob: float
    special: bool


class TextGenerationStreamDetails(BaseModel):
    finish_reason: Optional[str] = None
    prompt_tokens: Optional[int] = None
    generated_tokens: Optional[int] = None
    seed: Optional[int] = None
    tokens: Optional[List[TextGenerationStreamToken]] = None


class TextGenerationStreamOutput(BaseModel):
    token: TextGenerationStreamToken
    generated_text: Optional[str] = None
    details: Optional[TextGenerationStreamDetails] = None


class TextGenerationOutput(BaseModel):
    generated_text: str
    details: Optional[TextGenerationStreamDetails] = None
