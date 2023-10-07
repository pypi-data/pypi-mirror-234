"""
Base generator class for all content generators.
"""
from abc import ABC, abstractmethod
from logging import Logger
from typing import Any

from langchain.chains import LLMChain
from langchain.prompts import (ChatPromptTemplate, HumanMessagePromptTemplate,
                               SystemMessagePromptTemplate)


class GenBaseV2(ABC):
    SYSTEM_PROMPT = "You act as a helpful content writer AI assistant."
    HUMAN_PROMPT = None

    def __init__(self, llm, verbose: bool = False, logger: Logger = None):
        self.logger = logger
        chat_prompt = ChatPromptTemplate.from_messages([
            self._get_system_prompt(),
            self._get_human_prompt(),
        ])
        self._chain = LLMChain(
            llm=llm,
            prompt=chat_prompt,
            verbose=verbose,
        )

    def _get_system_prompt(self):
        return SystemMessagePromptTemplate.from_template(self.SYSTEM_PROMPT)

    def _get_human_prompt(self):
        return HumanMessagePromptTemplate.from_template(self.HUMAN_PROMPT)

    @abstractmethod
    def parse_output(self, output: str) -> Any:
        raise NotImplementedError

    def generate_output(self, **kwargs) -> Any:
        output = self._chain.run(**kwargs)
        return self.parse_output(output)
