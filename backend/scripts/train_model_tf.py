import sys
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Input
import numpy as np

# --- Train model using TensorFlow ---

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

if project_root not in sys.path:
    sys.path.append(project_root)

# Load the data from the CSV file
raw_data_dir = os.path.join(project_root, 'data/raw')
csv_file_path = os.path.join(raw_data_dir, 'tic_tac_toe_games.csv')
data = pd.read_csv(csv_file_path)

# Separate the features (board state) from the labels (best move)
X = data.iloc[:, :9]
y = data.iloc[:, 9:] # Now we take both columns for the label

# Convert the data to numpy arrays, which TensorFlow prefers
X = X.to_numpy()
y = y.to_numpy()

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Training data size: {len(X_train)} samples")
print(f"Testing data size: {len(X_test)} samples")

# --- Define the Keras model ---
# This is a simple feed-forward neural network
input_layer = Input(shape=(9,)) # The input is our 9-element board vector
hidden_layer_1 = Dense(64, activation='relu')(input_layer) # First hidden layer with 64 neurons
hidden_layer_2 = Dense(32, activation='relu')(hidden_layer_1) # Second hidden layer with 32 neurons
output_layer = Dense(2, activation='linear')(hidden_layer_2) # Output layer with 2 neurons (for row and col)

model = Model(inputs=input_layer, outputs=output_layer)

# Compile the model
# We use mean squared error as our loss function, as we're predicting numerical values (0, 1, 2)
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

# Train the model
print("\nTraining the TensorFlow model...")
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2, verbose=1)

# Evaluate the model on the test set
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"\nAccuracy for predicting both ROW and COLUMN: {accuracy:.2f}")
print(f"Loss on test data: {loss:.4f}")

# Save the trained model
model_dir = os.path.join(project_root, 'ml_artifacts')
model_filename = os.path.join(model_dir, 'tic_tac_toe_tf_model.keras')

model.save(model_filename)
print(f"\nTensorFlow model saved to '{model_filename}'")