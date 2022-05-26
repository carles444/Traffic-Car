package me.pablo.robotcontroller.gui;

import me.pablo.robotcontroller.model.Robot;
import me.pablo.robotcontroller.network.PacketConstants;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;

public class DirectionPanel extends JPanel implements KeyListener, ItemListener {

    private final Robot robot;
    private final JToggleButton forward, backward, left, right;

    public DirectionPanel() {
        this.robot = Robot.getInstance();
        this.setLayout(new GridBagLayout());

        this.forward = add(createButton("^"), 1, 0);
        this.backward = add(createButton("v"), 1, 2);
        this.left = add(createButton("<"), 0, 1);
        this.right = add(createButton(">"), 2, 1);
    }

    private <T extends Component> T add(T comp, int x, int y) {
        GridBagConstraints c = new GridBagConstraints();
        c.gridx = x;
        c.gridy = y;
        add(comp, c);
        return comp;
    }

    private JToggleButton createButton(String str) {
        JToggleButton b = new JToggleButton(str);
        b.setFocusable(false);
        b.setPreferredSize(new Dimension(50, 50));
        b.addItemListener(this);
        return b;
    }

    @Override
    public void keyTyped(KeyEvent e) {}

    @Override
    public void keyPressed(KeyEvent e) {
        JToggleButton btn = getButton(e.getKeyChar());
        if (btn != null) btn.setSelected(true);
    }

    @Override
    public void keyReleased(KeyEvent e) {
        JToggleButton btn = getButton(e.getKeyChar());
        if (btn != null) btn.setSelected(false);
    }

    @Override
    public void itemStateChanged(ItemEvent e) {
        int btnState = getButtonState();
        robot.setDirection(btnState);
    }

    public JToggleButton getButton(char keycode) {
        switch (keycode) {
            case 'w': return forward;
            case 'a': return left;
            case 'd': return right;
            case 's': return backward;
            default: return null;
        }
    }

    private int getButtonState() {
        return ((forward.isSelected() ? PacketConstants.FORWARD : 0) |
                (backward.isSelected() ? PacketConstants.BACKWARD : 0) |
                (left.isSelected() ? PacketConstants.LEFT : 0) |
                (right.isSelected() ? PacketConstants.RIGHT : 0));
    }

}
