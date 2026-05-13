# app.py
from microsoft_agents.hosting.core import (
   AgentApplication,
   TurnState,
   TurnContext,
   MemoryStorage,
   ConversationState
)
from microsoft_agents.hosting.aiohttp import CloudAdapter
from microsoft_agents.hosting.aiohttp.jwt_authorization_middleware import AgentAuthConfiguration


from start_server import start_server

storage = MemoryStorage()
auth_config = AgentAuthConfiguration(anonymous_allowed=True) 

# ---------- Session Memory Model ----------
class SessionMemory:
    def __init__(self):
        self.messages = []


# ---------- Storage + State ----------
storage = MemoryStorage()
conversation_state = ConversationState(storage)


AGENT_APP = AgentApplication[TurnState](
    storage=storage, adapter=CloudAdapter()
)

conversation_history_accessor = conversation_state.create_property("conversationHistory")



# Create a state property for your session memory
#session_data = conversation_state.create_property("sessionData")

async def _help(context: TurnContext, _: TurnState):
    await context.send_activity(
        "Welcome to the Echo Agent sample 🚀. "
        "Type /help for help or send a message to see the echo feature in action."
    )





AGENT_APP.conversation_update("membersAdded")(_help)

AGENT_APP.message("/help")(_help)


@AGENT_APP.activity("message")
async def on_message(context: TurnContext, state: TurnState):
    
    # Load existing session memory (or create empty list)
    history = await conversation_history_accessor.get(context, default_value_or_factory=list)

    # Add the user's message
    history.append({
        "role": "user",
        "text": context.activity.text
    })
    
    
    # Generate bot response
    bot_reply = f"I remember {len(history)} messages so far. You said: {context.activity.text}"

    # Add bot response to memory
    history.append({
        "role": "assistant",
        "text": bot_reply
    })

    # Save updated memory
    await conversation_history_accessor.set(context, history)

    # Send bot reply
    await context.send_activity(bot_reply)

    # Persist state
    await conversation_state.save(context)
    

    
    
    
    
if __name__ == "__main__":
    try:
        start_server(AGENT_APP, auth_config )
    except Exception as error:
        raise error