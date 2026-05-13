from state.user_profile import UserProfile
from state.conversation_state import ConversationState
from dialogs.data_collection import DataCollectionDialog

from microsoft_agents.hosting.core import (
   AgentApplication,
   TurnState,
   TurnContext,
   MemoryStorage,
)

class MainRouter:

    def __init__(self):
        self.data_collection = DataCollectionDialog()

    async def main_route(self, context: TurnContext, turn_state: TurnState):

        # Load or create state
        #user_state = turn_state.user_state.get(UserProfile) or UserProfile()
        #convo_state = turn_state.conversation_state.get(ConversationState) or ConversationState()
        
        user_state = turn_state.user.get(UserProfile)
        convo_state = turn_state.conversation.get(ConversationState)
        convo_state
        

        text = context.activity.text.strip().lower()
        
        
        await context.send_activity(f"you said: {text }")

        # If a dialog is active → continue it
        if convo_state.step:
            await self.data_collection.run(context, text, user_state, convo_state)

        # Otherwise → start a new dialog
        else:
            if "data collection" in text or text == "1":
                convo_state.step = "ask_company"
                await context.send_activity("Let's begin. What is your company name?")
            else:
                await context.send_activity(
                    "Choose an option:\n"
                    "1. Data Collection\n"
                    "(Only Data Collection is implemented for now)"
                )

        # Save state
        turn_state.user.set_value(user_state)
        turn_state.conversation.set_value(convo_state)
        #turn_state.user_state.set(user_state)
        #turn_state.conversation_state.set(convo_state)
