"""
Generator for course's articles titles.
"""
import json
import logging
from typing import List
from pydantic import BaseModel, Field

from .gen_base_v2 import GenBaseV2


class CourseArticlesTitlesModel(BaseModel):
    titles: List[str] = Field(
        description="List of course's articles titles. All the titles are unique and sequential for the course.")


class GenCourseArticleTitles(GenBaseV2):
    """
    Generator class for course's articles titles.
    """
    HUMAN_PROMPT = """I'm developing a micro learning course about the following:
---
Title: {course_title}
Description: {course_description}
---
Write {articles_count} titles for the articles of the course. Each title should be maximum of {title_length_words} words.
Strictly output in JSON format. The JSON should have the following format: 
[
   "...",
]"""

    def __init__(self, llm, verbose: bool = False):
        self.logger = logging.getLogger(__name__)
        super().__init__(llm, verbose, self.logger)

    def parse_output(self, output: str) -> CourseArticlesTitlesModel:
        try:
            self.logger.debug(f"Parsing output: {output}")
            titles = json.loads(output)
            return CourseArticlesTitlesModel(titles=titles)
        except json.JSONDecodeError:
            self.logger.error(f"Output is not a valid JSON: {output}")
            raise

    def generate(self,
                 course_title: str,
                 course_description: str,
                 articles_count: int,
                 title_length_words: int = 8,
                 ) -> CourseArticlesTitlesModel:
        return self.generate_output(
            course_title=course_title,
            course_description=course_description,
            articles_count=articles_count,
            title_length_words=title_length_words,
        )
