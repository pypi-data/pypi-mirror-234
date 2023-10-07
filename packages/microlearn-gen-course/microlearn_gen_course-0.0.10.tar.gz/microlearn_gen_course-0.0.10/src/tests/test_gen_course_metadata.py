"""
Test GenCourseMetadata

Usage:
    pytest src/tests/test_gen_course_metadata.py -v --log-cli-level INFO
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from llm_factory.llm_factory import LLMFactory
from gen_course.gen_course_metadata import GenCourseMetadata
from dotenv import load_dotenv
import logging


load_dotenv(override=True)

logger = logging.getLogger(__name__)


def test_generate():
    llm = LLMFactory().build_llm(
        llm_type=LLMFactory.LLM_OPENAI_CHAT_NAME,
        model_name="gpt-4",
        temperature=0.0,
        max_tokens=256,
        pl_tags=["microlearnai", "gen_course", "gen_course_metadata"],
    )
    gen = GenCourseMetadata(llm=llm, verbose=True)
    output = gen.generate(
        course_description="Generate a course about Python programming language for beginners.",
    )
    logger.info(f"course's title: {output.title}")
    logger.info(f"course's description: {output.description}")
    assert len(output.title) >= 2 and len(output.title.split()) <= 4
    assert len(output.description.split()) <= 40
