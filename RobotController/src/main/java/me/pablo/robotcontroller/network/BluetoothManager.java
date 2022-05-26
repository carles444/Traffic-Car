package me.pablo.robotcontroller.network;


import com.intel.bluetooth.BluetoothConsts;
import me.pablo.robotcontroller.model.Robot;

import javax.bluetooth.DiscoveryAgent;
import javax.bluetooth.LocalDevice;
import javax.microedition.io.Connection;
import javax.microedition.io.Connector;
import javax.microedition.io.StreamConnection;
import javax.microedition.io.StreamConnectionNotifier;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.Objects;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.function.Consumer;

public class BluetoothManager implements Runnable {

    private static final String RP_ADDR = "DC:A6:32:AA:AA:E6"; // UNUSED
    private static final String HOST = "localhost";
    private static final int PORT = 5;
    private static BluetoothManager INSTANCE;

    public static void initialize() throws IOException {
        LocalDevice ld = LocalDevice.getLocalDevice();
        System.out.println("Local BT address: " + ld.getBluetoothAddress());
        ld.setDiscoverable(DiscoveryAgent.GIAC);

        if (INSTANCE != null) throw new IllegalStateException("Cannot initialize twice.");
        Thread t = new Thread(INSTANCE = new BluetoothManager(), "Bluetooth server thread");
        t.setDaemon(true);
        t.start();
    }

    private final StreamConnectionNotifier notifier;

    private final Robot robot;
    private final LinkedBlockingQueue<Byte> queue = new LinkedBlockingQueue<>();

    public BluetoothManager() throws IOException {
        Connection c = Connector.open(BluetoothConsts.PROTOCOL_SCHEME_RFCOMM + "://" + HOST + ":" + PORT);
        if (!(c instanceof StreamConnectionNotifier))
            throw new IllegalStateException("Didn't get a BT server!");
        this.notifier = (StreamConnectionNotifier) c;

        this.robot = Robot.getInstance();
        robot.addChangeListener(this::onRobotChange);
    }

    private void onRobotChange(String change) {
        switch (change) {
            case "state":
                BluetoothManager.sendData(Packet.SET_MODE, robot.getState());
                break;
            case "direction":
                BluetoothManager.sendData(Packet.MOVE, robot.getDirection());
                break;
        }
    }

    @Override
    public void run() {
        while (true) {
            try {
                robot.setStatus("Waiting for client...");
                StreamConnection conn = notifier.acceptAndOpen();
                robot.setStatus("Accepted connection!");

                handleConnection(conn);

                robot.setStatus("Connection finished.");
            } catch (IOException e) {
                robot.setStatus("Connection errored.");
                e.printStackTrace();
            }
            queue.clear();
        }
    }

    private void handleConnection(StreamConnection conn) throws IOException {
        try (InputStream is = conn.openInputStream();
             OutputStream os = conn.openOutputStream()) {
            queue.clear(); // make sure clear

            // initialize state
            BluetoothManager.sendData(Packet.SET_MODE, robot.getState());
            BluetoothManager.sendData(Packet.MOVE, robot.getDirection());

            // Send
            Byte currVal;
            while ((currVal = queue.poll()) != null) os.write(currVal);

            // Receive
            while (is.available() > 0) {
                System.out.println("Read: " + is.read());
            }

            Thread.sleep(10);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    public static void sendData(Packet p, MetadataProvider metadata) {
        sendData(p, metadata.metadata());
    }

    public static void sendData(Packet p, int metadata) {
        if (INSTANCE == null) return;
        INSTANCE.queue.add((byte) p.create(metadata));
    }

}
