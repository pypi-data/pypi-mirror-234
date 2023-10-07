"""
Base generator class for all content generators.
"""
from abc import ABC, abstractmethod
from typing import Any

from langchain.chains import LLMChain
from langchain.prompts import (ChatPromptTemplate, HumanMessagePromptTemplate,
                               PromptTemplate, SystemMessagePromptTemplate)


class GenBase(ABC):
    SYSTEM_PROMPT = "You act as a helpful content writer AI assistant."
    HUMAN_PROMPT = None

    def __init__(self, llm, verbose: bool = False):
        self._output_parser = self.get_output_parser()
        self._format_instructions = self._output_parser.get_format_instructions()
        chat_prompt = ChatPromptTemplate.from_messages([
            self._get_system_prompt(),
            self._get_human_prompt(),
        ])
        self._chain = LLMChain(
            llm=llm,
            prompt=chat_prompt,
            verbose=verbose,
        )

    @abstractmethod
    def get_output_parser(self):
        raise NotImplementedError

    def _get_system_prompt(self):
        return SystemMessagePromptTemplate.from_template(self.SYSTEM_PROMPT)

    def _get_human_prompt(self):
        human_msg_prompt = HumanMessagePromptTemplate.from_template(
            self.HUMAN_PROMPT)
        human_msg_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template=human_msg_prompt.prompt.template +
                "\n{format_instructions}",
                input_variables=human_msg_prompt.prompt.input_variables,
                partial_variables={
                    "format_instructions": self._format_instructions},
            )
        )
        return human_msg_prompt

    def generate_output(self, **kwargs) -> Any:
        output = self._chain.run(**kwargs)
        return self._output_parser.parse(output)
