import pdb
import pandas as pd
from seleya import SeleyaAPI


class Empolyee(object):

    def fetch_es_reviews(self, code, review_num, topic=None):
        try:
            if not topic:
                review_df = SeleyaAPI.search_gd_reviews(query='',
                                                    codes=[code],
                                                    pos=0,
                                                    count=review_num)
            else:
                review_df = SeleyaAPI.search_gd_reviews(query=topic,
                                                    codes=[code],
                                                    pos=0,
                                                    count=review_num)
        except Exception as e:
            review_df = pd.DataFrame()
        if review_df.empty:
            return review_df

        review_df['summary'] = review_df['summary'].apply(
            lambda x: f"{x} " if isinstance(x, str) else " ")
        review_df['pros'] = review_df['pros'].apply(
            lambda x: f"{x} " if isinstance(x, str) else " ")
        review_df['cons'] = review_df['cons'].apply(
            lambda x: f"{x} " if isinstance(x, str) else " ")
        review_df['advice'] = review_df['advice'].apply(
            lambda x: f"{x}" if isinstance(x, str) else " ")
        review_df['text'] = review_df['summary'] + review_df[
            'pros'] + review_df['cons'] + review_df['advice']
        return review_df