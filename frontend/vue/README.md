# Frontend - Vue.js

This is the Vue.js frontend for the TicTacToe AI Fullstack project. It offers a reactive single-page application (SPA) interface built with Vue 3 that communicates with the backend Flask API to play Tic-Tac-Toe with multiple difficulty levels.

---

## 🧩 Features

- Reactive 3×3 game board rendered using Vue's `v-for` loops and reactive data binding
- Clickable cells with Vue event handling (`@click`) to register player moves
- Vue data properties (`data()`) manage the board state, difficulty, loading, and game status
- Asynchronous API calls to the backend `/api/get_computer_move` endpoint using `fetch` with timeout support
- Difficulty selection and reset buttons integrated with Vue's reactive state
- Loading overlay and modal dialogs controlled by reactive boolean flags (`v-if`) for smooth UI feedback
- Handles game state changes with modal messages for wins, losses, and draws
- Clean separation of UI and logic leveraging Vue's component lifecycle (`mounted` hook)

---

## 📁 Project Structure

```
frontend/vue
├── images/             # Image assets for the game UI (board, X, O)
├── scripts/
│   └── main.js         # Vue 3 app instance; contains data, methods, and lifecycle hooks
├── styles/
│   └── main.css        # Stylesheet for the game layout and visual elements
├── index.html          # Single-page HTML entry point hosting the Vue app
└── README.md           # This file
```

---

## 🧰 How It Works

The app loads `index.html`, which contains a root `<div id="app">` that Vue mounts onto. The Vue application instance defined in `main.js`:

- Uses reactive data properties to track the current board (`boardData`), the selected difficulty (`difficultyLevel`), and UI states like loading and modal visibility
- Dynamically renders the 3×3 game board with nested `v-for` loops, applying conditional classes for "X" and "O" cells
- Handles player clicks on cells with the `handleCellClick` method, updating the local board state immediately
- Calls the backend API asynchronously to retrieve the AI's move, using a helper function to add a timeout to the `fetch` call
- Updates the board with the AI's move when the response arrives, and displays modal messages for game outcomes
- Provides a Reset button to clear the board and restart the game at any time
- Disables interaction controls while awaiting the AI's move to prevent multiple concurrent requests

This SPA approach leverages Vue's reactive data binding and declarative templates to keep UI and state in sync seamlessly.

---

## 🚀 Setup and Usage

To run locally, copy the contents of this folder into the backend's `static/` directory and serve it via the Flask backend server.

**Steps:**

1. Copy the contents of `frontend/vue` into `backend/static`

2. Start the backend Flask server:

   ```bash
   python run.py
   ```

3. Open your browser to:

   ```
   http://127.0.0.1:5000/index.html
   ```

The Vue Tic-Tac-Toe app should load and connect with the backend API automatically.

---

## ⚙️ Configuration

The API URL is currently hardcoded in `scripts/main.js` as:

```js
apiUrl: "http://127.0.0.1:5000/api/get_computer_move",
```

If hosting the frontend separately, update this URL accordingly.
