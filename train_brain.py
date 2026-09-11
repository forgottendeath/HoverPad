import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

print("1. Reading your spreadsheet data...")
# Read the CSV we just made
df = pd.read_csv('gesture_data.csv', header=None)

# The first column is the Label (0,1,2,3,4,5). The rest are the 63 coordinates.
X = df.iloc[:, 1:].values
y = df.iloc[:, 0].values

# We hide 20% of the data from the AI to test how smart it actually is!
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("2. Training the Machine Learning Model...")
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Give it a pop quiz on the 20% of data it hasn't seen
accuracy = model.score(X_test, y_test)
print(f"3. Brain Training Complete! AI Accuracy: {accuracy * 100:.2f}%")

print("4. Saving the brain to 'gesture_model.pkl'...")
with open('gesture_model.pkl', 'wb') as f:
    pickle.dump(model, f)
    
print("--- SUCCESS! Ready for Phase 3! ---")