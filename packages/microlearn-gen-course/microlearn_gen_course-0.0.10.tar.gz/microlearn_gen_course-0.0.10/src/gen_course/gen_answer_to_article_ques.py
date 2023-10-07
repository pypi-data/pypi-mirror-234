"""
Generator for course's article's question's answer.
"""
import json
import logging
from pydantic import BaseModel, Field

from .gen_base_v2 import GenBaseV2


class ArticleQuesAnswerModel(BaseModel):
    answer: str = Field(description="Article's question's answer")


class GenAnswerToArticleQues(GenBaseV2):
    """
    Generator class to answer article's question.
    """
    HUMAN_PROMPT = """I've developed a micro learning course about the following:
---
Course title: {course_title}
Course description: {course_description}
Article title: {article_title}
Article content: {article_content}
---
Based on the information specified above, answer the question: "{question}" with maximum length of {content_length_words} words.
Strictly output in JSON format. The JSON should have the following format:
{{
   "answer": "..."
}}"""

    def __init__(self, llm, verbose: bool = False):
        self.logger = logging.getLogger(__name__)
        super().__init__(llm, verbose, self.logger)

    def parse_output(self, output: str) -> ArticleQuesAnswerModel:
        try:
            self.logger.debug(f"Parsing output: {output}")
            answer = json.loads(output)
            return ArticleQuesAnswerModel(**answer)
        except json.JSONDecodeError:
            self.logger.error(f"Output is not a valid JSON: {output}")
            raise

    def generate(self,
                 course_title: str,
                 course_description: str,
                 article_title: str,
                 article_content: str,
                 question: str,
                 content_length_words: int = 150,
                 ) -> ArticleQuesAnswerModel:
        return self.generate_output(
            course_title=course_title,
            course_description=course_description,
            article_title=article_title,
            article_content=article_content,
            question=question,
            content_length_words=content_length_words,
        )
