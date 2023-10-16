from typing import Optional

from langchain import LLMChain
from langchain.chains.base import Chain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

import config


def get_simple_chat_chain(
        system,
        openai_api_key=None,
        chat_model_kwargs: Optional[dict] = None,
        llm_chain_kwargs: Optional[dict] = None,
) -> Chain:
    chat_model = ChatOpenAI(openai_api_key=openai_api_key or config.openai_api_key, openai_proxy=config.proxy, **chat_model_kwargs or {})
    template = system
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    chain = LLMChain(llm=chat_model, prompt=chat_prompt, **llm_chain_kwargs or {})
    return chain
