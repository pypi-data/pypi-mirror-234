from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, validator


class TextPrompt(BaseModel):
    text: str
    weight: int


class TextToImageRequestBody(BaseModel):
    model: str = "accounts/fireworks/models/stable-diffusion-xl-1024-v1-0"
    cfg_scale: int = 7
    clip_guidance_preset: str = "NONE"
    height: int = 1024
    width: int = 1024
    sampler: Optional[str] = None
    samples: int = 1
    steps: int = 50
    seed: int = 0
    style_preset: Optional[str] = None
    text_prompts: List[TextPrompt]


class ImageToImageRequestBody(BaseModel):
    model: str = "accounts/fireworks/models/stable-diffusion-xl-1024-v1-0"
    cfg_scale: int = Field(default=7)
    clip_guidance_preset: str = "NONE"
    sampler: Optional[str]
    samples: int = 1
    steps: int = 50
    seed: int = 0
    style_preset: Optional[str]

    init_image_mode: str = "IMAGE_STRENGTH"
    image_strength: Optional[float]
    step_schedule_start: Optional[float] = 0.65
    step_schedule_end: Optional[float]

    @validator("image_strength", pre=True, always=True)
    def validate_image_strength(cls, v, values):
        if values["init_image_mode"] == "IMAGE_STRENGTH" and v is None:
            raise ValueError(
                "image_strength is required when init_image_mode is IMAGE_STRENGTH"
            )
        return v

    @validator("step_schedule_start", "step_schedule_end", pre=True, always=True)
    def validate_step_schedule(cls, v, values):
        if values["init_image_mode"] == "STEP_SCHEDULE" and v is None:
            raise ValueError(
                "Both step_schedule_start and step_schedule_end are required when init_image_mode is STEP_SCHEDULE"
            )
        return v
