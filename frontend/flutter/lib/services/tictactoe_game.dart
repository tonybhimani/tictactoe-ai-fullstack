import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:async';
import 'package:tictactoe_app/utils/constants.dart';

class TicTacToeGame {
  final String _apiUrl = "$kApiUrl/get_computer_move";

  // Use a List of Lists to represent the 3x3 board
  // The type is `String?` to allow for null values (empty cells)
  List<List<String?>> boardData;

  bool gameActive;
  String humanSymbol;
  String computerSymbol;
  String difficultyLevel;

  // Constructor to initialize the game state
  TicTacToeGame()
    : boardData = List.generate(3, (_) => List.filled(3, null)),
      gameActive = true,
      humanSymbol = "O",
      computerSymbol = "X",
      difficultyLevel = "Easy";

  // This method will be called by the UI's setState
  void clearGameBoard() {
    gameActive = true;
    boardData = List.generate(3, (_) => List.filled(3, null));
  }

  // Update the board and check for game status
  void makeHumanMove(int row, int col) {
    if (gameActive && boardData[row][col] == null) {
      boardData[row][col] = humanSymbol;
    }
  }

  // This function makes the API call to get the computer's move
  // It returns the new game status after the move is made
  Future<String> getComputerMove() async {
    try {
      final Map<String, dynamic> data = {
        "board": boardData,
        "computer_symbol": computerSymbol,
        "difficulty_level": difficultyLevel,
      };

      // Set a timeout for the HTTP request.
      final response = await http
          .post(
            Uri.parse(_apiUrl),
            headers: {
              "Content-Type": "application/json",
              // Add any other headers here, like authorization tokens
            },
            body: jsonEncode(data),
          )
          .timeout(const Duration(seconds: 2));

      if (response.statusCode != 200) {
        throw Exception("Failed to get computer move: ${response.statusCode}");
      }

      final responseData = jsonDecode(response.body);
      final List<dynamic> computerMove = responseData['computer_move'];

      if (computerMove[0] != -1 && computerMove[1] != -1) {
        int row = computerMove[0];
        int col = computerMove[1];
        boardData[row][col] = computerSymbol;
      }

      return responseData['game_status'] as String;
    } on TimeoutException {
      // Handles timeout errors
      return "An error occurred: The request timed out.";
    } catch (e) {
      // General error handling for other exceptions
      print("Error fetching computer move: $e");
      return "An error occurred: Please try again.";
    }
  }

  // Setters for game properties
  void setDifficultyLevel(String newDifficulty) {
    difficultyLevel = newDifficulty;
  }
}
