import java.awt.*;
import java.util.List;
import javax.swing.*;

public class StudentRadialPanel extends JPanel {

    private static final int START_ANGLE = 90;
    private static final Color BASE = new Color(220, 220, 220);
    private static final Color HIGHLIGHT = new Color(255, 180, 90);

    private final String question = "2 + 3 = ?";
    private final List<String> answers =
            List.of("4", "5", "6");

    private int highlightedIndex = 0;

    public StudentRadialPanel() {
        setBackground(Color.WHITE);

        // DEMO rotation (replace with TUIO later)
        new Timer(800, e -> {
            highlightedIndex =
                    (highlightedIndex + 1) % answers.size();
            repaint();
        }).start();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;
        g2.setRenderingHint(
                RenderingHints.KEY_ANTIALIASING,
                RenderingHints.VALUE_ANTIALIAS_ON
        );

        int size = Math.min(getWidth(), getHeight()) - 100;
        int x = (getWidth() - size) / 2;
        int y = (getHeight() - size) / 2;

        int slices = answers.size();
        int sliceAngle = 360 / slices;

        // Draw wedges
        for (int i = 0; i < slices; i++) {
            int start = START_ANGLE - i * sliceAngle;
            g2.setColor(i == highlightedIndex ? HIGHLIGHT : BASE);
            g2.fillArc(x, y, size, size, start, -sliceAngle);
        }

        // Inner circle
        int inner = size / 2;
        int ix = x + size / 4;
        int iy = y + size / 4;
        g2.setColor(Color.WHITE);
        g2.fillOval(ix, iy, inner, inner);

        // Question text
        g2.setColor(Color.BLACK);
        g2.setFont(new Font("SansSerif", Font.BOLD, 18));
        drawCentered(g2, question,
                getWidth() / 2, getHeight() / 2);

        // Answer labels
        int cx = getWidth() / 2;
        int cy = getHeight() / 2;
        int r = size / 2 - 30;

        g2.setFont(new Font("SansSerif", Font.BOLD, 14));

        for (int i = 0; i < slices; i++) {
            double angle = Math.toRadians(
                    START_ANGLE - (i + 0.5) * sliceAngle
            );

            int tx = cx + (int) (r * Math.cos(angle));
            int ty = cy - (int) (r * Math.sin(angle));

            drawCentered(g2, answers.get(i), tx, ty);
        }
    }

    private void drawCentered(Graphics2D g2,
                              String text, int x, int y) {
        FontMetrics fm = g2.getFontMetrics();
        g2.drawString(text,
                x - fm.stringWidth(text) / 2,
                y + fm.getAscent() / 2);
    }
}
