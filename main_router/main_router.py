from microsoft_agents.hosting.core import (
   AgentApplication,
   TurnState,
   TurnContext,
   MemoryStorage,
   ConversationState
)
from microsoft_agents.hosting.aiohttp import CloudAdapter
from microsoft_agents.hosting.aiohttp.jwt_authorization_middleware import AgentAuthConfiguration

from state.analyse_state import AnalyseState
from state.user_profile import UserProfile


class MainRouter:
    def __init__(self):
        self.storage = MemoryStorage()
        self.auth_config = AgentAuthConfiguration(anonymous_allowed=True) 
        self.conversation_state = ConversationState(self.storage)
        self.AGENT_APP = AgentApplication[TurnState](
            storage=self.storage, adapter=CloudAdapter()
        )
        
        self._conversation_history_accessor = self.conversation_state.create_property("conversationHistory")
        self._analyse_preference = self.conversation_state.create_property("analysePreference")
        self.user_preferences = self.conversation_state.create_property("userPreferences")
        self.setup_routes()

        
    
    async def _help(self, context: TurnContext, _: TurnState):
        await context.send_activity(
            "Welcome to the Research Agent sample 🚀. "
            "Let us know the company, topic and timeframe you want to research on. For example, you can say 'I want to research about Microsoft in the last 5 years'."
        )
        # 1: fullfiel user preferences. Ask for missing preferences: companic, topic, timeframe. If all preferences are fulfilled, move to next step.
        # 2: full fiel analyse user preferences for analysis: trend, impressions grouwth, engagement growth, comparaison with other copetitors, or bench for the same period last year
        # 3: build reporting
        



    def setup_routes(self):
        self.AGENT_APP.conversation_update("membersAdded")(self._help)
        self.AGENT_APP.message("/help")(self._help)
        self.AGENT_APP.activity("message")(self._on_message)
        
    async def send_message(self, context: TurnContext, message: str):
        
        history = await self._conversation_history_accessor.get(context, default_value_or_factory=list)

        # Add the user's message
        history.append({
            "role": "agent",
            "text": message
        })
        
        # Save updated memory
        await  self._conversation_history_accessor.set(context, history)
        
        # Send bot reply
        await context.send_activity(message)

        # Persist state
        await self.conversation_state.save(context)
        
    async def _on_message(self, context: TurnContext, state: TurnState):
        # Load existing session memory (or create empty list)
        
        user_state = await self.user_preferences.get(context, default_value_or_factory=UserProfile)
        analyse_state = await self._analyse_preference.get(context, default_value_or_factory=AnalyseState)
        
        input_text = context.activity.text.strip().lower()
        if "BotTask: Data Collection".strip().lower() in input_text:
            print("Data Collection Task identified.")
            await self.send_message(context, "Great! Let's start with data collection. Please provide the company name, topic, and timeframe you want to research on.")
            
        if("BotTask: Data Analysis".strip().lower() in input_text):
            print("Data Analysis Task identified.")
            await self.send_message(context, "Data Analysis Task identified.")
        if("BotTask: Reporting".strip().lower() in input_text):
            print("Reporting Task identified.")
            await self.send_message(context, "Reporting Task identified.")
            
    def get_agent_app(self) -> AgentApplication:
        return self.AGENT_APP
        
       
        
    
