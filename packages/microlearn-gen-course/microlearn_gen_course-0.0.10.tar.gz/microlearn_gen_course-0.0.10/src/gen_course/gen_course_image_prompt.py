"""
Generator for course's image generation prompt via other tools like MidJourney.
"""
import json
import logging
from pydantic import BaseModel, Field

from .gen_base_v2 import GenBaseV2


class CourseImagePromptModel(BaseModel):
    prompt: str = Field(
        description="prompt of maximum 30 words for image generation of the course.")


class GenCourseImagePrompt(GenBaseV2):
    """
    Generator class for course image prompt.
    """
    SYSTEM_PROMPT = """Act like a photo editor that defines the perfect image for an article and craft a prompt directing Midjourney to generate a photo-realistic image that will be published with the article. Include essential details and do not exceed {prompt_length_words} words.
No textual or letter elements should be included in the image.
Only write the prompt."""
    HUMAN_PROMPT = """The image I need is for the course described below:
---
Description: {description}
---
Strictly output in JSON format. The JSON should have the following format:
{{
    "prompt": "..."
}}"""

    def __init__(self, llm, verbose: bool = False):
        self.logger = logging.getLogger(__name__)
        super().__init__(llm, verbose, self.logger)

    def parse_output(self, output: str) -> CourseImagePromptModel:
        try:
            self.logger.debug(f"Parsing output: {output}")
            prompt = json.loads(output)
            return CourseImagePromptModel(**prompt)
        except json.JSONDecodeError:
            self.logger.error(f"Output is not a valid JSON: {output}")
            raise

    def generate(self,
                 description: str,
                 prompt_length_words: int = 30,
                 ) -> CourseImagePromptModel:
        return self.generate_output(
            description=description,
            prompt_length_words=prompt_length_words,
        )
