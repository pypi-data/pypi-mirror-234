"""
Generator for course's metadata(title, description, etc.) using the description as text.
"""
import json
import logging
from pydantic import BaseModel, Field

from .gen_base_v2 import GenBaseV2


class CourseMetadataModel(BaseModel):
    title: str = Field(
        description="title of the course of only 3 words")
    description: str = Field(
        description="description of the course which is an introduction article of maximum 40 words")


class GenCourseMetadata(GenBaseV2):
    """
    Generator class for course metadata(title, description, etc.) using the description as text.
    """
    SYSTEM_PROMPT = """Act like a copywriter expert in course editing"""
    HUMAN_PROMPT = """Write a title of only 3 words and an introduction article to a course of aproximately 40 words based on the following:
---
Description: {course_description}
---
Strictly output in JSON format. The JSON should have the following format:
{{
    "title": "...",
    "description": "..."
}}"""

    def __init__(self, llm, verbose: bool = False):
        self.logger = logging.getLogger(__name__)
        super().__init__(llm, verbose, self.logger)

    def parse_output(self, output: str) -> CourseMetadataModel:
        try:
            self.logger.debug(f"Parsing output: {output}")
            metadata = json.loads(output)
            return CourseMetadataModel(**metadata)
        except json.JSONDecodeError:
            self.logger.error(f"Output is not a valid JSON: {output}")
            raise

    def generate(self,
                 course_description: str,
                 ) -> CourseMetadataModel:
        return self.generate_output(
            course_description=course_description,
        )
