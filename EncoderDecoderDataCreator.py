from transformers import AutoTokenizer
import pandas as pd
import ollama
from random import randint


def encoder(data):
    encoded_list = []
# This task converts text into numerical feature vectors (embeddings)
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    for i in data:
        result = tokenizer.encode(i)
        encoded_list.append(result)

# 'result' is a list containing a large array of numbers
# Let's convert it to a Torch tensor to see its shape
#embeddings = torch.tensor(result)
#print(f"Numerical Shape: {embeddings}")
    tables = {
        "job":[0 for i in range(500)]+[1 for i in range(500)],
        "role":encoded_list
    }
    new_df = pd.DataFrame(tables)
    new_df.to_csv("output.csv")
    return "Data generated"
response_list = []
def DataCreator(prompt):

    for i in range(500):
        response = ollama.generate(model="qwen2.5:1.5b", system="Add some variation.", prompt=f"{prompt} BUT CANNOT CONTAIN THESE WORDS:{response_list[-1] if response_list else "nothing"}",  options={
        'temperature':0.85,       # Slightly lower to keep grammar stable for BERT
    'min_p': 0.05,            # Lower threshold lets more English synonyms through
    'repeat_penalty': 1.1,    # Enough to stop loops without forcing language-hopping
    'presence_penalty': 0.2,  # Subtly nudges new topics without breaking the flow
    'num_predict': 80,
    'stop': ["\n", "."],
    'seed': randint(1, 2147483647)
    })
        print(response["response"]+f"---------------------------------{i+1} of 500")
        response_list.append(response["response"])
        

       

response = DataCreator("Think of words to do with emails specifically reading, writing and sending and viewing emails and draft a sentence out of it. Remove any nouns and just write a sentence MAKE IT EMAIL SPECIFIC.")
responseList = response_list
response_list = []
response2 = DataCreator("Think of words to do with calendars specifically reading, writing, viewing and updating events and draft a sentence out of it. Remove any nouns and just write a sentence MAKE IT CALENDAR SPECIFIC.")
combined_list = responseList+response_list
print(encoder(combined_list))




