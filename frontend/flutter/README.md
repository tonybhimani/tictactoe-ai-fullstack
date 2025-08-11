# 📱 Tic-Tac-Toe – Flutter Frontend

This is the Flutter-based frontend for the Tic-Tac-Toe game. It's built in **Flutter 3.32.8** and communicates with the Flask backend via a RESTful API. The app has been **built and tested for Android**, and also works on web and desktop.

---

## 🧩 Features

- **Interactive game board** using a `Stack` with an `Image` (board) and `GridView` (cells) overlayed in a 3×3 layout
- **Tap-to-play** — Each cell is wrapped in a GestureDetector; the onTap callback triggers \_onCellTapped, which updates the board with the player's symbol, calls the backend for the AI move, and updates with the computer's symbol
- **End-of-game dialogs** — uses `AlertDialog` to show win, draw, or loss messages
- **Exact board alignment** — removed all padding and disabled scrolling to make the grid sit perfectly over the board image
- **Responsive layout** for multiple screen sizes
- Built and tested for **Android** deployment

---

## 📁 Project Structure

```
frontend/flutter
├── lib/
│   ├── main.dart                # Entry point of the Flutter app
│   ├── screens/
│   │   └── game_screen.dart     # UI layout and interaction logic
│   ├── services/
│   │   └── tictactoe_game.dart  # Game logic and API interaction
│   ├── utils/
│   │   └── constants.dart       # API base URL and other constants
├── assets/                      # Game board and symbol images
├── pubspec.yaml                 # Dependencies and metadata
└── README.md                    # This file
```

---

## 🧰 Development Environment

Built and tested using:

```text
Flutter 3.32.8 • channel stable • https://github.com/flutter/flutter.git
Framework • revision edada7c56e (2 weeks ago) • 2025-07-25 14:08:03 +0000
Engine • revision ef0cd00091 (2 weeks ago) • 2025-07-24 12:23:50 -0700
Tools • Dart 3.8.1 • DevTools 2.45.1
```

---

## 🚀 Setup & Running

Make sure Flutter is installed and working:

```bash
flutter doctor
```

Install dependencies:

```bash
flutter pub get
```

Run on a chosen device:

```bash
flutter run -d chrome   # Web
flutter run -d windows  # Desktop
```

---

### 📱 Running on Android

You can run the app directly on an Android device or emulator without building a signed APK:

1. **Check connected devices/emulators**

   ```bash
   adb devices
   ```

   This lists available devices. Copy the device ID of your phone or emulator.

2. **Run on a physical device**

   ```bash
   flutter run -d <device-id>
   ```

   _(USB debugging must be enabled on the phone.)_

3. **Run on an emulator**

   ```bash
   flutter run -d emulator-5554
   ```

   Replace `emulator-5554` with the ID from `adb devices`.

---

### 🎯 UI Alignment Notes

Positioning the `GridView` exactly over the game board image was the most challenging layout task.
The fix was to remove all padding and disable scrolling:

```dart
GridView.builder(
  padding: EdgeInsets.zero, // Removes extra spacing around grid
  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
    crossAxisCount: 3,
  ),
  itemCount: 9,
  physics: NeverScrollableScrollPhysics(), // Prevents drag-induced misalignment
  itemBuilder: (BuildContext context, int index) {
    // Cell builder logic
  },
)
```

Without these properties, the grid would shift slightly due to default padding and scroll physics, breaking the visual alignment with the board image.

---

## 📝 Additional Notes

- The game board UI uses a **GridView** with `padding: EdgeInsets.zero` and `physics: NeverScrollableScrollPhysics()` to perfectly overlay the 3x3 grid on top of the board image without any unwanted spacing or scrolling.

- Each grid cell is wrapped in a **GestureDetector** that listens for taps and disables input while the computer is thinking (loading state).

- A **loading spinner overlay** appears during the computer's move to indicate processing and prevent further user input until the move is complete.

- The app automatically selects the correct backend API URL based on the running platform (Android emulator, iOS, web, desktop) to simplify configuration and testing.

- The Flutter app was built and tested on **Android physical devices and emulators** using `flutter run -d <device_id>`. No production APK build or key signing was performed.
