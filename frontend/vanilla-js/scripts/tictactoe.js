class TicTacToeClient {
  // API Endpoint URL to Flask server
  apiUrl = "http://127.0.0.1:5000/api/get_computer_move";

  // Store all the game moves here
  boardData = [];

  constructor(rootElementId) {
    this.gameActive = true;

    // Initialize the board with 3 rows and 3 columns
    for (let row = 0; row < 3; row++) {
      this.boardData[row] = new Array(3);
    }

    // Set default symbols
    this.humanSymbol = "O";
    this.computerSymbol = "X";

    // Set the default difficulty level
    this.difficultyLevel = "Easy";

    // Create the game board UI
    this.createGameUI(rootElementId);
  }

  createGameUI(rootElementId) {
    const rootElement = document.getElementById(rootElementId);

    if (!rootElement) {
      console.error(`Error: Element with ID '${rootElementId}' not found.`);
      return;
    }

    const gameContainer = document.createElement("div");
    gameContainer.id = "game-container";

    rootElement.appendChild(gameContainer);

    this.createGameBoard("game-container");
    this.createOptionsPanel("game-container");
    this.createLoadingOverlay("game-container");
    this.createGameMessageModal("game-container");
  }

  createGameBoard(rootElementId) {
    const rootElement = document.getElementById(rootElementId);

    if (!rootElement) {
      console.error(`Error: Element with ID '${rootElementId}' not found.`);
      return;
    }

    const gameBoard = document.createElement("div");
    gameBoard.classList.add("gameboard");

    for (let i = 0; i < 9; i++) {
      const cell = document.createElement("div");
      cell.id = `cell${i + 1}`;
      cell.classList.add("cell");

      // Use the dataset property to store row and column
      const row = Math.floor(i / 3);
      const col = i % 3;
      cell.dataset.row = row;
      cell.dataset.col = col;

      gameBoard.appendChild(cell);
    }

    gameBoard.addEventListener("click", this.handleGameBoardClick.bind(this));

    rootElement.appendChild(gameBoard);
  }

  createOptionsPanel(rootElementId) {
    const rootElement = document.getElementById(rootElementId);

    if (!rootElement) {
      console.error(`Error: Element with ID '${rootElementId}' not found.`);
      return;
    }

    const optionsPanel = document.createElement("div");
    optionsPanel.classList.add("options-panel");

    const difficultyLabel = document.createElement("label");
    difficultyLabel.textContent = "Difficulty: ";

    const difficultyDropdown = document.createElement("select");
    difficultyDropdown.id = "difficulty_level";

    ["Easy", "Medium", "Hard"].forEach((level) => {
      const option = document.createElement("option");
      option.value = level;
      option.textContent = level;
      difficultyDropdown.appendChild(option);
    });

    difficultyDropdown.addEventListener(
      "change",
      this.handleDifficultyChange.bind(this)
    );

    optionsPanel.appendChild(difficultyLabel);
    optionsPanel.appendChild(difficultyDropdown);

    const resetButton = document.createElement("button");
    resetButton.id = "reset-game";
    resetButton.textContent = "Reset Game";

    resetButton.addEventListener("click", this.handleResetGameClick.bind(this));

    optionsPanel.appendChild(resetButton);

    rootElement.appendChild(optionsPanel);

    this.gameControls = {
      difficultyDropdown: difficultyDropdown,
      resetButton: resetButton,
    };
  }

  createLoadingOverlay(rootElementId) {
    const rootElement = document.getElementById(rootElementId);

    if (!rootElement) {
      console.error(`Error: Element with ID '${rootElementId}' not found.`);
      return;
    }

    const overlay = document.createElement("div");
    overlay.id = "loading-overlay";
    overlay.classList.add("hidden"); // Initially hidden

    const spinner = document.createElement("div");
    spinner.classList.add("spinner");

    overlay.appendChild(spinner);

    rootElement.appendChild(overlay);
  }

  createGameMessageModal(rootElementId, onClose = () => {}) {
    const rootElement = document.getElementById(rootElementId);

    if (!rootElement) {
      console.error(`Error: Element with ID '${rootElementId}' not found.`);
      return;
    }

    // Main modal container
    const modal = document.createElement("div");
    modal.id = "game-message-modal";
    modal.classList.add("hidden"); // Initially hidden

    // Modal content box
    const modalContent = document.createElement("div");
    modalContent.classList.add("modal-content");

    // Paragraph for the message text
    const messageText = document.createElement("p");
    messageText.id = "game-message-text";

    // Close button
    const closeButton = document.createElement("button");
    closeButton.id = "modal-close-button";
    closeButton.textContent = "Close";

    // Attach event listener for the close button
    closeButton.addEventListener("click", () => {
      modal.classList.add("hidden");
      onClose(); // Execute the optional callback
    });

    // Assemble the modal structure
    modalContent.appendChild(messageText);
    modalContent.appendChild(closeButton);
    modal.appendChild(modalContent);

    // Append the entire modal to the root element
    rootElement.appendChild(modal);
  }

  showMessageModal(message) {
    const modal = document.getElementById("game-message-modal");
    const messageText = document.getElementById("game-message-text");

    messageText.textContent = message;
    modal.classList.remove("hidden");
  }

  toggleLoadingOverlay(isVisible) {
    const loadingOverlay = document.getElementById("loading-overlay");
    if (isVisible) {
      loadingOverlay.classList.remove("hidden");
    } else {
      loadingOverlay.classList.add("hidden");
    }
  }

  setGameControlsEnabled(enabled) {
    if (this.gameControls && this.gameControls.difficultyDropdown) {
      this.gameControls.difficultyDropdown.disabled = !enabled;
    }

    if (this.gameControls && this.gameControls.resetButton) {
      this.gameControls.resetButton.disabled = !enabled;
    }
  }

  setDifficultyLevel(difficultyLevel) {
    this.difficultyLevel = difficultyLevel;
  }

  clearGameBoard() {
    this.gameActive = true;
    // Update the state
    for (let row = 0; row < 3; row++) {
      for (let col = 0; col < 3; col++) {
        this.boardData[row][col] = null;
      }
    }
    // Update the UI
    this.render();
  }

  render() {
    // Loop through the boardData and update the UI
    for (let row = 0; row < 3; row++) {
      for (let col = 0; col < 3; col++) {
        const linearPosition = this.getLinearPosition(row, col);
        const gameCell = document.getElementById("cell" + linearPosition);
        const symbol = this.boardData[row][col];

        // Clear any existing symbols
        gameCell.classList.remove("x-symbol", "o-symbol");
        gameCell.removeAttribute("data-value");

        if (symbol) {
          // If there's a symbol in our data, add it to the UI
          const symbolClass = symbol == "X" ? "x-symbol" : "o-symbol";
          gameCell.classList.add(symbolClass);
          gameCell.dataset.value = symbol;
        }
      }
    }
  }

  updateBoardPosition(position, symbol) {
    const [row, col] = this.getCellIndices(position);
    this.boardData[row][col] = symbol;
  }

  getCellIndices(linearPosition) {
    if (linearPosition < 1 || linearPosition > 9) {
      throw new Error("Linear position must be between 1 and 9.");
    }

    // Adjust to a 0-based index
    const zeroBasedIndex = linearPosition - 1;

    const row = Math.floor(zeroBasedIndex / 3);
    const col = zeroBasedIndex % 3;

    return [row, col];
  }

  getLinearPosition(row, col) {
    // Add validation to ensure the indices are within a 3x3 grid
    if (row < 0 || row > 2 || col < 0 || col > 2) {
      throw new Error("Row and column indices must be between 0 and 2.");
    }

    // Formula: (rows before * cols per row) + current col + 1 for 1-based index
    const linearPosition = row * 3 + col + 1;

    return linearPosition;
  }

  printBoardData() {
    console.log(this.boardData);
  }

  async getComputerMove() {
    // Show the overlay & disable controls
    this.toggleLoadingOverlay(true);
    this.setGameControlsEnabled(false);

    try {
      const data = {
        board: this.boardData,
        computer_symbol: this.computerSymbol,
        difficulty_level: this.difficultyLevel,
      };

      const response = await fetchWithTimeout(this.apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          // Add any other headers here, like authorization tokens
        },
        body: JSON.stringify(data),
        timeout: 2000,
      });

      // Check if the request was successful
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // Parse the JSON from the response
      const responseData = await response.json();

      // Update the board data from the response
      let row = responseData.computer_move[0];
      let col = responseData.computer_move[1];
      if (row != -1 && col != -1) {
        this.boardData[row][col] = this.computerSymbol;
      }

      // Now, call the render method to update the UI
      this.render();

      // If the game isn't ongoing, display the message
      if (responseData.game_status != "ongoing") {
        this.gameActive = false;
        switch (responseData.game_status) {
          case "win-O":
            this.showMessageModal("You Won!");
            break;
          case "win-X":
            this.showMessageModal("You lost!");
            break;
          case "draw":
            this.showMessageModal("It's a draw!");
            break;
        }
      }
    } catch (error) {
      console.error("Error:", error);
      // Disable the game so the user can't click on the board
      this.gameActive = false;
      // Show a user-friendly error message
      this.showMessageModal(
        "An error occurred. Please try resetting the game."
      );
    } finally {
      // Hide the overlay regardless of success or failure
      this.toggleLoadingOverlay(false);
      // Re-enable the game controls
      this.setGameControlsEnabled(true);
    }
  }

  handleGameBoardClick(event) {
    if (!this.gameActive) return;

    // Get the row and column from the target's dataset
    const cellElement = event.target;
    const row = cellElement.dataset.row;
    const col = cellElement.dataset.col;

    if (row != undefined && col != undefined) {
      const cellValue = this.boardData[row][col];
      if (cellValue == null) {
        this.boardData[row][col] = this.humanSymbol; // Update the state
        this.render(); // Call the render method
        this.getComputerMove();
      } else {
        console.log(`Cell already has a value set.`);
      }
    }
  }

  handleDifficultyChange(event) {
    this.setDifficultyLevel(event.target.value);
  }

  handleResetGameClick() {
    this.clearGameBoard();
  }
}

// Help function to give fetch a timeout
async function fetchWithTimeout(url, options = {}) {
  const { timeout = 5000, ...fetchOptions } = options;

  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, {
      ...fetchOptions,
      signal: controller.signal,
    });
    return response;
  } catch (error) {
    // Just re-throw the error so the calling function can handle it
    throw error;
  } finally {
    clearTimeout(id); // Clear the timeout
  }
}

export default TicTacToeClient;
