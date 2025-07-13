 from crewai import Agent
from exa.exa_utils import get_meme_templates
from weave_logger.logger import log_agent_action

class TemplateAgent(Agent):
    def fetch_templates(self, topic: str):
        images = get_meme_templates(topic)
        log_agent_action("TemplateAgent", f"Fetched {len(images)} templates for '{topic}'")
        return images
