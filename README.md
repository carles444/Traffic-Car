# Traffic-Car
A robot that tries to replicate the inner workings of a real car. Instead of building a typical 3-wheel car
with 2 engines or even a 4-wheel car with 4 engines, we have focused on creating a 4-wheel car with a single 
dc engine and a servomotor, doing it this way makes it harder since you need steering and transmission
mechanisms, but thats the challenge! 
The main goal of the project is to be able to drive the car with a bluetooth controller, in addition we wanted use 
a camera in the car and apply computer vision algorithms to make it self-driven. The car has a differential that enables
the rear wheels to spin at different speeds, as well as a steering system for the front wheels to turn.


## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Python3.10 packages:
 - pybluez
 - RPi.GPIO

Java:
 - JDK 11 or greater
 - maven
   - bluecove (via maven)
   - flatlaf (via maven)

## Architecture
### Software architecture
![software](https://github.com/carles444/other-stuff/blob/main/software.png)

This project is divided in two main components:
 - [Raspberry controller](https://github.com/carles444/Traffic-Car/tree/main/raspberryController), written in python, runs on the raspberry pi on the robot itself
 - [Robot controller](https://github.com/carles444/Traffic-Car/tree/main/RobotController), written in java, runs on the PC, and allows input commands being sent to the robot.

The main idea behind this is that we have a client-server based architecture that ties (via Bluetooth) the Raspberry controller and the robot controller together.
Robot controller acts as a bluetooth server, while raspberry controller acts as a client that will search for a controller server.
Once they are connected the robot controller sends the necessary inputs to swap between modes and control the car via keyboard. When the manual driver or the autonomous drivers request a movement(forward, turn left, ...) the Driver module within raspberry controller uses the Raspberry pi pins to manipulate the different physical components(ex: servomotor).

## Hardware architecture

![hardware](https://github.com/carles444/other-stuff/blob/main/hardware.png)

The robot consists of one servo motor and one dc motor, both are connected to a raspberry pi, the dc motor is connected via a motor controller.
The dc motor is powered by a 9 volt battery, and the servo motor is supplied by the raspberry pi itself. We also have a pi camera connected to the raspberry pi. The raspberry pi is connected to a portable battery.

## Compiling

The javaside RobotController is compiled using maven:

```bash
  $ cd RobotController
  $ mvn clean package
```

The compile output will be in the `target` subfolder.

## Running
Note: On linux operating systems bluetooth control requires sudo permissions from our testing, and will fail when running in normal user mode.

### Raspberry pi
```bash
  $ cd raspberryController/src
  $ sudo python3 controller.py
```

### Laptop
```bash
  $ cd target
  $ sudo java -jar RobotController-1.0-SNAPSHOT.jar
```

#### Controller view
![not found](https://github.com/carles444/other-stuff/blob/main/controller.png)

The inputs are taken either from toggling the individual buttons with your mouse or, more conveniently, holding the W-A-S-D keys on your keyboard.

## Authors
- Carles Andreu Torreblanca
- Pablo Herrera
- Victor Fusalba Raña
- Miguel Angel Mendoza

