# Backend – Flask API

This is the backend component of the TicTacToe AI Fullstack project. It provides a RESTful API that powers AI gameplay across multiple difficulty levels — from random moves to a machine learning–driven medium mode, to an unbeatable minimax mode.

The backend is built with **Flask** and includes:

- Game state processing and move generation
- AI logic implemented in both traditional algorithms and trained ML models
- Scripts for generating training data and retraining models
- Static file hosting for the web-based frontends

It serves as the central game engine for all frontend implementations — Vanilla JavaScript, Vue.js, Unity, and Flutter — ensuring a consistent AI experience across platforms.

---

## 🧩 Features

The backend provides the core AI engine for TicTacToe gameplay, handling move generation, difficulty scaling, and model-based decision-making — all exposed via a clean REST API.

- **Single stateless API endpoint** — `/api/get_computer_move` accepts a 3×3 board, computer symbol, and difficulty; returns the AI's move and game status in JSON.
- **Three difficulty levels:**

  - **Easy** — picks a random available move.
  - **Medium** — uses an ML model trained on 10,000 self-play games (20% random / 80% minimax); defaults to Scikit-learn, with a TensorFlow model included as an option.
  - **Hard** — employs a minimax search for perfect, unbeatable play.

- **Centralized game logic** — `TicTacToeGame` class with enums for `CellState` and `DifficultyLevel`, plus utilities for win/draw checks.
- **Optimized AI model loading** — models are loaded once at server start for fast responses; API remains stateless with no server-side game tracking.
- **Built-in training pipeline** — `scripts/` folder includes tools to generate self-play data and train both Scikit-learn and TensorFlow models; artifacts stored in `ml_artifacts/`.
- **Static file serving** — allows local hosting of Vanilla JS and Vue.js frontend demos directly from the backend.
- **Lightweight, dependency-based design** — no database or persistent storage required.

---

## 📁 Project Structure

The backend contains the Flask API, core game logic, machine learning models, training scripts, and supporting data organized as follows:

```
backend/
├── data/
│   ├── raw/
│   │   └── tic_tac_toe_games.csv      # Generated gameplay dataset used for ML training
├── game/
│   └── tictactoe.py                   # Core game logic, win/draw checks, and move handling
├── ml_artifacts/
│   ├── feature_names.joblib           # Feature labels for Scikit-learn models
│   ├── tic_tac_toe_col_model.joblib   # Trained Scikit-learn model (column prediction)
│   ├── tic_tac_toe_row_model.joblib   # Trained Scikit-learn model (row prediction)
│   └── tic_tac_toe_tf_model.keras     # Trained TensorFlow model (combined row/col)
├── scripts/
│   ├── generate_game_data.py          # Generates self-play games for training data
│   ├── train_model_sk.py              # Trains the Scikit-learn model from generated data
│   └── train_model_tf.py              # Trains the TensorFlow model from generated data
├── static/                            # Hosts static web clients for local testing
├── requirements.txt                   # Python package dependencies
├── run.py                             # Flask app entry point (starts the API server)
└── README.md                          # Documentation for the backend
```

---

## 📦 Requirements

- Python 3.10+
- pip
- virtualenv (optional but recommended)

---

## 🚀 Setup

1. Clone the repository and navigate to the backend folder:

```bash
cd backend
```

2. (Optional) Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Generate training data and train ML models

Even if prebuilt models are included, you can regenerate the training data and retrain the models to customize or experiment.

Run all commands from the project root or `/backend` folder.

**Step 1: Generate training data**

```bash
python scripts/generate_game_data.py
```

This simulates 10,000 games with 20% random and 80% minimax moves to create training data.

The output CSV will be saved as:

```
data/raw/tic_tac_toe_games.csv
```

Sample console output during generation:

```
Playing 10000 games to collect training data...
  1000 games played.
  2000 games played.
  3000 games played.
  4000 games played.
  5000 games played.
  6000 games played.
  7000 games played.
  8000 games played.
  9000 games played.
  10000 games played.
Data collection complete! Collected 79902 data points.
```

**Step 2: Train the Scikit-learn model**

```bash
python scripts/train_model_sk.py
```

Sample console output:

```
Training data size: 63921 samples
Testing data size: 15981 samples

Training model for best move ROW...
Accuracy for predicting the ROW: 0.86

Training model for best move COLUMN...
Accuracy for predicting the COLUMN: 0.88
```

**Step 3: Train the TensorFlow model**

```bash
python scripts/train_model_tf.py
```

Sample console output:

```
Training the TensorFlow model...
Epoch 1/10
1598/1598 [==============================] - 2s 956us/step - loss: 0.3590 - accuracy: 0.7058 - val_loss: 0.2722 - val_accuracy: 0.6998
Epoch 2/10
1598/1598 [==============================] - 1s 838us/step - loss: 0.2683 - accuracy: 0.7263 - val_loss: 0.2590 - val_accuracy: 0.6833
...
Epoch 10/10
1598/1598 [==============================] - 1s 832us/step - loss: 0.2433 - accuracy: 0.7386 - val_loss: 0.2430 - val_accuracy: 0.6842

Accuracy for predicting both ROW and COLUMN: 0.68
Loss on test data: 0.2394
```

> **Note:** Generating gameplay data and training models can be time-consuming depending on your machine. TensorFlow training tends to be faster than data generation but is still CPU-intensive.

5. Run the development server:

```bash
python run.py
```

The API will be available at:

```
http://127.0.0.1:5000/api
```

---

## 📂 Static Files

The `/static` folder in the backend serves static web clients such as the Vanilla JS and Vue.js frontends.

To run these clients locally, copy their build files into the `/backend/static` directory, then start the Flask server. Access them via:

```
http://127.0.0.1:5000/index.html
```

This provides a simple way to test frontend clients without a separate web server.
