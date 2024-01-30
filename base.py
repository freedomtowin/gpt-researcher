import time
from researcher.config import Config
from researcher.functions import *

import researcher.api as api 
from researcher.api.context import Context

from langchain.vectorstores import FAISS
import pdb
import os

environ = os.getenv("environ", 'prd')

if environ == 'prd':
    import researcher.secrets_manager as secrets_manager
    openai_api_key = secrets_manager.get_secret("/amplify/d22dk4zcipyt2f/main/openai_api_key")
    openai_api_key = json.loads(openai_api_key)['openai_api_key']
    os.environ['openai_api_key'] = openai_api_key

    tavily_api_key = secrets_manager.get_secret("/amplify/d22dk4zcipyt2f/main/tavily_api_key")
    tavily_api_key = json.loads(tavily_api_key)['tavily_api_key']
    os.environ['tavily_api_key'] = tavily_api_key


class Researcher:
    """
    Researcher
    """
    def __init__(self, store, query, report_type="research_report", source_urls = [], config_path=None, websocket=None):
        """
        Initialize the Researcher class.
        Args:
            query:
            report_type:
            config_path:
            websocket:
        """
        self.store = store
        self.query = query
        self.agent = None
        self.role = None
        self.report_type = report_type
        self.websocket = websocket
        self.cfg = Config(config_path)
        self.context = []
        
        self.api_context = Context(query = query, urls = source_urls, cfg_path = config_path, websocket = websocket)

    async def run(self):
        """
        Runs the Researcher
        Returns:
            Report
        """
        print(f"🔎 Running research for '{self.query}'...")
        # Generate Agent
        self.agent, self.role = await self.api_context.choose_agent()
        await self.api_context.stream_output("logs", self.agent, self.websocket)

        # If specified, the researcher will use the given urls as the context for the research.


        self.aisle_context = await self.api_context.get_aisle_category_context(self.store)

        self.context = await self.api_context.get_context()

        # Write Research Report
        if self.report_type == "custom_report":
            self.role = self.cfg.agent_role if self.cfg.agent_role else self.role
        
        await self.api_context.stream_output("logs", f"✍️ Writing {self.report_type} for research task: {self.query}...", self.websocket)

        report = await self.api_context.generate_aisle_categories(
                                       store = self.aisle_context,
                                       query = self.query,
                                       context = self.context,
                                       agent_role_prompt = self.role,
                                       report_type = self.report_type,
                                       websocket = self.websocket,
                                       cfg = self.cfg)
        time.sleep(2)
        return report




