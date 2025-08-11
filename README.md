# 🧠 TicTacToe AI Fullstack

TicTacToe AI Fullstack is a complete multi-platform project featuring a Flask API backend with three difficulty levels — including a machine learning–powered medium mode — and four distinct frontend implementations: Vanilla JavaScript, Vue.js, Unity, and Flutter.

The backend exposes a RESTful API that accepts the current game board state and returns the AI's next move. Difficulty modes include:

- **Easy** → Random moves
- **Medium** → 80% minimax algorithm, 20% random (trained on 10,000 games)
- **Hard** → Pure minimax for optimal play

The frontends showcase how the same API can be integrated into different frameworks, engines, and platforms, making this a practical reference for developers learning cross-platform client development.

---

## ✨ Features

✅ **Backend (Python + Flask)**

- Flask-based REST API for AI-powered Tic-Tac-Toe
- Three AI difficulty levels (Random, Hybrid ML, Minimax)
- Machine learning model trained on 10,000 simulated games
- TensorFlow + Scikit-learn training scripts included
- Modular backend with scripts for data generation and training
- Static file hosting for web-based clients
- Environment-based configuration via `.env`

✅ **Frontend Implementations**

- **Vanilla JavaScript** — Simple DOM-based client served via Flask static files
- **Vue.js** — SPA example, also served via Flask static files
- **Unity** — 2D project integrating the Flask API via HTTP
- **Flutter** — Cross-platform mobile/web client using the same API

---

## 📂 Project Structure

```
tictactoe-ai-fullstack/
├── backend/                   # Flask backend API for game logic, ML models, static hosting
├── frontend/                  # Four parallel client implementations: Vanilla JS, Vue.js, Unity, Flutter
├── LICENSE                    # MIT license for the entire project
└── README.md                  # Main project overview and usage instructions
```

---

## 🚀 Getting Started

### 1. Backend Setup (Flask)

#### a. Set up virtual environment and install dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

> **Note:** Installing dependencies may take a while, especially TensorFlow (due to compilation). Be patient — coffee breaks are encouraged.

---

#### b. Generate gameplay data and train models

Even though prebuilt models may be included in the repository, you can regenerate them to:

- Use more/less training data
- Adjust the randomness percentage for medium difficulty
- Experiment with different ML configurations

Run all commands from the `/backend` directory.

1. **Generate training data**

   ```bash
   python scripts/generate_game_data.py
   ```

   Output saved to:

   ```
   data/raw/tic_tac_toe_games.csv
   ```

2. **Train the Scikit-learn model**

   ```bash
   python scripts/train_model_sk.py
   ```

3. **Train the TensorFlow model**

   ```bash
   python scripts/train_model_tf.py
   ```

---

#### c. Run the API server

```bash
python run.py
```

Your API will be available at:

```
http://127.0.0.1:5000/api
```

---

## 2. Frontend Setup

### 2.a Vanilla JS

The files need to be hosted on a web server. You can copy the contents of `frontend/vanilla-js` into the backend's `static` folder and access it at:

```
http://127.0.0.1:5000/index.html
```

---

### 2.b Vue.js

Same as Vanilla JS — copy the `frontend/vue` build output into the backend's `static` folder, then access via the same URL.

---

### 2.c Unity

1. Create a new Unity 2D project and close Unity.
2. Delete your project's default `Assets/` folder.
3. Copy the `Assets/` folder from `frontend/unity` into your Unity project directory.
4. Open Unity — you may see a "Safe Mode" warning if Newtonsoft.Json isn't installed.
5. Import Newtonsoft.Json:

   - Go to **Window → Package Manager**.
   - Click **+** → "Add package by name..." and enter:

     ```
     com.unity.nuget.newtonsoft-json
     ```

   - Click **Add**.

6. Unity should reload and the error will disappear. If not, close and reopen the project.

---

### 2.d Flutter

Ensure Flutter is installed (`flutter doctor`) and working:

```bash
cd frontend/flutter
flutter pub get
flutter run -d chrome    # or other device/emulator id
```

Update API base URL in:

```
frontend/flutter/lib/utils/constants.dart
```

---

## 🔌 API Endpoints

| Endpoint                 | Method | Description                                                                                            |
| ------------------------ | ------ | ------------------------------------------------------------------------------------------------------ |
| `/api/get_computer_move` | POST   | Accepts current board state, computer symbol, and difficulty; returns AI's move and updated game state |

**Request JSON:**

```json
{
  "board": [
    ["X", "", ""],
    ["", "O", ""],
    ["", "", ""]
  ],
  "computer_symbol": "O",
  "difficulty_level": "Medium"
}
```

**Response JSON:**

```json
{
  "success": true,
  "board": [
    ["X", "", ""],
    ["", "O", ""],
    ["", "O", ""]
  ],
  "computer_move": [2, 1],
  "game_status": "ongoing"
}
```

`game_status` can be:

- `"win-X"`
- `"win-O"`
- `"draw"`
- `"ongoing"`

---

## 📸 Demo Preview

### Tic-Tac-Toe Gameplay

![Tic-Tac-Toe Gameplay](https://raw.githubusercontent.com/tonybhimani/tictactoe-ai-fullstack/refs/heads/media/tictactoe_flutter_demo.gif)

---

## 📌 Future Plans

There are no active plans to expand this project further. That said, I may revisit or build on it in the future. For now, it's meant as a functional example—feel free to explore or adapt it as you see fit.

---

## 🙌 Acknowledgments

This project was a hands-on way to apply concepts from a machine learning course, put more Flask API experience into practice, and make it fun with a classic game like Tic-Tac-Toe.

It also served as an experiment in building the same project across multiple frontends:

- **Unity** — familiar territory from my game tutorial channel.
- **Vanilla JS** — a long-time staple in my toolkit.
- **Vue.js** and **Flutter** — newer technologies I'm learning, explored here through practical implementation.

The result is both a learning exercise and a reference for cross-platform AI-powered game development.

---

## 📄 License

MIT License. Feel free to use or build on it. Attribution is appreciated but not required.
