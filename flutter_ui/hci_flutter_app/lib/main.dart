import 'package:flutter/material.dart';

import 'screens/role_selection_screen.dart';
import 'screens/teacher_screen.dart';
import 'screens/student_screen.dart';

void main() {
  runApp(const HCITangibleApp());
}

class HCITangibleApp extends StatelessWidget {
  const HCITangibleApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'HCI Tangible Learning',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        scaffoldBackgroundColor: const Color(0xFFFFF7FB),
        colorSchemeSeed: Colors.deepPurple,
      ),
      initialRoute: '/',
      routes: {
        '/': (context) => const RoleSelectionScreen(),
        '/teacher': (context) => const TeacherScreen(),
        '/student': (context) => const StudentScreen(),
      },
    );
  }
}
