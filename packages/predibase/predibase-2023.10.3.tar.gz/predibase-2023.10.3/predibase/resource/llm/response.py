from dataclasses import dataclass
from typing import Dict, List, Optional

import pandas as pd
from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GeneratedResponse:
    prompt: str
    response: str
    raw_prompt: Optional[str] = None
    sample_index: Optional[int] = None
    sample_data: Dict[str, any] = None
    context: Optional[str] = None
    model_name: Optional[str] = None
    finish_reason: Optional[str] = None
    generated_tokens: Optional[int] = None

    @staticmethod
    def to_responses(df: pd.DataFrame) -> List["GeneratedResponse"]:
        return [GeneratedResponse(**row.to_dict()) for _, row in df.iterrows()]

    @staticmethod
    def to_pandas(responses: List["GeneratedResponse"]) -> pd.DataFrame:
        return pd.DataFrame([response.to_dict() for response in responses])
