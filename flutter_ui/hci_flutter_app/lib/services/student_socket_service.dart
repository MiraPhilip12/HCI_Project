import 'dart:convert';
import 'dart:io';

class StudentSocketService {
  static const String host = '127.0.0.1';
  static const int port = 51000;

  late Socket _socket;

  Stream<Map<String, dynamic>> connect() async* {
    _socket = await Socket.connect(host, port);
    print('[STUDENT UI] Connected to backend');

    await for (final line in _socket
        .cast<List<int>>()
        .transform(utf8.decoder)
        .transform(const LineSplitter())) {
      try {
        yield jsonDecode(line) as Map<String, dynamic>;
      } catch (e) {
        print('[STUDENT UI] Invalid JSON received: $line');
      }
    }
  }

  void dispose() {
    _socket.close();
  }
}
