from typing import List, Optional, Union
from .image_api import ImageToImageRequestBody, TextToImageRequestBody, TextPrompt

import fireworks.client
import httpx
from PIL import Image
import io
import copy
import os


class ImageInference:
    """
    Main client class for the Fireworks Image Generation API. Currently supports Stable Diffusion
    XL 1.0 (see https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0). This client
    supports both text-to-image and image-to-image generation.

    Attributes:
    - base_url (str): Base URL for the image generation API. Defaults to `fireworks.client.base_url`, which should
                      be set at initialization.
    - api_key (str): API key for authentication. Defaults to `fireworks.client.api_key`, which should be set at
                     initialization.
    """

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = base_url or fireworks.client.base_url
        self.api_key = api_key or fireworks.client.api_key

        self.client = httpx.Client()
        self.endpoint_base_uri = f"{self.base_url}/image_generation/stable_diffusion"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
        }

    def text_to_image(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        cfg_scale: int = 7,
        clip_guidance_preset: str = "NONE",
        height: int = 1024,
        width: int = 1024,
        sampler: Optional[str] = None,
        samples: int = 1,
        steps: int = 50,
        seed: int = 0,
        style_preset: Optional[str] = None,
    ) -> Union[Image.Image, List[Image.Image]]:
        """
        Generate an image or images based on the given text prompt and optional negative prompt.
        See the OpenAPI spec (https://readme.fireworks.ai/reference/post_image-generation-stable-diffusion)
        for the most up-to-date description of the supported parameters

        Parameters:
        - prompt (str): The main text prompt based on which the image will be generated.
        - negative_prompt (str, optional): A secondary text prompt which can be used to guide the image generation in a negative way.
        - cfg_scale (int, optional): Configuration scale for the image generation. Defaults to 7.
        - clip_guidance_preset (str, optional): CLIP guidance preset. Defaults to "NONE".
        - height (int, optional): Desired height of the generated image. Defaults to 1024.
        - width (int, optional): Desired width of the generated image. Defaults to 1024.
        - sampler (str, optional): Sampler type. Optional.
        - samples (int, optional): Number of images to be generated. Defaults to 1.
        - steps (int, optional): Number of steps for the generation process. Defaults to 50.
        - seed (int, optional): Seed for random number generation. Defaults to 0.
        - style_preset (str, optional): Style preset for the generated image. Optional.

        Returns:
        Image.Image or List[Image.Image]: Generated image or a list of generated images.

        Raises:
        RuntimeError: If there is an error in the image generation process.
        """
        text_prompts = [
            TextPrompt(text=prompt, weight=1.0),
        ]
        if negative_prompt:
            text_prompts.append(TextPrompt(text=negative_prompt, weight=-1.0))
        request_body = TextToImageRequestBody(
            cfg_scale=cfg_scale,
            clip_guidance_preset=clip_guidance_preset,
            height=height,
            width=width,
            sampler=sampler,
            samples=samples,
            steps=steps,
            seed=seed,
            style_preset=style_preset,
            text_prompts=text_prompts,
        )
        payload_dict = request_body.dict()
        headers_copy = copy.copy(self.headers)
        headers_copy["Content-Type"] = "application/json"
        if samples == 1:
            headers_copy["Accept"] = "image/png"
        else:
            headers_copy["Accept"] = "application/json"
        response = self.client.post(
            self.endpoint_base_uri, headers=headers_copy, json=payload_dict, timeout=300
        )
        if response.status_code == 200:
            if samples == 1:
                return Image.open(io.BytesIO(response.content))
            else:
                return [
                    Image.open(io.BytesIO(artifact.binary))
                    for artifact in response.json()["artifacts"]
                ]
        else:
            raise RuntimeError(
                f"Failed to generate image: HTTP {response.status_code}, {response.text}"
            )

    def image_to_image(
        self,
        init_image: Union[Image.Image, str, os.PathLike, bytes],
        prompt: str,
        negative_prompt: Optional[str] = None,
        cfg_scale: int = 7,
        clip_guidance_preset: str = "NONE",
        sampler: Optional[str] = None,
        samples: int = 1,
        steps: int = 50,
        seed: int = 0,
        style_preset: Optional[str] = None,
        init_image_mode: str = "IMAGE_STRENGTH",
        image_strength: Optional[float] = None,
        step_schedule_start: Optional[float] = 0.65,
        step_schedule_end: Optional[float] = None,
    ):
        """
        Modify an existing image based on a given text prompt and optional negative prompt.
        See the OpenAPI spec (https://readme.fireworks.ai/reference/post_image-generation-stable-diffusion)
        for the most up-to-date description of the supported parameters

        Parameters:
        - init_image (Union[Image.Image, str, os.PathLike, bytes]): Initial image to be modified. It can be provided as a PIL Image object, path to an image, or raw bytes.
        - prompt (str): The main text prompt based on which the image will be modified.
        - negative_prompt (str, optional): A secondary text prompt which can be used to guide the image modification in a negative way.
        - cfg_scale (int, optional): Configuration scale for the image modification. Defaults to 7.
        - clip_guidance_preset (str, optional): CLIP guidance preset. Defaults to "NONE".
        - sampler (str, optional): Sampler type. Optional.
        - samples (int, optional): Number of images to be generated. Defaults to 1.
        - steps (int, optional): Number of steps for the modification process. Defaults to 50.
        - seed (int, optional): Seed for random number generation. Defaults to 0.
        - style_preset (str, optional): Style preset for the modified image. Optional.
        - init_image_mode (str, optional): Initialization mode for the image modification. Defaults to "IMAGE_STRENGTH".
        - image_strength (float, optional): Strength of the initial image. Required when init_image_mode is "IMAGE_STRENGTH".
        - step_schedule_start (float, optional): Start of the step schedule. Required when init_image_mode is "STEP_SCHEDULE". Defaults to 0.65.
        - step_schedule_end (float, optional): End of the step schedule. Required when init_image_mode is "STEP_SCHEDULE".

        Returns:
        Image.Image or List[Image.Image]: Modified image or a list of modified images.

        Raises:
        ValueError: If required parameters are missing based on the given init_image_mode.
        RuntimeError: If there is an error in the image modification process.
        """
        # Argument Validation
        if init_image_mode == "IMAGE_STRENGTH" and image_strength is None:
            raise ValueError(
                "image_strength is required when init_image_mode is IMAGE_STRENGTH"
            )
        if init_image_mode == "STEP_SCHEDULE" and (
            step_schedule_start is None or step_schedule_end is None
        ):
            raise ValueError(
                "Both step_schedule_start and step_schedule_end are required when init_image_mode is STEP_SCHEDULE"
            )

        # Construct and validate request fields.
        # NB: prompt and init_image are not used here. Instead, we construct
        # them specially to be sent as multipart/form-data
        request_body = ImageToImageRequestBody(
            cfg_scale=cfg_scale,
            clip_guidance_preset=clip_guidance_preset,
            sampler=sampler,
            samples=samples,
            steps=steps,
            seed=seed,
            style_preset=style_preset,
            init_image_mode=init_image_mode,
            image_strength=image_strength,
            step_schedule_start=step_schedule_start,
            step_schedule_end=step_schedule_end,
        )
        payload_dict = request_body.dict()

        # Special fields
        payload_dict["text_prompts[0][text]"] = prompt
        payload_dict["text_prompts[0][weight]"] = 1.0
        if negative_prompt:
            payload_dict["text_prompts[1][text]"] = negative_prompt
            payload_dict["text_prompts[1][weight]"] = -1.0

        headers_copy = copy.copy(self.headers)
        if samples == 1:
            headers_copy["Accept"] = "image/png"
        else:
            headers_copy["Accept"] = "application/json"

        # Normalize all forms of `init_image` into a `bytes` object
        # to send over the wire
        if isinstance(init_image, Image.Image):
            img_bio = io.BytesIO()
            init_image.save(img_bio, format="PNG")
            init_image = img_bio.getvalue()
        elif isinstance(init_image, (str, os.PathLike)):
            with open(init_image, "rb") as f:
                init_image = f.read()

        files = {
            "init_image": init_image,
        }
        response = self.client.post(
            f"{self.endpoint_base_uri}/image_to_image",
            headers=headers_copy,
            data=payload_dict,
            files=files,
            timeout=300,
        )
        if response.status_code == 200:
            if samples == 1:
                return Image.open(io.BytesIO(response.content))
            else:
                return [
                    Image.open(io.BytesIO(artifact.binary))
                    for artifact in response.json()["artifacts"]
                ]
        else:
            raise RuntimeError(
                f"Failed to generate image: HTTP {response.status_code}, {response.text}"
            )
