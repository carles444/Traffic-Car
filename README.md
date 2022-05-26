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
  <li>opencv-python</li>
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
