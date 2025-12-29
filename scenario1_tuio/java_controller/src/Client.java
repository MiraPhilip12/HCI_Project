import java.io.*;
import java.net.Socket;

public class Client {
    public static void main(String[] args) {
        try {
            Socket socket = new Socket("127.0.0.1", 5005);

            PrintWriter out = new PrintWriter(
                socket.getOutputStream(), true);
            BufferedReader in = new BufferedReader(
                new InputStreamReader(socket.getInputStream()));

            out.println("TEST_FROM_JAVA");

            String response = in.readLine();
            System.out.println("SERVER: " + response);

            socket.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
