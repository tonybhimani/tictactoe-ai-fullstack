// Create a Vue application instance
const app = Vue.createApp({
  // The `data` option defines the reactive state of the application
  data() {
    return {
      gameActive: true,
      apiUrl: "http://127.0.0.1:5000/api/get_computer_move",
      boardData: [
        [null, null, null],
        [null, null, null],
        [null, null, null],
      ],
      humanSymbol: "O",
      computerSymbol: "X",
      difficultyLevel: "Easy",
      isLoading: false,
      modalMessage: "",
      isModalVisible: false,
    };
  },
  methods: {
    handleCellClick(row, col) {
      if (!this.gameActive || this.boardData[row][col] !== null) return;

      this.boardData[row][col] = this.humanSymbol;
      this.getComputerMove();
    },

    handleResetGameClick() {
      this.gameActive = true;
      this.boardData = [
        [null, null, null],
        [null, null, null],
        [null, null, null],
      ];
    },

    handleModalClose() {
      this.isModalVisible = false;
    },

    printBoardData() {
      console.log(this.boardData);
    },

    async getComputerMove() {
      this.isLoading = true;

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
        const [row, col] = responseData.computer_move;
        if (row !== -1 && col !== -1) {
          this.boardData[row][col] = this.computerSymbol;
        }

        // If the game isn't ongoing, display the message
        if (responseData.game_status != "ongoing") {
          this.gameActive = false;
          switch (responseData.game_status) {
            case "win-O":
              this.modalMessage = "You Won!";
              break;
            case "win-X":
              this.modalMessage = "You lost!";
              break;
            case "draw":
              this.modalMessage = "It's a draw!";
              break;
          }
          this.isModalVisible = true;
        }
      } catch (error) {
        console.error("Error:", error);
        this.gameActive = false;
        this.modalMessage = "An error occurred. Please try resetting the game.";
        this.isModalVisible = true;
      } finally {
        this.isLoading = false;
      }
    },

    // Leaving this method, but :disabled handles the state -- see mounted() below
    setGameControlsEnabled(enabled) {
      if (this.gameControls && this.gameControls.difficultyDropdown) {
        this.gameControls.difficultyDropdown.disabled = !enabled;
      }

      if (this.gameControls && this.gameControls.resetButton) {
        this.gameControls.resetButton.disabled = !enabled;
      }
    },
  },
  mounted() {
    // Vue's lifecycle hook for when the component is mounted
    this.gameControls = {
      difficultyDropdown: document.getElementById("difficulty_level"),
      resetButton: document.getElementById("reset-game"),
    };
  },
});

// Mount the application to the HTML element with id="app"
app.mount("#app");

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
