import javax.swing.*;
import java.awt.*;
import java.util.List;

public class TeacherRadialPanel extends JPanel {

    private static final int START_ANGLE = 90;
    private static final Color BASE = new Color(220,220,220);
    private static final Color ACTIVE = new Color(255,180,90);
    private static final Color CONFIRMED = new Color(120,200,120);

    private final List<String> options =
            List.of("5–9", "10–14", "15–20");

    private int highlighted = 0;
    private boolean locked = false;

    public void setHighlightedIndex(int i) {
        if (!locked) {
            highlighted = i;
            repaint();
        }
    }

    public void confirmSelection() {
        locked = true;
        repaint();

        new Timer(800, e -> {
            JFrame top = (JFrame) SwingUtilities.getWindowAncestor(this);
            top.dispose();
            new EvaluationReport("Teacher selected: " + options.get(highlighted));
        }).start();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING,
                            RenderingHints.VALUE_ANTIALIAS_ON);

        int size = Math.min(getWidth(), getHeight()) - 100;
        int x = (getWidth() - size) / 2;
        int y = (getHeight() - size) / 2;
        int slice = 360 / options.size();

        for (int i = 0; i < options.size(); i++) {
            int start = START_ANGLE - i * slice;
            g2.setColor(
                locked && i == highlighted ? CONFIRMED :
                i == highlighted ? ACTIVE : BASE
            );
            g2.fillArc(x, y, size, size, start, -slice);
        }

        drawLabels(g2, size, slice);
    }

    private void drawLabels(Graphics2D g2, int size, int slice) {
        int cx = getWidth() / 2;
        int cy = getHeight() / 2;
        int r = size / 2 - 30;
        g2.setFont(new Font("SansSerif", Font.BOLD, 14));

        for (int i = 0; i < options.size(); i++) {
            double ang = Math.toRadians(START_ANGLE - (i + 0.5) * slice);
            int tx = cx + (int)(r * Math.cos(ang));
            int ty = cy - (int)(r * Math.sin(ang));
            drawCentered(g2, options.get(i), tx, ty);
        }
    }

    private void drawCentered(Graphics2D g2, String t, int x, int y) {
        FontMetrics fm = g2.getFontMetrics();
        g2.drawString(t, x - fm.stringWidth(t)/2, y + fm.getAscent()/2);
    }
}
