using System;
using System.Collections;
using System.Collections.Generic; // For List
using System.Linq;
using Newtonsoft.Json;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;

public enum CellState
{
	Empty,
	X,
	O
}

public enum DifficultyLevel
{
	Easy,
	Medium,
	Hard
}

// Class to serialize game data
[System.Serializable]
public class GameData
{
	public string[][] board;
	public string computer_symbol;
	public string difficulty_level;
}

// Class to deserialize API response
[System.Serializable]
public class ApiResponse
{
	public bool success;
	public string[][] board;
	public int[] computer_move;
	public string game_status;
}

// Class to deserial API error response
[System.Serializable]
public class ErrorResponse
{
	public bool success;
	public string message;
}

public class TicTacToe : MonoBehaviour
{
	private string apiUrl = "http://127.0.0.1:5000/api/get_computer_move";

	private CellState[,] boardData = new CellState[3, 3];

	private CellState humanSymbol = CellState.O;
	private CellState computerSymbol = CellState.X;

	private DifficultyLevel difficultyLevel = DifficultyLevel.Easy;

	private bool gameActive = true;

	private UIManager uiManager;

	public GameObject boardCellPrefab;
	public Transform boardCellParent;

	private BoardCell[,] uiBoardCells;

	[SerializeField] private Dropdown difficultyDropdown;
	[SerializeField] private Button resetButton;

	private void Awake()
	{
		// Find the UI Manager script
		uiManager = FindObjectOfType<UIManager>();
		if (uiManager == null)
		{
			Debug.LogError("UIManager Tester: UIManager script not found in the scene.");
			enabled = false;
			return;
		}

		// Populate the Difficulty dropdown
		if (difficultyDropdown != null)
		{
			difficultyDropdown.ClearOptions();
			List<string> difficultyLevels = Enum.GetNames(typeof(DifficultyLevel)).ToList();
			difficultyDropdown.AddOptions(difficultyLevels);
		}

		// Set up the UI handlers and game board 
		AddUIListeners();
		InitializeBoardUI();
	}

	private void OnDestroy()
	{
		RemoveUIListeners();
	}

	public bool IsGameActive()
	{
		return this.gameActive;
	}

	public CellState GetHumanSymbol()
	{
		return this.humanSymbol;
	}

	private void InitializeBoardUI()
	{
		uiBoardCells = new BoardCell[3, 3];

		for (int row = 0; row < 3; row++)
		{
			for (int col = 0; col < 3; col++)
			{
				GameObject boardCellGO = Instantiate(boardCellPrefab, boardCellParent);
				BoardCell boardCell = boardCellGO.GetComponent<BoardCell>();

				if (boardCell != null)
				{
					boardCell.Initialize(row, col, this);
					uiBoardCells[row, col] = boardCell;
				}
				else
				{
					// Log an error if the prefab is missing the script
					Debug.LogError("BoardCell Prefab is missing the BoardCell script!");
				}
			}
		}

		ClearGameBoard();
	}

	private void AddUIListeners()
	{
		if (difficultyDropdown != null) difficultyDropdown.onValueChanged.AddListener(OnDifficultyChanged);
		if (resetButton != null) resetButton.onClick.AddListener(OnResetGameButtonClicked);
	}

	private void RemoveUIListeners()
	{
		if (difficultyDropdown != null) difficultyDropdown.onValueChanged.RemoveListener(OnDifficultyChanged);
		if (resetButton != null) resetButton.onClick.RemoveListener(OnResetGameButtonClicked);		
	}

	/* Example: how to render the entire game board
	private void Render()
	{
		for (int row = 0; row < 3; row++)
		{
			for (int col = 0; col < 3; col++)
			{
				CellState symbol = this.boardData[row, col];
				this.uiBoardCells[row, col].ClearState();
				if (symbol != CellState.Empty)
				{
					this.uiBoardCells[row, col].SetState(symbol);
				}
			}
		}
	}
	*/

	public void HandleGameBoardClick(int row, int col)
	{
		if (!this.gameActive) return;
		this.boardData[row, col] = this.humanSymbol;
		this.uiBoardCells[row, col].SetState(this.humanSymbol);
		StartCoroutine(GetComputerMove());
	}

