# Frontend - Vanilla JavaScript

This is the Vanilla JavaScript frontend for the TicTacToe AI Fullstack project. It provides a simple web-based UI that communicates with the backend Flask API to play Tic-Tac-Toe with three difficulty levels.

---

## 🧩 Features

- Dynamic 3×3 game board created in the browser DOM using `div` elements
- Clickable cells with event listeners for player moves
- Internal game state management in JavaScript for consistent gameplay logic
- Asynchronous API calls to the backend endpoint to get the AI's next move
- Difficulty levels selectable mid-game: Easy, Medium, Hard
- Reset button to clear the board and start a new game
- Visual feedback with overlays and spinners during AI move computation
- Displays game status messages for wins, draws, and ongoing play

---

## 📁 Project Structure

```
frontend/vanilla-js
├── images/              # Image assets for game UI elements (board, X, O)
├── scripts/
│   ├── main.js          # Instantiates and initializes the TicTacToe game class on page load
│   └── tictactoe.js     # Game logic class; manages moves, UI updates, and API communication
├── styles/
│   └── main.css         # Stylesheet controlling the layout and look of the game
├── index.html           # Entry point; HTML skeleton hosting the game UI
└── README.md            # This file
```

---

## 🧰 How It Works

The app loads `index.html` which initializes a TicTacToe game instance using the `tictactoe.js` class. This class dynamically creates the game board as a grid of clickable `div` elements, each with `data-row` and `data-col` attributes representing their position.

When the player clicks on an empty cell:

1. The human player's symbol is placed visually on the board.
2. The internal game state is updated accordingly.
3. An asynchronous POST request is sent to the backend `/api/get_computer_move` endpoint with the current board state, the AI symbol, and selected difficulty.
4. A loading overlay and spinner appear to indicate the AI is thinking.
5. When the backend responds with the AI's move and updated game status, the board updates with the AI's move.
6. The game status is checked and displayed — whether it's a win, draw, or ongoing play.
7. The player can reset the game at any time or switch difficulty mid-game.

This approach keeps the game logic centralized on the frontend while delegating AI move calculation to the backend API.

---

## 🚀 Setup and Usage

To run locally, you need a webserver that can serve static files. The simplest approach is to copy the contents of this folder into the backend's `static/` directory and serve it via the Flask server.

**Steps:**

1. Copy the contents of `frontend/vanilla-js` into `backend/static`
2. Start the backend server (`python run.py`)
3. Open your browser and navigate to:

   ```
   http://127.0.0.1:5000/index.html
   ```

The game should load and be fully playable.

---

## ⚙️ Configuration

The API URL is currently hardcoded in `scripts/tictactoe.js` as:

```js
apiUrl = "http://127.0.0.1:5000/api/get_computer_move";
```

If hosting the frontend separately, update this URL accordingly.
