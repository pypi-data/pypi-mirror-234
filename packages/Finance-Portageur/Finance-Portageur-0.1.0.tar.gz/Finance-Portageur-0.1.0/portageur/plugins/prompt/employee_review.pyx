# -*- coding: utf-8 -*
import pdb
import re

from langchain import PromptTemplate

from portageur.kdutils.division.lazy import LazyFunc
from portageur.plugins.prompt.base import transformer, PromptsMessage

class EmployeeReview(object):

    @classmethod
    def research(cls, company):
        return company.emplyee_review

    @classmethod
    def single_doc(cls, topic=None):
        if not topic:
            prompt_template = """Summarize what employees are saying about the company in the list of reviews delimited by triple quotes.
                            Respond in about 200 words in concise and professional tone in markdown text.
                            Please highlight item headers and important phrases in bold.
                            Please organize your response by the pros, cons, and advice separately.

                            Reviews:```{text}```

                            CONCISE SUMMARY:"""
        else:
            prompt_template = f"""Summarize what employees are saying about the company on the topic {topic} in the list of reviews delimited by triple quotes.""" + \
                              """Respond in about 200 words in concise and professional tone in markdown text.
                              Please highlight item headers and important phrases in bold.
                              Please organize your response by the compliments, criticism, and advice separately.
                              Please only focus on the reviews that are relevant to the topic.
                              Please respond with "No relevant reviews found." if there are no relevant reviews.

                              Reviews:```{text}```

                              CONCISE SUMMARY:"""
        return PromptTemplate(template=prompt_template, input_variables=["text"])

    @classmethod
    def multi_doc_map(cls):
        map_prompt_template = """Summarize what employees are saying about the company in the list of reviews delimited by triple quotes.
                        Respond in about 200 words in concise and professional tone.
                        Please highlight item headers and important phrases in bold.
                        Please organize your response by the pros, cons, and advice separately.

                        Reviews:```{text}```

                        SUMMARY:"""
        return PromptTemplate(template=map_prompt_template, input_variables=["text"])

    @classmethod
    def multi_doc_reduce(cls):
        reduce_prompt_template = """Aggregate what employees are saying about the company in the text delimited by triple quotes.
                        Respond in about 200 words in concise and professional tone in markdown text.
                        Present your findings in bullet points.
                        Please organize your response by the pros, cons, and advice separately.

                        Reviews:```{text}```

                        SUMMARY:"""
        return PromptTemplate(template=reduce_prompt_template, input_variables=["text"])
