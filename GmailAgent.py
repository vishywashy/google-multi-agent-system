from ReactTools import *
from GoogleAPI import create_service
from EmailFormatter import create_message
import os
from dotenv import load_dotenv
load_dotenv()
client_secret_file = os.environ.get("GoogleCreds")
api_name = "gmail"
api_version = "v1"
scope = ["https://mail.google.com/"]
service = create_service(client_secret_file, api_name, api_version, scope)


class AgentState(TypedDict):
    messages:Annotated[Sequence[BaseMessage], add_messages]
    response_getter:str





@tool
def Send_message(to:str, subject:str, message_text:str):
    """
    Sends an email message to a specified recipient.
    All of the parameters are strings.

    Args:
        to: The email address of the recipient (e.g., 'user@example.com').
        subject: The brief title or subject line of the email.
        message_text: The full body content of the email."""
    email = service.users().getProfile(userId='me').execute()['emailAddress']
    message = create_message(email, to, subject, message_text)
    try:
        sent_message = service.users().messages().send(userId="me", body=message).execute()
        return "Message has been sent"
    except Exception as e:
        return 
        
    
@tool
def View_Emails():
      """Views first 5 emails of gmail inbox"""
      message_list = []
      results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=5).execute()
      messages = results.get('messages', [])
      try:
        for m, item in enumerate(messages):
            msg = service.users().messages().get(userId='me', id=item['id']).execute()
            clean_snippet = msg['snippet'].encode('ascii', 'ignore').decode('ascii')
            formatted_message = f"{clean_snippet}"
            message_list.append(formatted_message)
        return "Here are the emails from the users inbox. Please format to the user"+"\n".join(message_list)
      except Exception as e:
          return e

tools = [Send_message, View_Emails]

llm = ChatOllama(model = "llama3.2", temperature=0)
model = llm.bind_tools(tools = tools)
async def Agent(state:AgentState):
    sys_prompt = SystemMessage("""You are my AI Assistant designed to operate on the user's emails. Please 
                               complete the user's task to the best of your ability by using the available tools. Make sure you follow their docstring carefully.
                               STOP WRITING IN JSON FORMAT AS WELL.""")
    all_messages = [sys_prompt]+list(state["messages"])
    response = await model.ainvoke(all_messages)
    response.content = response.content.split("%")[-1]
    return {"messages":[response], "response_getter":f"{response.content}%"}

def Looper(state:AgentState):
    message = state["messages"][-1]
    if message.tool_calls:
        return "continue"
    else:
        return "exit"
    
graph = StateGraph(AgentState)
graph.add_node("Agent", Agent)
graph.add_node("Tool", ToolNode(tools=tools))
graph.add_conditional_edges(
    "Agent",
    Looper,
    {"continue": "Tool", "exit": END},

)
graph.set_entry_point("Agent")
graph.add_edge("Tool", "Agent")
app = graph.compile()
           

             


async def Run(inputs):
    final_state = None
    
    # "values" mode gives you the full state dictionary after each node finishes
    async for chunk in app.astream(inputs, stream_mode="values"):
        final_state = chunk  # Keep overwriting until the last node finishes

    # Now you have everything in one object
    messages = final_state.get("messages", [])#extracts the text from chunk
    response_text = final_state.get("response_getter", "")#extracts text from chunk defined in agent 

    print(f"{response_text}")
    #print(f"Done")
    
    return response_text
   






       






