from portageur.plugins.serper.bing import Bing as SerperBing


def serper_bing(query,
                total_token_limit=6050,
                article_cutoff=2500,
                citation_start=1,
                method='urls_long_json',
                **kwargs):
    if method == 'urls_long_json':
        return SerperBing().run_urls_long_json(
            query=query,
            total_token_limit=total_token_limit,
            article_cutoff=article_cutoff,
            citation_start=citation_start,
            **kwargs)