import os, sys, time, pdb

os.environ['SERPER_API_KEY'] = '8097262ac2c7440ea4f7a694abf5af7dc40cf05e'
os.environ['VALUE_SERPER_API_KEY'] = 'CD1E74E442294421A0B31F31A5E39B5B'
os.environ["BING_SUBSCRIPTION_KEY"] = "6080aec710e44c939b8c833fcc15a451"
os.environ["BING_SEARCH_URL"] = "https://api.bing.microsoft.com/v7.0/search"
os.environ['USER_FILE'] = '/workspace/molecule/config.yml'

os.environ['IGNORE_WARNINGS'] = '0'
sys.path.insert(0, os.path.abspath('..'))

search_terms = [
    'Controversies or Investor concerns', 'Environment concerns',
    'Regulatory concerns', 'Social concerns'
]
name = 'Microsoft'
code = 'MSFT.OQ'

from portageur.plugins.serper.delayed.search import AsyncSearch

async_search = AsyncSearch()

s = time.perf_counter()
search_terms = [f'{name} {search_term}' for search_term in search_terms]
controversy_dict, citationmap_dict = async_search.run_urls_long_json(
    search_terms)
elapsed = time.perf_counter() - s
pdb.set_trace()
print("\033[1m" + f"Concurrent executed in {elapsed:0.2f} seconds." +
      "\033[0m")
