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
class UserInfo:
    def __init__(self, userName: str = "", preferences: dict = None):
        self.userName = userName
        self.preferences = preferences or {}
        
    def updateUserName(self, name: str):
        self.userName = name


# ---------- Storage + State ----------
storage = MemoryStorage()
conversation_state = ConversationState(storage)


AGENT_APP = AgentApplication[TurnState](
    storage=storage, adapter=CloudAdapter()
)

conversation_history_accessor = conversation_state.create_property("conversationHistory")


userInfo_session = conversation_state.create_property("userInfoSession")



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
    
    userInfo = await userInfo_session.get(context, default_value_or_factory=UserInfo)
    
    userInput = context.activity.text

    # Add the user's message
    history.append({
        "role": "user",
        "text": userInput
    })
    
    
    # Generate bot response
    bot_reply = f"I remember {len(history)} messages so far. You said: {userInput}"

    # Add bot response to memory
    history.append({
        "role": "assistant",
        "text": bot_reply
    })

    # Save updated memory
    await conversation_history_accessor.set(context, history)


    # handle bot ouput
    
    if "my name is" in userInput.lower():
        name = userInput.lower().split("my name is")[-1].strip()
        userInfo.updateUserName(name)
        await userInfo_session.set(context, userInfo)
        bot_reply = f"Nice to meet you, {userInfo.userName}!"
    
    if "what is my name" in userInput.lower():
        if userInfo.userName != "":
            bot_reply = f"Your name is {userInfo.userName}."
        else:
            bot_reply = "I don't know your name yet. You can tell me by saying 'My name is ...'."
            
    if "update my name to" in userInput.lower():
        name = userInput.lower().split("update my name to")[-1].strip()
        userInfo.updateUserName(name)
        await userInfo_session.set(context, userInfo)
        bot_reply = f"Your name has been updated to {userInfo.userName}."
        
        
    # Send bot reply
    await context.send_activity(bot_reply)

    # Persist state
    await conversation_state.save(context)
    

    
    
    
    
if __name__ == "__main__":
    try:
        start_server(AGENT_APP, auth_config )
    except Exception as error:
        raise error