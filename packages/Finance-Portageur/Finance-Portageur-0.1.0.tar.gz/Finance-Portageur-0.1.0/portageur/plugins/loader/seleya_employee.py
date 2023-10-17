import logging
from typing import Dict, Optional

import tiktoken
from langchain import PromptTemplate
from langchain.base_language import BaseLanguageModel
from langchain.chains.summarize import load_summarize_chain
from langchain.schema import Document
from langchain.utils import get_from_dict_or_env
from pydantic.class_validators import root_validator
from pydantic.main import BaseModel
from seleya import *

from portageur.plugins.prompt.employee_review import EmployeeReview
from portageur.plugins.splitter.seleya_text_splitter import SeleyaTextSplitter


class SeleyaEmployeeReviews(BaseModel):
    llm: BaseLanguageModel = None
    llm_advanced: BaseLanguageModel = None

    def _num_tokens_from_string(self, string, encoding_name='cl100k_base'):
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def summarize_single_doc(self, docs, topic=None):
        prompt_to_use = EmployeeReview.single_doc(topic=topic)
        sum_chain = load_summarize_chain(self.llm_advanced, chain_type="stuff",
                                         prompt=prompt_to_use)
        return sum_chain.run(docs)

    async def asummarize_single_doc(self, docs, topic=None):
        prompt_to_use = EmployeeReview.single_doc(topic=topic)
        sum_chain = load_summarize_chain(self.llm_advanced, chain_type="stuff",
                                         prompt=prompt_to_use)
        return await sum_chain.arun(docs)

    def summarize_multi_docs(self, docs):
        sum_chain = load_summarize_chain(self.llm, chain_type="map_reduce",
                                         map_prompt=EmployeeReview.multi_doc_map(),
                                         combine_prompt=EmployeeReview.multi_doc_reduce(),
                                         reduce_llm=self.llm_advanced)
        return sum_chain.run(docs)

    async def asummarize_multi_docs(self, docs):
        sum_chain = load_summarize_chain(self.llm, chain_type="map_reduce",
                                         map_prompt=EmployeeReview.multi_doc_map(),
                                         combine_prompt=EmployeeReview.multi_doc_reduce(),
                                         reduce_llm=self.llm_advanced)
        return await sum_chain.arun(docs)

    def _parse_reviews(self, review_df, document_len_limit):
        pros = review_df['pros'].dropna().tolist()
        cons = review_df['cons'].dropna().tolist()
        advice = review_df['advice'].dropna().tolist()
        text_splitter = SeleyaTextSplitter(chunk_size=document_len_limit, encoding_name='cl100k_base')
        pro_docs = text_splitter.split_text(pros)
        pro_docs = [Document(page_content=t) for t in pro_docs]
        con_docs = text_splitter.split_text(cons)
        con_docs = [Document(page_content=t) for t in con_docs]
        advice_docs = text_splitter.split_text(advice)
        advice_docs = [Document(page_content=t) for t in advice_docs]
        return pro_docs, con_docs, advice_docs

    def _parse_reviews_flat(self, review_df, document_len_limit):
        review_df['summary'] = review_df['summary'].apply(lambda x: f"{x} " if isinstance(x, str) else " ")
        review_df['pros'] = review_df['pros'].apply(lambda x: f"{x} " if isinstance(x, str) else " ")
        review_df['cons'] = review_df['cons'].apply(lambda x: f"{x} " if isinstance(x, str) else " ")
        review_df['advice'] = review_df['advice'].apply(lambda x: f"{x}" if isinstance(x, str) else " ")
        review_df['text'] = review_df['summary'] + review_df['pros'] + review_df['cons'] + review_df['advice']
        review_str = review_df['text'].dropna().tolist()
        text_splitter = SeleyaTextSplitter(chunk_size=document_len_limit, encoding_name='cl100k_base')
        review_docs = text_splitter.split_text(review_str)
        review_docs = [Document(page_content=t) for t in review_docs]
        return review_docs

    def _query_reviews(self, company_code, document_len_limit, review_num, query='') -> str:
        try:
            review_df = SeleyaAPI.search_gd_reviews(query=query, codes=[company_code], pos=0, count=review_num)
            if len(review_df) == 0:
                return 'We do not cover employee reviews for this company.'
            return self._parse_reviews_flat(review_df, document_len_limit)
        except Exception as e:
            logging.info(e)
            return 'We do not cover employee reviews for this company.'

    def run(self, company_code, document_len_limit=2000, review_num=2500) -> str:
        """Run employee review pulling and summarization."""
        review_docs = self._query_reviews(company_code, document_len_limit, review_num)

        if len(review_docs) == 1:
            reviews = self.summarize_single_doc(review_docs)
        else:
            reviews = self.summarize_multi_docs(review_docs)

        return reviews

    async def arun(self, company_code, document_len_limit=2000, review_num=2500) -> str:
        """Run employee review pulling."""
        # logging.info(f"pulling employee reviews for {company_code}")
        review_docs = self._query_reviews(document_len_limit, review_num)
        # logging.info(f"pulled employee reviews for {company_code}")

        if len(review_docs) == 1:
            reviews = await self.asummarize_single_doc(review_docs)
        else:
            reviews = await self.asummarize_multi_docs(review_docs)
        # logging.info(f"Got reviews for {company_code}")

        return reviews

    def run_topic(self, company_code, query, document_len_limit=3000) -> str:
        """run employee reviews with ES results on a single topic"""
        reviews = self._query_reviews(company_code, document_len_limit, review_num=200, query=query)
        return self.summarize_single_doc(reviews, topic=query)

    async def arun_topic(self, company_code, query, document_len_limit=3000) -> str:
        """run employee reviews with ES results on a single topic"""
        reviews = self._query_reviews(company_code, document_len_limit, review_num=200, query=query)
        result = await self.asummarize_single_doc(reviews, topic=query)
        return result
