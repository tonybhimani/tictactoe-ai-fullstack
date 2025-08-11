import sys
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib  # To save the trained model

# --- Train model usng Scikit-learn ---

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

if project_root not in sys.path:
    sys.path.append(project_root)

# Load the data from the CSV file
raw_data_dir = os.path.join(project_root, 'data/raw')
csv_file_path = os.path.join(raw_data_dir, 'tic_tac_toe_games.csv')
data = pd.read_csv(csv_file_path)

# Separate the features (board state) from the labels (best move)
# The first 9 columns are the board features, and the last 2 are the best move.
X = data.iloc[:, :9]
y_row = data['best_move_row']
y_col = data['best_move_col']

# We need to train two separate models, one for the row and one for the column.
# This is because Scikit-learn's classifiers typically predict a single target variable.
# We'll create two classifiers to predict the two coordinates of the best move.

# Split the data into training and testing sets
X_train, X_test, y_row_train, y_row_test, y_col_train, y_col_test = train_test_split(
    X, y_row, y_col, test_size=0.2, random_state=42
)

print(f"Training data size: {len(X_train)} samples")
print(f"Testing data size: {len(X_test)} samples")

# --- Train the model for predicting the best move's ROW ---
print("\nTraining model for best move ROW...")
row_classifier = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
row_classifier.fit(X_train, y_row_train)

# Make predictions on the test set
y_row_pred = row_classifier.predict(X_test)
row_accuracy = accuracy_score(y_row_test, y_row_pred)
print(f"Accuracy for predicting the ROW: {row_accuracy:.2f}")

# --- Train the model for predicting the best move's COLUMN ---
print("\nTraining model for best move COLUMN...")
col_classifier = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
col_classifier.fit(X_train, y_col_train)

# Make predictions on the test set
y_col_pred = col_classifier.predict(X_test)
col_accuracy = accuracy_score(y_col_test, y_col_pred)
print(f"Accuracy for predicting the COLUMN: {col_accuracy:.2f}")

# Save the trained models to disk
model_dir = os.path.join(project_root, 'ml_artifacts')
model_filename_row = os.path.join(model_dir, 'tic_tac_toe_row_model.joblib')
model_filename_col = os.path.join(model_dir, 'tic_tac_toe_col_model.joblib')
joblib.dump(row_classifier, model_filename_row)
joblib.dump(col_classifier, model_filename_col)

# Get the feature names from the DataFrame
feature_names = X_train.columns.tolist()

# Save the feature names as well
model_filename_feature_names = os.path.join(model_dir, 'feature_names.joblib')
joblib.dump(feature_names, model_filename_feature_names)

print(f"\nModels saved to '{model_filename_row}' and '{model_filename_col}'")
print(f"Feature names saved to '{model_filename_feature_names}'")