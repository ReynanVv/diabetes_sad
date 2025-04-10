import pandas as pd
from sklearn.model_selection import train_test_split
import pickle
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('data/diabetes.csv')
print(df.info())

X = df.drop('Outcome', axis=1)
y = df['Outcome']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train)

with open('models/diabetes_model.pkl', 'wb') as f:
    pickle.dump(model, f)
