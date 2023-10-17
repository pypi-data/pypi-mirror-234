import pdb
import pandas as pd
from pydantic.main import BaseModel
from langchain.schema import Document
from langchain.chains.summarize import load_summarize_chain
#from langchain.chat_models import AzureChatOpenAI
from portageur.plugins.auth.azure import AzureChatOpenAI
from portageur.plugins.prompt.employee_hint import EmployeesHint
from portageur.plugins.splitter.seleya_text_splitter import SeleyaTextSplitter
from portageur.plugins.loader.employee import Empolyee as LoaderEmpolyee
from portageur.kdutils.logger import kd_logger


class Immediate(BaseModel):

    def splitter(self, data, document_len_limit):
        review_str = data['text'].dropna().tolist()
        text_splitter = SeleyaTextSplitter(chunk_size=document_len_limit,
                                           encoding_name='cl100k_base')
        review_docs = text_splitter.split_text(review_str)
        review_docs = [Document(page_content=t) for t in review_docs]
        return review_docs

    def summarize_single_docs(self, docs, llm_advanced, topic=None):
        prompt = EmployeesHint.universal_reviews(
        ) if not topic else EmployeesHint.topic_reviews(topic=topic)
        sum_chain = load_summarize_chain(llm_advanced,
                                         chain_type="stuff",
                                         prompt=prompt)
        return sum_chain.run(docs)

    def summarize_multi_docs(self, docs, llm, llm_advanced):
        map_prompt = EmployeesHint.map_reviews()
        reduce_prompt = EmployeesHint.reduce_reviews()
        sum_chain = load_summarize_chain(llm,
                                         chain_type="map_reduce",
                                         map_prompt=map_prompt,
                                         combine_prompt=reduce_prompt,
                                         reduce_llm=llm_advanced)
        return sum_chain.run(docs)

    def run(self, code, document_len_limit=2000, review_num=1500, topic=None):
        loader_emplyee = LoaderEmpolyee()
        llm_advanced = AzureChatOpenAI(temperature=0,
                                       max_tokens=800,
                                       deployment_name="gpt-4",
                                       model_name="gpt-4",
                                       request_timeout=60,
                                       max_retries=4)
        llm = AzureChatOpenAI(temperature=0,
                              max_tokens=500,
                              deployment_name="gpt-35-turbo",
                              model_name="gpt-35-turbo",
                              request_timeout=40,
                              max_retries=2)

        kd_logger.info("{0}  load ES reviews".format(code))
        review_df = loader_emplyee.fetch_es_reviews(code=code,
                                                    review_num=review_num,
                                                    topic=topic)

        if len(review_df) == 0:
            return "Sorry, we can't find relevant reviews for the company at the moment."

        kd_logger.info("{0} splitter reviews".format(code))
        review_docs = self.splitter(data=review_df,
                                    document_len_limit=document_len_limit)

        # if it's topic research, we only summarize the latest doc
        if topic:
            review_docs = review_docs[:1]

        kd_logger.info("{0} summarize docs".format(code))

        reviews = self.summarize_single_docs(
            docs=review_docs,
            llm_advanced=llm_advanced.instance(),
            topic=topic) if len(
                review_docs) == 1 else self.summarize_multi_docs(
                    docs=review_docs,
                    llm=llm.instance(),
                    llm_advanced=llm_advanced.instance())
        return reviews
