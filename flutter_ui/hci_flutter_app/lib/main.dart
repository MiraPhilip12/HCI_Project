import 'package:flutter/material.dart';
import 'services/backend_service.dart';


void main() {
  runApp(const HCIApp());
}

class HCIApp extends StatelessWidget {
  const HCIApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'HCI Project',
      theme: ThemeData(primarySwatch: Colors.indigo),
      home: const HomeScreen(),
    );
  }
}

/* =========================
   HOME (Role Selection)
   ========================= */
class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Select Role")),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () {
                Navigator.push(context,
                    MaterialPageRoute(builder: (_) => const TeacherScreen()));
              },
              child: const Text("Teacher"),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                Navigator.push(context,
                    MaterialPageRoute(builder: (_) => const StudentScreen()));
              },
              child: const Text("Student"),
            ),
          ],
        ),
      ),
    );
  }
}

/* =========================
   TEACHER SCREEN
   ========================= */
class TeacherScreen extends StatefulWidget {
  const TeacherScreen({super.key});

  @override
  State<TeacherScreen> createState() => _TeacherScreenState();
}

class _TeacherScreenState extends State<TeacherScreen> {
  final List<String> ageGroups = ["5–9", "10–14", "15–20"];
  final List<String> subjects = ["Math", "Science", "English"];

  int ageIndex = 0;
  int subjectIndex = 0;

  void rotateAge(int direction) {
    setState(() {
      ageIndex = (ageIndex + direction) % ageGroups.length;
      if (ageIndex < 0) ageIndex = ageGroups.length - 1;
    });
  }

  void rotateSubject(int direction) {
    setState(() {
      subjectIndex = (subjectIndex + direction) % subjects.length;
      if (subjectIndex < 0) subjectIndex = subjects.length - 1;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Teacher Configuration")),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text(
              "Rotate to Select Age Group",
              style: TextStyle(fontSize: 20),
            ),
            const SizedBox(height: 10),

            RotationCard(
              label: ageGroups[ageIndex],
              onLeft: () => rotateAge(-1),
              onRight: () => rotateAge(1),
            ),

            const SizedBox(height: 40),

            const Text(
              "Rotate to Select Subject",
              style: TextStyle(fontSize: 20),
            ),
            const SizedBox(height: 10),

            RotationCard(
              label: subjects[subjectIndex],
              onLeft: () => rotateSubject(-1),
              onRight: () => rotateSubject(1),
            ),

            const SizedBox(height: 50),

            ElevatedButton(
              onPressed: () async {
                await BackendService.sendTeacherConfig(
                  ageGroup: ageGroups[ageIndex],
                  subject: subjects[subjectIndex],
                );

                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text(
                      "Sent to backend: ${ageGroups[ageIndex]} | ${subjects[subjectIndex]}",
                    ),
                  ),
                );
              },
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.all(16),
                textStyle: const TextStyle(fontSize: 18),
              ),
              child: const Text("Start Test"),
            ),
          ],
        ),
      ),
    );
  }
}

/* =========================
   ROTATION CARD WIDGET
   ========================= */
class RotationCard extends StatelessWidget {
  final String label;
  final VoidCallback onLeft;
  final VoidCallback onRight;

  const RotationCard({
    super.key,
    required this.label,
    required this.onLeft,
    required this.onRight,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            IconButton(
              icon: const Icon(Icons.rotate_left),
              onPressed: onLeft,
            ),
            Text(
              label,
              style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
            ),
            IconButton(
              icon: const Icon(Icons.rotate_right),
              onPressed: onRight,
            ),
          ],
        ),
      ),
    );
  }
}

/* =========================
   STUDENT SCREEN (unchanged)
   ========================= */
class StudentScreen extends StatefulWidget {
  const StudentScreen({super.key});

  @override
  State<StudentScreen> createState() => _StudentScreenState();
}

class _StudentScreenState extends State<StudentScreen> {
  String selectedAnswer = "";
  int score = 0;

  final String question = "2 + 3 = ?";
  final Map<String, String> answers = {
    "A": "4",
    "B": "5",
    "C": "6",
  };
  final String correctAnswer = "B";

  void selectAnswer(String answer) {
    setState(() {
      selectedAnswer = answer;
    });
  }

  void confirmAnswer() {
    setState(() {
      if (selectedAnswer == correctAnswer) {
        score++;
      }
      selectedAnswer = "";
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Student Test")),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text("Score: $score",
                textAlign: TextAlign.right,
                style:
                    const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 20),
            Card(
              elevation: 4,
              child: Padding(
                padding: const EdgeInsets.all(20),
                child: Text(question,
                    textAlign: TextAlign.center,
                    style: const TextStyle(
                        fontSize: 26, fontWeight: FontWeight.bold)),
              ),
            ),
            const SizedBox(height: 30),
            ...answers.entries.map((e) => Padding(
                  padding: const EdgeInsets.symmetric(vertical: 6),
                  child: GestureDetector(
                    onTap: () => selectAnswer(e.key),
                    child: Container(
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: selectedAnswer == e.key
                            ? Colors.indigo.shade200
                            : Colors.grey.shade200,
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Text("${e.key}) ${e.value}",
                          textAlign: TextAlign.center,
                          style: const TextStyle(fontSize: 22)),
                    ),
                  ),
                )),
            const Spacer(),
            ElevatedButton(
              onPressed: selectedAnswer.isEmpty ? null : confirmAnswer,
              child: const Text("Confirm Answer"),
            )
          ],
        ),
      ),
    );
  }
}