	public void ClearGameBoard()
	{
		this.gameActive = true;
		
		for (int row = 0; row < 3; row++)
		{
			for (int col = 0; col < 3; col++)
			{
				this.boardData[row, col] = CellState.Empty;
				this.uiBoardCells[row, col].ClearState();
			}
		}
	}

	private string[][] ParseBoardData()
	{
		string[][] parsedBoard = new string[3][];
		for (int row = 0; row < 3; row++)
		{
			parsedBoard[row] = new string[3];
			for (int col = 0; col < 3; col++)
			{
				parsedBoard[row][col] = this.boardData[row, col] == CellState.Empty ? null : this.boardData[row, col].ToString();
			}
		}
		return parsedBoard;
	}

	private void PrintGameData()
	{
		string[][] board = ParseBoardData();
		GameData gameData = new GameData();
		gameData.board = board;
		string json = JsonConvert.SerializeObject(gameData);
		Debug.Log("Board Data: " + json);
	}

	private void OnDifficultyChanged(int newIndex)
	{
		this.difficultyLevel = (DifficultyLevel)newIndex;
	}

	private void OnResetGameButtonClicked()
	{
		ClearGameBoard();
	}

	private IEnumerator GetComputerMove()
	{
		// Show UI spinner overlay
		uiManager.ShowLoadingSpinner();

		GameData gameData = new GameData();
		gameData.board = ParseBoardData();
		gameData.computer_symbol = this.computerSymbol.ToString();
		gameData.difficulty_level = this.difficultyLevel.ToString();

		// Serialize the C# object to a JSON string
		string jsonBody = JsonConvert.SerializeObject(gameData);

		// Convert the JSON string to a byte array
		byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(jsonBody);

		// Create a UnityWebRequest object for POST
		UnityWebRequest request = new UnityWebRequest(this.apiUrl, "POST");

		// Attach the raw body data to the request's upload handler
		request.uploadHandler = (UploadHandler)new UploadHandlerRaw(bodyRaw);

		// Set a download handler to receive the server's response
		request.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();

		// Set the Content-Type header to indicate JSON data
		request.SetRequestHeader("Content-Type", "application/json");

		// Sets a 2-second timeout
		request.timeout = 2;

		// Send the request and wait for a response
		yield return request.SendWebRequest();

		// Check for errors
		if (request.result == UnityWebRequest.Result.ConnectionError || request.result == UnityWebRequest.Result.ProtocolError)
		{
			Debug.LogError("Error: " + request.error);
			this.gameActive = false;
			// Show a user-friendly error message
			uiManager.ShowDialog("An error occurred. Please try resetting the game.");
		}
		else
		{
			// Check for HTTP success status codes (e.g., 200, 201, 204)
			if (request.responseCode >= 200 && request.responseCode < 300)
			{
				Debug.Log("Response received: " + request.downloadHandler.text);

				// Response is a success, deserialize to ApiResponse class
				string jsonResponse = request.downloadHandler.text;
				ApiResponse apiResponse = JsonConvert.DeserializeObject<ApiResponse>(jsonResponse);

				// Update the board data from the response
				int row = apiResponse.computer_move[0];
				int col = apiResponse.computer_move[1];
				if (row != -1 && col != -1)
				{
					this.boardData[row, col] = this.computerSymbol;
					this.uiBoardCells[row, col].SetState(this.computerSymbol);
				}

				// If the game isn't ongoing, display the message
				if (apiResponse.game_status != "ongoing") 
				{
					this.gameActive = false;
					switch (apiResponse.game_status)
					{
						case "win-O":
							uiManager.ShowDialog("You Won!");
							break;
						case "win-X":
							uiManager.ShowDialog("You lost!");
							break;
						case "draw":
							uiManager.ShowDialog("It's a draw!");
							break;
					}
				}
			}
			else // The API responded with a non-200 status code but no network error
			{
				// Deserialize to a specific ErrorResponse class if the API provides a structured error
				string jsonResponse = request.downloadHandler.text;
				ErrorResponse error = JsonUtility.FromJson<ErrorResponse>(jsonResponse);
				Debug.LogError("API Error: " + error.message);
				this.gameActive = false;
				// Show a user-friendly error message
				uiManager.ShowDialog("API Error: " + error.message);
			}
		}

		// Hide UI spinner overlay
		uiManager.HideLoadingSpinner();
	}
}
