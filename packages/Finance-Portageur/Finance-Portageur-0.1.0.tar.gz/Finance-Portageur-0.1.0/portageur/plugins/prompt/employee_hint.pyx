# -*- coding: utf-8 -*

import pdb
from portageur.kdutils.division.lazy import LazyFunc
from portageur.plugins.prompt.base import transformer, PromptsMessage

class EmployeesHint(object):

    @classmethod
    def reduce_reviews(cls):
        query = """Aggregate what employees are saying about the company in the text delimited by triple quotes.
                Respond in about 200 words in concise and professional tone in markdown text.
                Present your findings in bullet points.
                Please organize your response by the pros, cons, and advice separately.

                Reviews:```{text}```

                SUMMARY:"""
        return transformer(query=query, method=PromptsMessage.Template, variables=["text"])

    @classmethod
    def map_reviews(cls):
        query = """Summarize what employees are saying about the company in the list of reviews delimited by triple quotes.
                Respond in about 200 words in concise and professional tone.
                Please highlight item headers and important phrases in bold.
                Please organize your response by the pros, cons, and advice separately.

                Reviews:```{text}```

                SUMMARY:"""
        return transformer(query=query, method=PromptsMessage.Template, variables=["text"])

    @classmethod
    def universal_reviews(cls):
        query = """Summarize what employees are saying about the company in the list of reviews delimited by triple quotes.
                            Respond in about 200 words in concise and professional tone in markdown text.
                            Please highlight item headers and important phrases in bold.
                            Please organize your response by the pros, cons, and advice separately.
    
                            Reviews:```{text}```
    
                            CONCISE SUMMARY:"""
        return transformer(query=query, method=PromptsMessage.Template, variables=["text"])
    
    @classmethod
    def topic_reviews(cls, topic):
        query = f"""Summarize what employees are saying about the company on the topic {topic} in the list of reviews delimited by triple quotes.""" +\
                                 """Respond in about 200 words in concise and professional tone in markdown text.
                                 Please highlight item headers and important phrases in bold.
                                 Please organize your response by the compliments, criticism, and advice separately.
                                 Please only focus on the reviews that are relevant to the topic.
                                 Please respond with "No relevant reviews found." if there are no relevant reviews.

                                 Reviews:```{text}```

                                 CONCISE SUMMARY:"""
        return transformer(query=query, method=PromptsMessage.Template, variables=["text"])