import java.awt.*;
import java.io.*;
import java.net.*;
import java.util.List;
import javax.swing.*;

public class StudentUI extends JFrame {

    public StudentUI() {
        setTitle("Student Interface");
        setSize(600, 600);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        StudentRadialPanel panel = new StudentRadialPanel();
        add(panel);

        new Thread(() -> listen(panel)).start();

        setVisible(true);
    }

    private void listen(StudentRadialPanel panel) {
        try (ServerSocket server = new ServerSocket(6002)) {
            Socket socket = server.accept();
            BufferedReader in =
                    new BufferedReader(new InputStreamReader(socket.getInputStream()));

            String line;
            while ((line = in.readLine()) != null) {
                if (line.startsWith("QUESTION")) {
                    panel.setQuestion(line.substring(9));
                }
                if (line.startsWith("HIGHLIGHT")) {
                    panel.setHighlighted(Integer.parseInt(line.split(":")[1]));
                }
                if (line.startsWith("CONFIRM")) {
                    panel.confirm();
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(StudentUI::new);
    }
}

class StudentRadialPanel extends JPanel {

    private static final int START_ANGLE = 90;

    private final List<String> answers = List.of("4", "5", "6");
    private String question = "2 + 3 = ?";
    private int highlighted = 0;
    private boolean locked = false;

    public void setQuestion(String q) {
        question = q;
        repaint();
    }

    public void setHighlighted(int idx) {
        if (!locked) {
            highlighted = idx;
            repaint();
        }
    }

    public void confirm() {
        locked = true;
        repaint();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING,
                            RenderingHints.VALUE_ANTIALIAS_ON);

        int size = Math.min(getWidth(), getHeight()) - 120;
        int x = (getWidth() - size) / 2;
        int y = (getHeight() - size) / 2;
        int slice = 360 / answers.size();

        for (int i = 0; i < answers.size(); i++) {
            int start = START_ANGLE - i * slice;
            g2.setColor(
                locked && i == highlighted ? Color.GREEN :
                i == highlighted ? Color.ORANGE :
                Color.LIGHT_GRAY
            );
            g2.fillArc(x, y, size, size, start, -slice);
        }

        drawText(g2, size, slice);
    }

    private void drawText(Graphics2D g2, int size, int slice) {
        int cx = getWidth() / 2;
        int cy = getHeight() / 2;

        g2.setFont(new Font("SansSerif", Font.BOLD, 20));
        drawCentered(g2, question, cx, cy);

        g2.setFont(new Font("SansSerif", Font.BOLD, 16));
        int r = size / 2 - 30;

        for (int i = 0; i < answers.size(); i++) {
            double ang = Math.toRadians(START_ANGLE - (i + 0.5) * slice);
            int tx = cx + (int)(r * Math.cos(ang));
            int ty = cy - (int)(r * Math.sin(ang));
            drawCentered(g2, answers.get(i), tx, ty);
        }
    }

    private void drawCentered(Graphics2D g2, String t, int x, int y) {
        FontMetrics fm = g2.getFontMetrics();
        g2.drawString(t, x - fm.stringWidth(t)/2, y + fm.getAscent()/2);
    }
}
