package me.pablo.robotcontroller.model;

import me.pablo.robotcontroller.network.MetadataProvider;

import java.util.Objects;
import java.util.function.Consumer;

public class Robot {

    private static final Robot INSTANCE = new Robot();
    public static Robot getInstance() {
        return INSTANCE;
    }

    private State state = State.MANUAL_MODE;
    private String status = "Initializing...";
    private int direction;

    private Consumer<String> changeListener = r -> {};

    private Robot() {}

    public State getState() {
        return this.state;
    }

    public void setState(State state) {
        if (this.state == state) return;
        this.state = state;
        changeListener.accept("state");
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        if (Objects.equals(this.status, status)) return;
        this.status = status;
        changeListener.accept("status");
    }

    public int getDirection() {
        return direction;
    }

    public void setDirection(int direction) {
        if (this.direction == direction) return;
        this.direction = direction;
        changeListener.accept("direction");
    }

    public void addChangeListener(Consumer<String> listener) {
        Consumer<String> prevListener = this.changeListener;
        this.changeListener = r -> {
            prevListener.accept(r);
            listener.accept(r);
        };
    }

    public enum State implements MetadataProvider {
        MANUAL_MODE("Manual"),
        AUTONOMOUS_MODE("Auto"),
        EXIT("Exit");

        private final String display;

        State(String display) {
            this.display = display;
        }

        @Override
        public String toString() {
            return display;
        }

        public int metadata() {
            return ordinal() + 1;
        }
    }

}
