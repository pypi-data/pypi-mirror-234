"""
Test GenCourseArticlesTitles

Usage:
    pytest src/tests/test_gen_course_articles_titles.py -v --log-cli-level INFO
"""
import logging
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from gen_course.gen_course_articles_titles import GenCourseArticleTitles

from llm_factory.llm_factory import LLMFactory


load_dotenv(override=True)

logger = logging.getLogger(__name__)


def test_generate():
    llm = LLMFactory().build_llm(
        llm_type=LLMFactory.LLM_OPENAI_CHAT_NAME,
        model_name="gpt-4",
        temperature=0.0,
        max_tokens=256,
        pl_tags=["microlearnai", "gen_course", "gen_course_articles_titles"],
    )
    gen = GenCourseArticleTitles(llm=llm, verbose=True)
    output = gen.generate(
        course_title="Python for Beginners",
        course_description="Learn Python from scratch.",
        articles_count=5,
    )
    logger.info(f"course's articles titles: {output.titles}")
    assert len(output.titles) == 5
