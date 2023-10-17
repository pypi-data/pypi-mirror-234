"""Util that calls Bing Custom Search.
"""
from typing import Dict, List

import requests
from pydantic import BaseModel, Extra, root_validator

from langchain.utils import get_from_dict_or_env


class BingCustomSearchAPIWrapper(BaseModel):
    """Wrapper for Bing Custom, Search API.
    """

    bing_subscription_key_custom: str
    bing_search_url_custom: str
    bing_config_id_custom: str
    k: int = 15

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    def _bing_search_results(self, search_term: str, count: int) -> List[dict]:
        headers = {"Ocp-Apim-Subscription-Key": self.bing_subscription_key_custom}
        params = {
            "q": search_term,
            "customConfig": self.bing_config_id_custom,
            "count": count,
            "mkt": "en-US",
            "safeSearch": 'Off'
        }
        response = requests.get(
            self.bing_search_url_custom, headers=headers, params=params  # type: ignore
        )
        response.raise_for_status()
        search_results = response.json()
        return search_results["webPages"]["value"]

    @root_validator(pre=True)
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and endpoint exists in environment."""
        bing_subscription_key_custom = get_from_dict_or_env(
            values, "bing_subscription_key_custom", "BING_SUBSCRIPTION_KEY_CUSTOM"
        )
        values["bing_subscription_key_custom"] = bing_subscription_key_custom

        bing_search_url_custom = get_from_dict_or_env(
            values,
            "bing_search_url_custom",
            "BING_SEARCH_URL_CUSTOM",
            # default="https://api.bing.microsoft.com/v7.0/search",
        )
        values["bing_search_url_custom"] = bing_search_url_custom

        bing_config_id_custom = get_from_dict_or_env(
            values,
            "bing_config_id_custom",
            "BING_SEARCH_CONFIG_CUSTOM",
        )
        values["bing_config_id_custom"] = bing_config_id_custom

        return values

    def run(self, query: str) -> str:
        """Run query through BingSearch and parse result."""
        snippets = []
        results = self._bing_search_results(query, count=self.k)
        if len(results) == 0:
            return "No good Bing Search Result was found"
        for result in results:
            snippets.append(result["snippet"])

        return " ".join(snippets)

    def results(self, query: str, num_results: int) -> List[Dict]:
        """Run query through BingSearch and return metadata.

        Args:
            query: The query to search for.
            num_results: The number of results to return.

        Returns:
            A list of dictionaries with the following keys:
                snippet - The description of the result.
                title - The title of the result.
                link - The link to the result.
        """
        metadata_results = []
        results = self._bing_search_results(query, count=num_results)
        if len(results) == 0:
            return [{"Result": "No good Bing Search Result was found"}]
        for result in results:
            metadata_result = {
                "snippet": result["snippet"],
                "title": result["name"],
                "link": result["url"],
            }
            metadata_results.append(metadata_result)

        return metadata_results
