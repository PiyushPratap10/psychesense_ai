import 'package:flutter/material.dart';
import 'dart:async';
import 'home_screen.dart';
import 'splash_screen.dart';

class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Home")),
      body: Center(child: Text("This is the Home Screen")),
    );
  }
}
