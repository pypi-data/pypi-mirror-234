"""
Test GenCourseArticleContent

Usage:
    pytest src/tests/test_gen_course_article_content.py -v --log-cli-level INFO
"""
import logging
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from llm_factory.llm_factory import LLMFactory
from gen_course.gen_course_article_content import (
    GenCourseArticleContent,
    GenCourseArticleContentUsingPreviousArticles,
    GenCourseArticleContentInBatchWPrevArticles,
    GenCourseContentForAllArticles,
)

load_dotenv(override=True)

logger = logging.getLogger(__name__)


# def test_generate():
#     llm = LLMFactory().build_llm(
#         llm_type=LLMFactory.LLM_OPENAI_CHAT_NAME,
#         model_name="gpt-4",
#         temperature=0.0,
#         max_tokens=256,
#         pl_tags=["microlearnai", "gen_course", "gen_course_article_content"],
#     )
#     gen = GenCourseArticleContent(llm=llm, verbose=True)
#     output = gen.generate(
#         course_title="Introductory Python Course",
#         course_description="Master the basics of Python programming language starting from zero knowledge.",
#         article_title="Introduction to Python Programming",
#     )
#     logger.info(f"course's article's content: {output.content}")
#     logger.info(f"course's article's questions: {output.questions}")
#     assert len(output.questions) == 3
#     assert len(output.content.split()) <= 150


# def test_generate_using_prev_articles():
#     llm = LLMFactory().build_llm(
#         llm_type=LLMFactory.LLM_OPENAI_CHAT_NAME,
#         model_name="gpt-4",
#         temperature=0.0,
#         max_tokens=256,
#         pl_tags=["microlearnai", "gen_course",
#                  "gen_course_article_content_w_prev_articles"],
#     )
#     gen = GenCourseArticleContentUsingPreviousArticles(llm=llm, verbose=True)
#     output = gen.generate(
#         course_title="Insulin resistance",
#         course_description="Explain to a broad audience what is insulin resistance and how to cure it based on traditional advice and exercising plan and healthy habits. Also explain consequences of insulin resistance. Your audience is 50-year-olds with no medical expertise so keep the language very simple.",
#         article_title="Exercising to Cure Insulin Resistance",
#         previous_articles=[
#             """Insulin resistance is a condition in which the body's cells do not respond to insulin normally. This means that insulin cannot effectively move blood sugar (glucose) into cells, causing glucose levels in the blood to remain high. Insulin resistance can be caused by lifestyle factors such as unhealthy eating habits and lack of physical activity, as well as genetic factors.""",
#             """Insulin resistance occurs when the body's cells don't respond properly to insulin, leading to high blood sugar levels. This may be caused by genetics, a sedentary lifestyle, certain medications or medical conditions like obesity, polycystic ovarian syndrome (PCOS) and type 2 diabetes. Other factors that can contribute include age and diet choices with too much fat and sugar in it.""",
#             """Insulin resistance is a condition in which the body does not respond to insulin as it should, leading to high blood sugar levels. Recognizing the symptoms of insulin resistance can help you prevent more serious health complications. Symptoms include fatigue, weight gain and difficulty losing weight, excessive thirst, frequent urination and blurry vision. If left untreated, insulin resistance can lead to type 2 diabetes or heart disease.""",
#             """Traditional advice for treating insulin resistance includes eating a healthy, balanced diet with low levels of refined sugars and grains. Eating more natural whole foods such as fruits, vegetables, lean proteins and complex carbohydrates is key to reversing insulin resistance. Regular exercise helps the body use insulin better and can also reduce weight which further decreases the risk of developing diabetes or other metabolic conditions. Additionally, it is important to get enough restful sleep in order to keep hormones like cortisol from spiking too high which could increase blood sugar levels.""",
#         ],
#     )
#     logger.info(f"course's article's content: {output.content}")
#     logger.info(f"course's article's questions: {output.questions}")
#     assert len(output.questions) == 3
#     assert len(output.content.split()) <= 150


# def assert_article(article, exp_title):
#     logger.debug(f"course's article title: {article.title}")
#     logger.debug(f"course's article content: {article.content}")
#     logger.debug(f"course's article questions: {article.questions}")
#     assert article.title == exp_title
#     assert len(article.questions) == 3
#     assert len(article.content.split()) <= 150


# def test_generate_articles_in_batch():
#     llm = LLMFactory().build_llm(
#         llm_type=LLMFactory.LLM_OPENAI_CHAT_NAME,
#         model_name="gpt-4",
#         temperature=0.0,
#         max_tokens=1024,
#         pl_tags=["microlearnai", "gen_course",
#                  "gen_course_article_content_in_batch_w_prev_articles"],
#     )
#     gen = GenCourseArticleContentInBatchWPrevArticles(llm=llm, verbose=True)
#     output = gen.generate(
#         course_title="Photography Basics 101",
#         course_description="Unleash your creative potential with our Photography Basics 101 course. Designed for beginners, this course will guide you through the fundamental skills needed to capture stunning images.",
#         title_list=[
#             "The Importance of Lighting in Photography",
#             "Getting to Know Your Camera Settings",
#             "The Basics of Portrait Photography",
#         ],
#         previous_articles_title_list=[
#             "Understanding Your Camera: An Introduction",
#             "Mastering the Art of Composition",
#             "Exploring Different Photography Genres",
#         ],
#     )
#     assert len(output) == 3
#     assert_article(output[0], "The Importance of Lighting in Photography")
#     assert_article(output[1], "Getting to Know Your Camera Settings")
#     assert_article(output[2], "The Basics of Portrait Photography")


def test_generate_articles_all():
    llm = LLMFactory().build_llm(
        llm_type=LLMFactory.LLM_OPENAI_CHAT_NAME,
        model_name="gpt-4",
        temperature=0.0,
        max_tokens=7500,
        pl_tags=["microlearnai", "gen_course",
                 "gen_course_content_for_all_articles"],
    )
    gen = GenCourseContentForAllArticles(llm=llm, verbose=True)
    output = gen.generate(
        course_title="Photography Basics 101",
        course_description="Unleash your creative potential with our Photography Basics 101 course. Designed for beginners, this course will guide you through the fundamental skills needed to capture stunning images.",
    )
    assert len(output) == 10
    for i, article in enumerate(output):
        logger.info(f"Article [{i+1}] title length: {len(output[i].title.split())}")
        logger.info(f"Article [{i+1}] content length: {len(output[i].content.split())}")
        assert len(article.questions) == 3
        assert len(article.content.split()) <= 150
