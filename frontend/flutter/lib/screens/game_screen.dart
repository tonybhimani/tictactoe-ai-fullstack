import 'package:flutter/material.dart';
import 'package:tictactoe_app/services/tictactoe_game.dart'; // Import the game logic class

class GameScreen extends StatefulWidget {
  const GameScreen({super.key});

  @override
  State<GameScreen> createState() => _GameScreenState();
}

class _GameScreenState extends State<GameScreen> {
  // Instantiate the game logic class
  final TicTacToeGame _game = TicTacToeGame();

  // State variables for UI feedback
  bool _isLoading = false;

  // Game state player message
  String _statusMessage = "Your turn (O)";

  void _onCellTapped(int index) async {
    // Return early if the game is not active or if a cell is already taken
    if (!_game.gameActive || _game.boardData[index ~/ 3][index % 3] != null) {
      return;
    }

    setState(() {
      // Human move: update the board data and UI
      _game.makeHumanMove(index ~/ 3, index % 3);
      _statusMessage = "Computer is thinking...";
    });

    // Computer move
    setState(() {
      _isLoading = true; // Show loading spinner
    });

    try {
      // Simulating network latency
      // await Future.delayed(const Duration(milliseconds: 500));
      // Get the final game status from the API
      String status = await _game.getComputerMove();

      setState(() {
        _isLoading = false; // Hide loading spinner
      });

      if (status != "ongoing") {
        _game.gameActive = false;
        _handleGameEnd(status);
      } else {
        setState(() {
          _statusMessage = "Your turn (O)";
        });
      }
    } catch (e) {
      _showErrorDialog("An error occurred: ${e.toString()}");
      setState(() {
        _isLoading = false; // Ensure spinner is hidden on error
      });
    }
  }

  void _handleGameEnd(String status) {
    String message;
    switch (status) {
      case "win-O":
        message = "You Won!";
        _showGameStatusDialog(message);
        break;
      case "win-X":
        message = "You Lost!";
        _showGameStatusDialog(message);
        break;
      case "draw":
        message = "It's a Draw!";
        _showGameStatusDialog(message);
        break;
      default:
        message = "Game Over!";
        _showErrorDialog(status);
    }
    setState(() {
      _statusMessage = message;
    });
  }

  void _resetGame() {
    setState(() {
      _game.clearGameBoard();
      _statusMessage = "Your turn (O)";
    });
  }

  void _showGameStatusDialog(String message) {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('Game Over'),
          content: Text(message),
          actions: <Widget>[
            OverflowBar(
              alignment: MainAxisAlignment.center,
              children: <Widget>[
                TextButton(
                  // child: const Text('New Game'),
                  child: const Text('Close'),
                  onPressed: () {
                    Navigator.of(context).pop();
                    // _resetGame();
                  },
                ),
              ],
            ),
          ],
        );
      },
    );
  }

  void _showErrorDialog(String message) {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('Error'),
          content: Text(message),
          actions: <Widget>[
            OverflowBar(
              alignment: MainAxisAlignment.center,
              children: <Widget>[
                TextButton(
                  child: const Text('Close'),
                  onPressed: () {
                    Navigator.of(context).pop();
                  },
                ),
              ],
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
        child: Center(
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                Padding(
                  padding: const EdgeInsets.only(top: 40.0),
                  child: const Text(
                    'Tic-Tac-Toe Game: Flutter Demo',
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: Text(
                    _statusMessage,
                    style: const TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
                // Game Board
                ConstrainedBox(
                  constraints: const BoxConstraints(
                    maxWidth: 417.0,
                    maxHeight: 417.0,
                  ),
                  child: Stack(
                    children: <Widget>[
                      Image.asset(
                        'assets/images/game_board.jpg',
                        fit: BoxFit.fitWidth,
                      ),
                      GridView.builder(
                        padding: EdgeInsets.zero,
                        gridDelegate:
                            const SliverGridDelegateWithFixedCrossAxisCount(
                              crossAxisCount: 3,
                            ),
                        itemCount: 9,
                        physics: NeverScrollableScrollPhysics(),
                        itemBuilder: (BuildContext context, int index) {
                          // Calculate row and column
                          int row = (index / 3).floor();
                          int col = index % 3;
                          String? symbol = _game.boardData[row][col];

                          return GestureDetector(
                            onTap: _isLoading
                                ? null
                                : () => _onCellTapped(index),
                            child: Container(
                              decoration: BoxDecoration(
                                // border: Border.all(color: Colors.black),
                              ),
                              child: Center(
                                child: symbol == null
                                    ? Container() // empty container for a blank cell
                                    : Image.asset(
                                        'assets/images/${symbol.toLowerCase()}.png',
                                        fit: BoxFit.cover,
                                      ),
                              ),
                            ),
                          );
                        },
                      ),

                      // Loading overlay
                      if (_isLoading)
                        Container(
                          color: Colors.black.withOpacity(0.5),
                          child: const Center(
                            child: CircularProgressIndicator(),
                          ),
                        ),
                    ],
                  ),
                ),
                // Options Panel
                Container(
                  padding: const EdgeInsets.all(20.0),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: <Widget>[
                      const Text("Difficulty: "),
                      const SizedBox(width: 10),
                      DropdownButton<String>(
                        value: _game.difficultyLevel,
                        items: const [
                          DropdownMenuItem(value: 'Easy', child: Text('Easy')),
                          DropdownMenuItem(
                            value: 'Medium',
                            child: Text('Medium'),
                          ),
                          DropdownMenuItem(value: 'Hard', child: Text('Hard')),
                        ],
                        onChanged: _isLoading
                            ? null
                            : (String? newValue) {
                                if (newValue != null) {
                                  setState(() {
                                    _game.setDifficultyLevel(newValue);
                                    // _resetGame(); // Reset game on difficulty change
                                  });
                                }
                              },
                      ),
                      const SizedBox(width: 10),
                      ElevatedButton(
                        onPressed: _isLoading ? null : _resetGame,
                        child: const Text('Reset Game'),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
