import torch
import joblib
import torch.nn as nn
import ast
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
import pandas as pd
# Load the full dataset object to get target names
target_names = ["Gmail Agent", "Google Calendar Agent"]

outputs = 2
class BCNet(nn.Module):
        def __init__(self, input_dim):
            super(BCNet, self).__init__()
            self.fcl = nn.Linear(input_dim, 512)
            self.fc2 = nn.Linear(512, 256)
            self.fc3 = nn.Linear(256, outputs)
        
        def forward(self, x):
            x = F.relu(self.fcl(x))
            x = F.relu(self.fc2(x))
            return self.fc3(x) 
        

def train_and_decode(X, y):
    #Splits the data into variables scales it and cleans it. and loads to AI.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    scalar = StandardScaler()
    X_train_scaled = scalar.fit_transform(X_train)
    X_test_scaled = scalar.transform(X_test)

    X_train_scaled_tensor = torch.from_numpy(X_train_scaled).float()
    X_test_scaled_tensor = torch.from_numpy(X_test_scaled).float()
    y_train_tensor = torch.from_numpy(y_train).long()
    y_test_tensor = torch.from_numpy(y_test).long()

    train_dataset = TensorDataset(X_train_scaled_tensor, y_train_tensor)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    joblib.dump(scalar, 'scaler.joblib')
   

    model = BCNet(X.shape[1])
    criterion = nn.CrossEntropyLoss()
    optimiser = optim.Adam(model.parameters(), lr=0.001)
    torch.save(model.state_dict(), "agent_model.pth")
    for epoch in range(500):
        model.train()
        for x_batch, y_batch in train_loader:
            optimiser.zero_grad()
            preds = model(x_batch)
            whole_number_preds = torch.argmax(preds, dim=1)
            loss = criterion(preds, y_batch)
            loss.backward()
            optimiser.step()

    # --- DECODING SECTION ---
    with torch.no_grad():
        model.eval()
        raw_preds = model(X_test_scaled_tensor)
        # Converts to whole number
        whole_number_preds = torch.argmax(raw_preds, dim=1)
        
        # Map integers back to text names
        text_preds = [target_names[p] for p in whole_number_preds]
        clean_preds = [str(p) for p in text_preds]
        print(clean_preds)
        print("Testing phase")
        print("First Predictions (Text):", clean_preds)
        
        accuracy = (torch.argmax(raw_preds, dim=1).long() == y_test_tensor.flatten().long()).float().mean().item()
        print(f"Accuracy: {accuracy}")


    return model
np.random.seed(42)
X,y = np.column_stack([
    np.random.randint(1, 11, 100),    # Urgency
    np.random.randint(1, 11, 100),    # Complexity
    np.random.randint(1, 6, 100),     # Security
    np.random.randint(100, 5001, 100),# Budget
    np.random.randint(1, 41, 100)     # Hours
]),np.random.randint(0, 5, 100)

#reads csv
df = pd.read_csv("output.csv")
df['role'] = df['role'].apply(ast.literal_eval)#removes speech mark
y = df['job'].to_numpy()#Tells the AI to find job

processer = MultiLabelBinarizer()#Loads the binarizer
X = processer.fit_transform(df['role'])#Get's the role so AI could learn how to find y and cleans it up
#train_and_decode(X, y)#puts inputs into system
joblib.dump(processer, 'processor.joblib') 

    
  
