import java.awt.*;
import javax.swing.*;

public class EvaluationReport extends JFrame {

    public EvaluationReport(String text) {
        setTitle("Evaluation Report");
        setSize(400, 250);
        setLocationRelativeTo(null);
        setDefaultCloseOperation(EXIT_ON_CLOSE);

        JLabel label = new JLabel(text, SwingConstants.CENTER);
        label.setFont(new Font("SansSerif", Font.BOLD, 18));

        add(label);
        setVisible(true);
    }
}
