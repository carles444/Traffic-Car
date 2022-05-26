package me.pablo.robotcontroller.gui;

import me.pablo.robotcontroller.model.Robot;

import javax.swing.*;
import java.awt.*;

public class MainFrame extends JFrame {

    private final Robot robot;
    private final DirectionPanel direction;
    private final JComboBox<Robot.State> mode;
    private final JLabel status, data;

    public MainFrame() {
        this.robot = Robot.getInstance();
        this.setLayout(new BoxLayout(getContentPane(), BoxLayout.Y_AXIS));

        this.status = new JLabel(robot.getStatus());
        this.data = new JLabel("-");
        this.status.setAlignmentX(Component.CENTER_ALIGNMENT);
        this.data.setAlignmentX(Component.CENTER_ALIGNMENT);

        this.direction = new DirectionPanel();

        this.mode = new JComboBox<>();
        for (Robot.State value : Robot.State.values()) mode.addItem(value);
        this.mode.setFocusable(false);
        this.mode.addActionListener(l -> {
            Robot.State rs = (Robot.State) this.mode.getSelectedItem();
            robot.setState(rs);
        });
        this.mode.setMaximumSize(new Dimension(130, 0));

        add(direction);
        add(mode);
        add(status);
        add(data);

        robot.addChangeListener(type -> {
            if (type.equals("status"))
                SwingUtilities.invokeLater(() -> this.status.setText(robot.getStatus()));
            else if (type.equals("direction"))
                data.setText("0x" + Integer.toString(robot.getDirection(), 16) +
                        " , 0b" + Integer.toString(robot.getDirection(), 2));
        });

        addKeyListener(direction);

        pack();
        setMinimumSize(getSize());
        setSize(getWidth() + 20, getHeight() + 20);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        setVisible(true);
    }

}
