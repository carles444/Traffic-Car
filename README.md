# Traffic-Car
A robot that tries to replicate a working real car, instead of trying to build a typical 3 wheel car
with 2 engines or even a 4 wheel car with 4 engines we have focused on creating a 4 wheel car with just
a dc engine and a servomotor, this way of doing it makes it harder to create a steering and transmission
mechanism, but thats the challenge! 
The main objective of this robot is to drive it with a bluetooth controller, in addition we wanted use a cam
in the car to apply computer vision algorithms to make it self-driven. The car has a differential that makes it
able to take the power from de dc engine to the wheels and also to make them roll at different
velocities. It also has a steering system so that the front wheels can turn the same way.


## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Python3.10 packages:
<ul>
  <li>pybluez</li>
  <li>RPi.GPIO</li>
  
</ul>

Java:
<ul>
  <li>JDK 11 or greater</li>
  <li>bluecove</li>
  <li>flatlaf</li>
</ul>

## Architecture
### Software architecture
![not found](https://github.com/carles444/other-stuff/blob/main/software.png)

This project is based in two parts, the Raspberry controller(controller) and the Main Controller(InputModule), the first runs in the Raspberry pi and its written in python3 and
the second one runs in a laptop and its written in Java. The main aim with this architecture is building a client-server based program that communicates via Bluetooth, the Raspberry controller tries
to connect until the Controller is up, once they are connected the controller sends the necessary inputs to swap between the different modes and control the car via keyboard. When manual driver or autonomous driver request some movement(forward, turn left, ...) the Driver module uses the Raspberry pi pins to manipulate the different physical components(ex: servomotor).

## Hardware architecture

![not found](https://github.com/carles444/other-stuff/blob/main/hardware.png)

The robot consists on one servo motor and one dc motor, theese two are connected to a raspberry pi.
The dc motor is supplied by a 9Volts battery and the servo motor is supplied by the raspberry pi itself. We also have a pi camera connected to the raspberry pi. The raspberry pi is connected to a portable battery.

## Usage
### Raspberry pi
```bash
  $ cd ~/source/raspberryController/src
  $ sudo python3 controller.py
```

### Laptop
```bash
  $ cd ~/source
  $ sudo java -jar RobotController-1.0-SNAPSHOT.jar
```

#### Controller view
![not found](https://github.com/carles444/other-stuff/blob/main/controller.png)

The inputs are taken either from clicking or using keys WASD.

## Authors
Carles Andreu Torreblanca
Pablo Herrera
Victor Fusalba Raña
Miguel Angel Mendoza

