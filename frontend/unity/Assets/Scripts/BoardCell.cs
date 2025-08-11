using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;

public class BoardCell : MonoBehaviour, IPointerClickHandler
{
	private TicTacToe gameManager;
	private int rowIndex, colIndex;
	private CellState humanSymbol;

	[SerializeField] private Sprite spriteX;
	[SerializeField] private Sprite spriteO;

	[SerializeField] private Image cellImage;	

	private CellState cellState = CellState.Empty;

	public void Initialize(int row, int col, TicTacToe gameManager)
	{
		this.rowIndex = row;
		this.colIndex = col;
		this.gameManager = gameManager;
		this.humanSymbol = gameManager.GetHumanSymbol();
	}

	public void OnPointerClick(PointerEventData eventData)
	{
		if (gameManager != null && gameManager.IsGameActive() && this.cellState == CellState.Empty)
		{
			SetState(this.humanSymbol);
			gameManager.HandleGameBoardClick(this.rowIndex, this.colIndex);
		}
	}

	public CellState GetState()
	{
		return this.cellState;
	}

	public void SetState(CellState symbol)
	{
		if (this.cellState == CellState.Empty)
		{
			this.cellState = symbol;
			this.cellImage.sprite = symbol == CellState.X ? spriteX : spriteO;
		}
	}

	public void ClearState()
	{
		this.cellState = CellState.Empty;
		this.cellImage.sprite = null;
	}
}
