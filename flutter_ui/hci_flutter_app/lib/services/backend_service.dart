import 'dart:io';

class BackendService {
  static const String host = '127.0.0.1';
  static const int port = 5007; // teacher → student logic

  static Future<void> sendTeacherConfig({
    required String ageGroup,
    required String subject,
  }) async {
    try {
      final socket = await Socket.connect(host, port);

      socket.writeln("AGE:$ageGroup");
      socket.writeln("SUBJECT:$subject");
      socket.writeln("START");

      await socket.flush();
      socket.close();
    } catch (e) {
      print("Backend connection error: $e");
    }
  }
}
