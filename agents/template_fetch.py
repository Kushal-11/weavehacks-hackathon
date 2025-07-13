from crewai import Agent
from exa.exa_utils import ExaClient

class TemplateFetchAgent(Agent):
    def __init__(self, exa_api_key: str):
        super().__init__(name="template_fetch")
        self.exa_client = ExaClient(api_key=exa_api_key)

    def fetch_templates(self, query: str, limit: int = 10):
        """
        Use exa.ai to search for meme templates based on a query.
        Returns a list of template URLs or metadata.
        """
        results = self.exa_client.search_templates(query=query, limit=limit)
        return results 