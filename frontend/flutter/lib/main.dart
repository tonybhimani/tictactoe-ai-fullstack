import 'package:flutter/material.dart';
import 'package:tictactoe_app/screens/game_screen.dart';
// import 'package:flutter/rendering.dart'; // Commented out: Used for debugging layout, not needed for production

void main() {
  // debugPaintSizeEnabled = true; // Commented out: Used for debugging layout boundaries
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Tic-Tac-Toe App', // Application title
      theme: ThemeData(
        // Set a global white background for all Scaffolds
        scaffoldBackgroundColor: Colors.white,
        // Set a global font style with black text
        textTheme: const TextTheme(
          bodyLarge: TextStyle(color: Colors.black),
          bodyMedium: TextStyle(color: Colors.black),
        ),
        visualDensity: VisualDensity
            .adaptivePlatformDensity, // Adapts UI density based on platform
      ),
      home: const GameScreen(), // Sets GameScreen as the initial screen
      debugShowCheckedModeBanner:
          false, // Hides the debug banner in the top right corner
    );
  }
}
