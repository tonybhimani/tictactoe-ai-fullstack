import sys
import os
from flask import Flask, Blueprint, jsonify, request, send_from_directory
from flask_cors import CORS

current_dir = os.path.dirname(os.path.abspath(__file__))

if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import the Tic-Tac-Toe Game
from game.tictactoe import TicTacToeGame, CellState, DifficultyLevel

# Initialize an instance of the game (so trained models load once)
tic_tac_toe_game = TicTacToeGame()

# Initialize CORS before anything else
cors = CORS()

# Create the app and blueprint
app = Flask(__name__)
bp = Blueprint('api', __name__)

# CORS initialization and route definitions
cors.init_app(app)

# --- ENDPOINTS ---

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@bp.route('/get_computer_move', methods=['POST'])
def get_computer_move():
    try:
        # Use request.get_json() to parse incoming JSON data
        request_data = request.get_json()
        if not request_data:
            return jsonify({'success': False, 'message': 'Request must be JSON'}), 400

        # Get the board, computer symbol, and difficulty level
        board_data = request_data.get('board')
        computer_symbol_str = request_data.get('computer_symbol')
        difficulty_str = request_data.get('difficulty_level', 'Easy')

        # Validate board data
        if not board_data or not isinstance(board_data, list):
            return jsonify({'success': False, 'message': 'Missing or invalid board data'}), 400

        # Validate computer symbol
        try:
            computer_symbol = CellState(computer_symbol_str)
        except ValueError:
            return jsonify({'success': False, 'message': 'Missing or invalid computer symbol'}), 400

        # Validate and convert difficulty level
        try:
            difficulty_level = DifficultyLevel(difficulty_str)
        except ValueError:
            return jsonify({'success': False, 'message': 'Invalid difficulty level'}), 400

        # Parse the JSON board into the Enum friendly version
        parsed_board = tic_tac_toe_game.parse_board_from_json(board_data)

        # Pre-computer move game check
        game_status = tic_tac_toe_game.check_game_status(parsed_board, computer_symbol)
        response_board = [list(row) for row in board_data]
        next_move = (-1, -1)

        # Only get a computer move if the game is still ongoing
        if game_status == "ongoing":
            # Get the computer's next move based on the board
            next_move = tic_tac_toe_game.get_computer_move(parsed_board, difficulty_level, computer_symbol)

            # Validation loop start here
            row, col = next_move

            # Continue looping until a valid, empty cell is found
            while parsed_board[row][col] != CellState.Empty:
                # Get a new move. In this case, a random valid one.
                next_move = tic_tac_toe_game.get_random_move(parsed_board)
                row, col = next_move

            # Update boards with computer's move
            response_board[row][col] = computer_symbol.value
            parsed_board[row][col] = computer_symbol
            
            # Post-computer move game check
            game_status = tic_tac_toe_game.check_game_status(parsed_board, computer_symbol)

        return jsonify({
            'success': True, 
            'board': response_board, 
            'computer_move': next_move, 
            'game_status': game_status
        }), 200
    except Exception as e:
        # Log the exception for debugging purposes
        app.logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return jsonify({'success': False, 'message': 'An internal server error occurred.'}), 500


# Register the blueprint AFTER all routes are defined
app.register_blueprint(bp, url_prefix='/api')

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)