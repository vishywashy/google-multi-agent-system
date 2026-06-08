# Workspace Multi Agent system

## What is this system❓

- This is a system that contains a gmail agent and a google calendar agent. These agents are built on **langgraph** and is routed by a pytorch router. 
- The neural networks I used are piecewise linear neural network which means that that the negative values in the data are turned to 0. This was done with the ReLu activation function.
- This is so that the AI can make decisions and classify the user's query to the right agent. I also used an LLM before the user's prompt to ensure that the pytorch router is able to route correctly without any "noise" getting in the way.

## 🧠 System Architecture
- The user types a prompt. An LLM takes that prompt and simplifies it to its direct intent. 
- The pytorch router then takes that direct intent and I use an if else statement after that based on the **pytorch router's** response. 
- It routes the task to the appropriate agent and that agent does that task. 
- The reason I used a pytorch router rather than a standard LLM is because of the drawbacks. 
- While LLM's are good at making decisions they tend to loop a lot especially when the architecture of a system gets complex. 
- A pytorch router is fast efficient and when paired with an LLM I don't get a looping problem because I have more control over the data I feed into it making the system more efficient if I were not to use it.

## 🛠 Tech Stack
- For this project I used **ollama's llama3.2** which is a local model. 
- With this model I built langgraph agents using **langgraph_ollama**. 
- As for the pytorch router I used sklearn only to preprocess the data to transform it into tensors and providing it the appropriate format before feeding it into the model. I also built my own data generation pipeline which generated data for my model with AI. 
- I was generating 1000 pieces of data. This data took hours to generate as I had to ensure that the data getting fed to my AI was suitable for the task.



## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com) installed and running.
- Google Cloud Console Project with Calendar/Gmail APIs enabled.
- Everything specified in **requirements.txt** installed. To do this you go into the project and run
```bash
pip install -r requirements.txt
```


### Installation
1.**Clone the repository:**
   ```bash
    git clone https://github.com/vishywashy/Workspace-Multi-agent-system
    cd Workspace-Multi-agent-system

```
- These lines of code will get you into the repo. You have to also replace the .env with your secrets to run the code

# Inside your .env you add:
```env
GoogleCreds="YOUR GOOGLE CREDENTIALS HERE"
DiscordBot="YOUR DISCORD BOT CREDENTIALS HERE"
```
