import sys
import os
import csv
import random
from enum import Enum
from typing import List, Tuple

# --- Generate game data for model training ---

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

if project_root not in sys.path:
    sys.path.append(project_root)

from game.tictactoe import TicTacToeGame, CellState

def print_board(board):
    for row in board:
        print(" | ".join([cell.value if cell.value is not None else " " for cell in row]))
        print("-" * 9)

def board_to_features(board: List[List[CellState]]) -> List[int]:
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

def play_game_and_collect_data(minimax_ai: TicTacToeGame, ai_symbol: CellState) -> List[Tuple[List[int], Tuple[int, int]]]:
    """
    Plays a single game of Tic-Tac-Toe using the minimax AI against itself,
    with a chance of making a random move to increase data diversity.
    """
    board = [[CellState.Empty] * 3 for _ in range(3)]
    data = []

    current_player = CellState.X
    exploration_rate = 0.2  # 20% chance of making a random move

    while not minimax_ai.check_win(board, CellState.X) and \
          not minimax_ai.check_win(board, CellState.O) and \
          not minimax_ai.is_board_full(board):

        features = board_to_features(board)

        # Check if the AI should make a random move (exploration)
        if random.random() < exploration_rate:
            empty_cells = []
            for row in range(3):
                for col in range(3):
                    if board[row][col] == CellState.Empty:
                        empty_cells.append((row, col))

            if empty_cells:
                best_move = random.choice(empty_cells)
        else:
            # Otherwise, use the minimax algorithm to find the best move (exploitation)
            best_move = minimax_ai.get_best_move(board, ai_symbol)

        # Store the current board state and the move that was chosen
        if best_move != (-1, -1):
            data.append((features, best_move))

            # Make the move on the board
            row, col = best_move
            if current_player == CellState.X:
                board[row][col] = CellState.X
                current_player = CellState.O
            else:
                board[row][col] = CellState.O
                current_player = CellState.X

    return data

if __name__ == "__main__":
    minimax_ai = TicTacToeGame(load_models=False)

    all_games_data = []
    num_games = 10000  # Increase number of games for more data
    ai_symbol = CellState.X

    print(f"Playing {num_games} games to collect training data...")
    for i in range(num_games):
        # We need to make sure the AI symbols are consistent for data collection.
        # Let's say AI plays as 'X' and 'O' in alternating games to get a balanced dataset.
        if i % 2 == 0:
            ai_symbol = CellState.X
        else:
            ai_symbol = CellState.O
            
        game_data = play_game_and_collect_data(minimax_ai, ai_symbol)
        all_games_data.extend(game_data)

        if (i + 1) % 1000 == 0:
            print(f"  {i + 1} games played.")

    print(f"Data collection complete! Collected {len(all_games_data)} data points.")

    # Now, let's write the data to a CSV file
    raw_data_dir = os.path.join(project_root, 'data/raw')
    csv_file_path = os.path.join(raw_data_dir, 'tic_tac_toe_games.csv')

    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write the header row
        header = [f'board_{i}' for i in range(9)] + ['best_move_row', 'best_move_col']
        writer.writerow(header)

        # Write the data rows
        for features, best_move in all_games_data:
            row_to_write = features + list(best_move)
            writer.writerow(row_to_write)

    print(f"Data successfully exported to '{csv_file_path}'.")