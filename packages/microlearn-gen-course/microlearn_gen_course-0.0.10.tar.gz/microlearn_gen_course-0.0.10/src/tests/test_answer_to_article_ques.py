"""
Test GenAnswerToArticleQues class.

Usage:
    pytest src/tests/test_answer_to_article_ques.py -v --log-cli-level INFO
"""
import logging
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from gen_course.gen_answer_to_article_ques import GenAnswerToArticleQues

from llm_factory.llm_factory import LLMFactory


load_dotenv(override=True)

logger = logging.getLogger(__name__)


def test_generate():
    llm = LLMFactory().build_llm(
        llm_type=LLMFactory.LLM_OPENAI_CHAT_NAME,
        model_name="gpt-4",
        temperature=0.0,
        max_tokens=256,
        pl_tags=["microlearnai", "gen_course",
                 "answer_to_article_ques"],
    )
    gen = GenAnswerToArticleQues(llm=llm, verbose=True)
    output = gen.generate(
        course_title="Introductory Python Course",
        course_description="Master the basics of Python programming language starting from zero knowledge.",
        article_title="Introduction to Python Programming",
        article_content="""Dive into the world of Python, a versatile and powerful programming language. With its simple syntax, Python is a great choice for beginners. It's widely used in various fields, from web development to data analysis. This course will guide you through the basics, including variables, data types, and control structures. You'll also learn about Python's rich library of modules, which can help you tackle complex tasks with ease. By the end of this course, you'll have a solid foundation in Python and be ready to explore more advanced topics.""",
        question="What are some practical applications of Python in different fields?",
        content_length_words=150,
    )
    logger.info(f"article's question's answer: {output.answer}")
    assert len(output.answer.split()) <= 150
