import 'package:flutter/material.dart';
import '../services/student_socket_service.dart';

class StudentScreen extends StatefulWidget {
  const StudentScreen({super.key});

  @override
  State<StudentScreen> createState() => _StudentScreenState();
}

class _StudentScreenState extends State<StudentScreen> {
  final StudentSocketService _service = StudentSocketService();

  Map<String, dynamic>? _state;

  @override
  void initState() {
    super.initState();
    _service.connect().listen((data) {
      setState(() {
        _state = data;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_state == null) {
      return const Scaffold(
        body: Center(
          child: Text(
            'Waiting for teacher to start test...\n\nUse tangible markers to answer.',
            textAlign: TextAlign.center,
            style: TextStyle(fontSize: 22),
          ),
        ),
      );
    }

    return Scaffold(
      appBar: AppBar(title: const Text('Student')),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          children: [
            Text(
              _state!['question'] ?? '',
              style: const TextStyle(fontSize: 26),
            ),
            const SizedBox(height: 40),
            for (final option in _state!['options'] ?? [])
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 8),
                child: Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Colors.grey.shade300),
                  ),
                  child: Text(
                    option,
                    textAlign: TextAlign.center,
                    style: const TextStyle(fontSize: 20),
                  ),
                ),
              ),
            const Spacer(),
            if (_state!['feedback'] != null)
              Text(
                _state!['feedback'],
                style: const TextStyle(
                  fontSize: 22,
                  color: Colors.green,
                ),
              ),
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    _service.dispose();
    super.dispose();
  }
}
