package me.pablo.robotcontroller.network;

public enum Packet {
    SET_MODE,
    MOVE;

    public int create(int metadata) {
        return ((ordinal() + 1) << 4) | (metadata & 0xF);
    }
}
