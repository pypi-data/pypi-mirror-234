"""
Test GenCourseImagePrompt

Usage:
    pytest src/tests/test_gen_course_image_prompt.py -v --log-cli-level INFO
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import logging
from dotenv import load_dotenv
from gen_course.gen_course_image_prompt import GenCourseImagePrompt
from llm_factory.llm_factory import LLMFactory

load_dotenv(override=True)

logger = logging.getLogger(__name__)


def test_generate():
    llm = LLMFactory().build_llm(
        llm_type=LLMFactory.LLM_OPENAI_CHAT_NAME,
        model_name="gpt-4",
        temperature=0.0,
        max_tokens=256,
        pl_tags=["microlearnai", "gen_course", "gen_course_image_prompt"],
    )
    gen = GenCourseImagePrompt(llm=llm, verbose=True)
    output = gen.generate(
        description="Unleash your creative potential with our Photography Basics 101 course. Designed for beginners, this course will guide you through the fundamental skills needed to capture stunning images.",
    )
    logger.info(f"image gen prompt: {output.prompt}")
    assert len(output.prompt.split()) <= 30
