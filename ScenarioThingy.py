import torch
import joblib
from transformers import AutoTokenizer
import ollama
from Training import BCNet # 1. Import your class
async def Runner(prompt):
    Result = []
    mlb = joblib.load("processor.joblib")
# 2. Setup the "Brain" (.pth)
# Must match your training: 5 inputs, 5 outputs
    model = BCNet(len(mlb.classes_)) 
    model.load_state_dict(torch.load("agent_model.pth"))
    model.eval() # Set to 'Prediction Mode'
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
# 3. Setup the "Translator" (.bin)
    scalar = joblib.load("scaler.joblib")
    my_task_tokens = ollama.generate(model = "llama3.2", prompt = f"Is {prompt} an EMAIL or CALENDAR TASK?ANSWER STRAIGHT TO THE POINT AND DON'T INFERENCE ANYTHING!!!", system ="You are my AI Differentiator designed to differentiate whether the user's prompt fits into the EMAIL category - Sending emails etc or CALENDAR TASK category - Events etc AND CAN ONLY SAY EMAIL OR CALENDAR TASK")

    print(my_task_tokens["response"])
    my_task_tokens = tokenizer.encode(my_task_tokens["response"])
# 4. YOUR SCENARIO (The np.array)
# Format: [Urgency, Complexity, Security, Budget, Hours]
    task_binary = mlb.transform([my_task_tokens])

# 5. THE PROCESS
# Scale it first!
    task_scaled = scalar.transform(task_binary)
# Convert to Tensor
    task_tensor = torch.from_numpy(task_scaled).float()

# 6. THE PREDICTION
    with torch.no_grad():
        output = model(task_tensor)
        winner_id = torch.argmax(output, dim=1).item()

    target_names = ["Gmail Agent", "Google Calendar Agent"]
    if target_names[winner_id] == "Gmail Agent":
        from GmailAgent import Run
        final_resp = await Run({"messages":["user", prompt]})
        print("Gmail Agent")
        return final_resp
            
    elif target_names[winner_id] == "Google Calendar Agent":
        from GoogleCalendarAgent import Run
        final_resp = await Run({"messages":["user", prompt]})
        print("Google Calendar Agent")
        return final_resp
     
