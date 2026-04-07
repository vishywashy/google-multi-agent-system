from GoogleAPI import convert_to_RFC_datetime, create_service
from datetime import datetime, timezone
from datetime import timedelta
from ReactTools import *
from dotenv import load_dotenv
import os
load_dotenv()
client_secret_file = os.environ.get("GoogleCreds")
api_name = "calendar"
api_version = "v3"
scope = ["https://www.googleapis.com/auth/calendar"]
calendar_service = create_service(client_secret_file, api_name, api_version, scope)

class AgentState(TypedDict):
    messages:Annotated[Sequence[BaseMessage], add_messages]
    response_getter:str



@tool
def Create_Event(subject:str, year:int, month:int, day:int, hour:int, minute:int, time_of_event:int):
    """Subject is the front of the event.
       Year:What year is the event booked?
       month:1-12
       day:1-how many days in the month
       hour:0-23
       minute:0-59
       time_of_event:How long event lasts in minutes
       Fill in these details based on the information the user provides."""
    start_dt = datetime(year, month, day, hour, minute)
    end_dt = start_dt+timedelta(minutes=time_of_event)
    end_year   = end_dt.year
    end_month  = end_dt.month
    end_day    = end_dt.day
    end_hour   = end_dt.hour
    end_minute = end_dt.minute
    event_request_body = {
  "summary":subject,
  "start": {
    "dateTime":convert_to_RFC_datetime(year, month, day, hour, minute),
    "timeZone": "Europe/London"
  },
  "end": {
    "dateTime":convert_to_RFC_datetime(end_year, end_month, end_day, end_hour, end_minute),
    "timeZone": "Europe/London",
   
  }
}
    response = calendar_service.events().insert(
    calendarId=""primary"",        # Use 'primary' or the specific calendar ID
    body=event_request_body,     # The dictionary containing event details,           # Options: 'all', 'externalOnly', or 'none'     # Set to 1 if you are generating Google Meet links
    maxAttendees=None,           # Integer: Maximum number of attendees to include
    supportsAttachments=False,
).execute()
    return "Calendar has been created"


@tool
def Event_Deleter(name_of_event):
    """Deletes events by name"""
    events_result = calendar_service.events().list(calendarId='primary', q=name_of_event).execute()
    events = events_result.get('items', [])
    for event in events:
        if event.get("summary") == name_of_event:
            calendar_service.events().delete(calendarId='primary', eventId=event['id']).execute()
    return "Event has been deleted"


@tool
def ViewEvent():
    """Views events"""
    total_events = []
    now = datetime.now(timezone.utc)
    year = now.year             # e.g., 2024
    month = now.month           # e.g., 5
    day = now.day               # e.g., 22
    day_new =now+timedelta(days=1)
    day_new_now = day_new.day
    year_new = day_new.year
    month_new = day_new.month
    events_result = calendar_service.events().list(
        calendarId='primary',
        timeMin=convert_to_RFC_datetime(year=year, month=month, day=day, hour = 0, minute=0),
        timeMax=convert_to_RFC_datetime(year=year_new, month=month_new, day = day_new_now, hour = 0, minute=0),
    singleEvents=True,
    orderBy='startTime'
).execute()

    events = events_result.get('items', [])

# Output results
    if not events:
       return 'No events found for today.'
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        total_events.append(f"Events:{event.get('summary', 'No Title')}")
    print(f"Here are the events:{total_events}")
    return f"Here are the events:{total_events}"

full_response = ""
tools = [Create_Event, Event_Deleter, ViewEvent]
llm = ChatOllama(model="llama3.2")
model = llm.bind_tools(tools=tools)
async def Agent(state:AgentState):
      sys_prompt = SystemMessage("""You are my AI Assistant designed to operate on the user's calendar.
                                 PLEASE FOLLOW THE DOCSTRING WITH CARE and follow the user's queries to the best of your ability and
                                 your job is to fill out key details (if necessary) and understand the user's needs. For the events please state what's in the list.""")
      all_messages = [sys_prompt]+list(state["messages"])
      response = await model.ainvoke(all_messages)
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

    #print(f"{response_text}")
    print(f"Done")
    
    return response_text







