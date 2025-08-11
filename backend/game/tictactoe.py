import os
import math
import random
import joblib
from tensorflow.keras.models import load_model
import pandas as pd
import numpy as np
from typing import List, Tuple
from enum import Enum

# --- TicTacToeGame Class ---

class CellState(Enum):
    Empty = None
    X = 'X'
    O = 'O'

class DifficultyLevel(Enum):
    Easy = 'Easy'
    Medium = 'Medium'
    Hard = 'Hard'

class TicTacToeGame:
    def __init__(self, load_models: bool = True) -> None:
        # Load the trained models
        if load_models:
            # 1. Get the directory of the current file (tictactoe.py)
            current_dir = os.path.dirname(os.path.abspath(__file__))

            # 2. Go up one directory to get to the project root
            project_root = os.path.dirname(current_dir)

            # 3. Construct the full paths to the model files
            model_dir = os.path.join(project_root, 'ml_artifacts')
            row_model_path = os.path.join(model_dir, 'tic_tac_toe_row_model.joblib')
            col_model_path = os.path.join(model_dir, 'tic_tac_toe_col_model.joblib')
            feature_names_path = os.path.join(model_dir, 'feature_names.joblib')
            tf_model_path = os.path.join(model_dir, 'tic_tac_toe_tf_model.keras')

            # Load the Scikit-learn models from their joblib files
            try:
                self.row_model = joblib.load(row_model_path)
                self.col_model = joblib.load(col_model_path)
                self.feature_names = joblib.load(feature_names_path)
            except FileNotFoundError as e:
                print(f"Error loading Scikit-learn models. Check the path: {e}")
                self.row_model = None
                self.col_model = None
                self.feature_names = None

            # Load the TensorFlow model
            try:
                self.tf_model = load_model(tf_model_path)
            except FileNotFoundError as e:
                print(f"Error loading TensorFlow model. Check the path: {e}")
                self.tf_model = None

        # Map difficulty levels to their respective move-getting methods
        self.move_strategies = {
            DifficultyLevel.Easy: self.get_random_move,
            DifficultyLevel.Medium: self.get_ai_move_sk,  # Using the higher-performing model
            DifficultyLevel.Hard: self.get_best_move
        }

    def get_opposing_symbol(self, symbol: CellState) -> CellState:
        return CellState.X if symbol == CellState.O else CellState.O

    def board_to_features(self, board: List[List[CellState]]) -> List[int]:
        """Converts the 3x3 board to a 9-element feature vector."""
        features = []
        for row in board:
            for cell in row:
                if cell == CellState.X:
                    features.append(1)
                elif cell == CellState.O:
                    features.append(-1)
                else:
                    features.append(0)
        return features

    def parse_board_from_json(self, raw_board: List) -> List[List[CellState]]:
        """
        Parses a raw list representation of the board (from JSON)
        into the CellState enum format.
        """
        parsed_board = []
        for row in raw_board:
            parsed_row = []
            for cell_value in row:
                if cell_value is None:
                    parsed_row.append(CellState.Empty)
                else:
                    # CellState(cell_value) will convert 'X' or 'O' string to CellState.X or CellState.O
                    parsed_row.append(CellState(cell_value))
            parsed_board.append(parsed_row)
        return parsed_board

    def get_computer_move(self, board: List[List[CellState]], difficulty_level: DifficultyLevel, ai_symbol: CellState) -> Tuple[int, int]:
        # if difficulty_level == DifficultyLevel.Easy:
        #     return self.get_random_move(board)
        # elif difficulty_level == DifficultyLevel.Medium:
        #     return self.get_ai_move_sk(board)
        # elif difficulty_level == DifficultyLevel.Hard:
        #     return self.get_best_move(board, ai_symbol)
        # return (-1, -1)

        # Use the dictionary to find the correct method and call it.

        # The get() method is used to safely handle cases where a key might not exist.
        # It will return None, which you can then handle.
        move_function = self.move_strategies.get(difficulty_level)

        if move_function:
            if move_function == self.get_best_move:
                # The 'Hard' difficulty requires the ai_symbol argument
                return move_function(board, ai_symbol)
            else:
                # Other difficulties just need the board
                return move_function(board)
    
        # Return a default error or random move if the difficulty isn't recognized
        return self.get_random_move(board)

    def get_random_move(self, board: List[List[CellState]]) -> Tuple[int, int]:
        """
        Determines the difficulty easy move for the computer picking a random empty cell.
        """
        empty_cells = []
        for row in range(3):
            for col in range(3):
                if board[row][col] == CellState.Empty:
                    empty_cells.append((row, col))
    
        # Pick a random empty cell
        if empty_cells:
            return random.choice(empty_cells)

        # No empty cells
        return (-1, -1)

    def get_ai_move_sk(self, board: List[List[CellState]]) -> Tuple[int, int]:
        """
        Predicts the medium difficulty move using the saved Scikit-learn models.
        """
        # Test if the Scikit-learn models are loaded
        if not self.row_model or not self.col_model:
            return (-1, -1)
    
        # Convert the current board state into a feature vector
        features = self.board_to_features(board)
    
        # The models expect a 2D array, so we reshape the single feature vector
        # input_data = np.array(features).reshape(1, -1)

        # Convert the feature vector into a pandas DataFrame
        input_data = pd.DataFrame([features], columns=self.feature_names)
    
        # Predict the row and column
        predicted_row = int(self.row_model.predict(input_data)[0])
        predicted_col = int(self.col_model.predict(input_data)[0])
    
        return (predicted_row, predicted_col)

    def get_ai_move_tf(self, board: List[List[CellState]]) -> Tuple[int, int]:
        """
        Predicts the medium difficulty move using the saved TensorFlow model.
        """
        # Test if the TensorFlow model is loaded
        if not self.tf_model:
            return (-1, -1)

        # Convert the current board state into a feature vector
        features = self.board_to_features(board)
    
        # The model expects a 2D array, so we reshape the single feature vector
        input_data = np.array(features).reshape(1, -1)
    
        # Make a prediction. The result is an array of predicted values.
        # We round the results as they are continuous values from a linear activation.
        predicted_coords = self.tf_model.predict(input_data, verbose=0)[0]
        predicted_row = int(round(predicted_coords[0]))
        predicted_col = int(round(predicted_coords[1]))
    
        # Clamp the values to be within the board boundaries (0, 1, 2)
        predicted_row = np.clip(predicted_row, 0, 2)
        predicted_col = np.clip(predicted_col, 0, 2)

        return (predicted_row, predicted_col)

    def get_best_move(self, board: List[List[CellState]], ai_symbol: CellState) -> Tuple[int, int]:
        """
        Determines the difficulty hard move for the computer using the Minimax algorithm.
        Prioritizes a winning move, then a blocking move.
        """
        if self.is_board_empty(board):
            return (1, 1)
        
        human_symbol = self.get_opposing_symbol(ai_symbol)

        best_score = -math.inf
        best_moves = [] # A list to store all moves with the best score

        for row in range(3):
            for col in range(3):
                if board[row][col] == CellState.Empty:
                    board[row][col] = ai_symbol
                
                    # Check for an immediate winning move (a quick optimization)
                    if self.check_win(board, ai_symbol):
                        board[row][col] = CellState.Empty
                        return (row, col)

                    score = self.minimax(board, 0, False, ai_symbol)
                    board[row][col] = CellState.Empty

                    if score > best_score:
                        best_score = score
                        best_moves = [(row, col)] # Start a new list of best moves
                    elif score == best_score:
                        best_moves.append((row, col)) # Add to the list

        # Tie-breaking logic
        # If there's only one best move, return it
        if len(best_moves) == 1:
            return best_moves[0]
    
        # If there are multiple best moves (e.g., all leading to a draw)
        # Apply a heuristic to choose the "smartest" one.
        # The order below is a common strategy for Tic-Tac-Toe.
    
        # 1. Prioritize blocking an opponent's win
        # Loop through the best moves and see if any of them block a win
        for move in best_moves:
            temp_board = [row[:] for row in board]
            temp_board[move[0]][move[1]] = human_symbol
            # If this move *would have been* a winning move for the human,
            # it's a good blocking move.
            if self.check_win(temp_board, human_symbol):
                return move
    
        # 2. Prioritize the center square
        if (1, 1) in best_moves:
            return (1, 1)
        
        # 3. Prioritize corner squares
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        for move in best_moves:
            if move in corners:
                return move

        # 4. If all else fails, pick randomly from the remaining best moves
        if best_moves:
            return random.choice(best_moves)
       
        # 5. There were no remaining best moves
        return (-1, -1)

    def minimax(self, board: List[List[CellState]], depth: int, is_maximizing_player: bool, ai_symbol: CellState) -> int:
        human_symbol = self.get_opposing_symbol(ai_symbol)
    
        if self.check_win(board, ai_symbol):
            return 1
        if self.check_win(board, human_symbol):
            return -1
        if self.is_board_full(board):
            return 0

        if is_maximizing_player:
            best_score = -math.inf
            for row in range(3):
                for col in range(3):
                    if board[row][col] == CellState.Empty:
                        board[row][col] = ai_symbol
                        score = self.minimax(board, depth + 1, False, ai_symbol)
                        board[row][col] = CellState.Empty
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for row in range(3):
                for col in range(3):
                    if board[row][col] == CellState.Empty:
                        board[row][col] = human_symbol
                        score = self.minimax(board, depth + 1, True, ai_symbol)
                        board[row][col] = CellState.Empty
                        best_score = min(score, best_score)
            return best_score

    def check_win(self, board: List[List[CellState]], player: CellState) -> bool:
        # Check rows
        for row in range(3):
            if board[row][0] == player and board[row][1] == player and board[row][2] == player:
                return True
        # Check columns
        for col in range(3):
            if board[0][col] == player and board[1][col] == player and board[2][col] == player:
                return True
        # Check diagonals
        if board[0][0] == player and board[1][1] == player and board[2][2] == player:
            return True
        if board[0][2] == player and board[1][1] == player and board[2][0] == player:
            return True

        return False

    def is_board_empty(self, board: List[List[CellState]]) -> bool:
        for row in board:
            for cell in row:
                if cell != CellState.Empty:
                    return False
        return True

    def is_board_full(self, board: List[List[CellState]]) -> bool:
        for row in board:
            for cell in row:
                if cell == CellState.Empty:
                    return False
        return True

    def check_game_status(self, board: List[List[CellState]], ai_symbol: CellState) -> str:
        # Get the human player symbol
        human_symbol = self.get_opposing_symbol(ai_symbol)

        # Check if the AI player won
        if self.check_win(board, ai_symbol):
            return f'win-{ai_symbol.value}'

        # Check if the human player won
        if self.check_win(board, human_symbol):
            return f'win-{human_symbol.value}'
    
        # Check for a draw (if the board is full)
        if self.is_board_full(board):
            return 'draw'

        # If the game is not over, it's ongoing
        return 'ongoing'
