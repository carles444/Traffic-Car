package me.pablo.robotcontroller;

import com.formdev.flatlaf.FlatDarculaLaf;
import me.pablo.robotcontroller.gui.MainFrame;
import me.pablo.robotcontroller.network.BluetoothManager;

import javax.swing.*;
import java.io.IOException;

public class Main {

    public static void main(String[] args) {
        FlatDarculaLaf.setup();
        try {
            BluetoothManager.initialize();
        } catch (IOException e) {
            e.printStackTrace();
        }
        SwingUtilities.invokeLater(MainFrame::new);
    }
}
