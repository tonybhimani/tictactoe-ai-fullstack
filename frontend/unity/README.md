# 🎮 Tic-Tac-Toe – Unity Frontend

This is the Unity-based frontend for the Tic-Tac-Toe game.
It uses **C# scripts** and Unity's scene system to render the game board, handle player interaction, and communicate with the Flask backend API for computer moves.

The project is designed for **quick setup in the Unity Editor**, and can be run either directly in-editor or built for platforms such as WebGL or desktop.

---

## 🧩 Features

- Interactive 2D board with clickable cells
- Real-time communication with the Flask backend API for AI moves
- Difficulty selection (Easy, Medium, Hard)
- Loading overlay with spinner during AI turn
- End-of-game dialog showing win, loss, or draw result
- Easy customization for sprites, board size, and UI

---

## 📁 Project Structure

```
frontend/unity
├── Assets/
│   ├── Prefabs/
│   │   └── BoardCell.prefab      # Single board cell prefab displaying X/O and handling clicks
│   ├── Scenes/
│   │   └── SampleScene.unity     # Main game scene
│   ├── Scripts/
│   │   ├── BoardCell.cs          # Controls a cell prefab and notifies the game manager on click
│   │   ├── TicTacToe.cs          # Game manager; tracks board state, turn logic, and API calls
│   │   └── UIManager.cs          # Manages overlay UI (loading spinner, game result dialog)
│   ├── Sprites/                  # Image assets for board, symbols, and spinner
├── Assets.zip                    # Zipped Assets folder for quick import into Unity
└── README.md                     # This file
```

---

## ⚠️ Unity Users — Read This First

Before opening the provided `Assets` folder in Unity, you **must** install the **Newtonsoft Json.NET** package.
If you skip this step, Unity will likely show a warning dialog and may open in **Safe Mode**.

**To install Newtonsoft Json.NET in Unity:**

1. Open Unity with any empty/new 2D project.
2. Go to **Window → Package Manager**.
3. Click the **+** dropdown → **Add package by name…**
4. Enter:

   ```
   com.unity.nuget.newtonsoft-json
   ```

5. Click **Add** — Unity will download and install the package.
6. Once installed, you can close this temporary project and proceed to copy the provided Assets folder (see below).

_For older Unity versions without “Add package by name,” manually edit `Packages/manifest.json`:_

```json
{
  "dependencies": {
    "com.unity.nuget.newtonsoft-json": "3.0.1"
  }
}
```

---

## 🚀 Setup & Running

Unity project files are too large for the repo — only the `Assets` folder is provided.
Follow these steps:

1. Create a new **Unity 2D project** and close Unity.
2. **(If you haven't already)** install Newtonsoft Json.NET (see “Unity Users — Read This First” above).
3. Navigate to your Unity project folder.
4. Delete the existing `Assets/` folder.
5. Copy the `Assets/` folder from this repo into your Unity project.
6. Reopen Unity — the project should now load with all settings and assets.
7. Press **▶ Play** in the Unity editor to start the game.

---

## 📌 Notes

- Default backend API endpoint is `http://127.0.0.1:5000/api/get_computer_move` — update in `TicTacToe.cs` if needed.
- The **`Assets.zip`** file contains the full `Assets/` folder for quick import into an empty Unity project.
- Can be built for **WebGL**, **Windows**, **macOS**, or **Linux** using Unity's build settings.
