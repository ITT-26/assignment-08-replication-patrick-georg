[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/sPpq67Dc)

# Requirements

- Audio Interface (for Input and Output with ASIO Drivers for latency free AMP simulation)
- Guitar Rig 7
- Electric Guitar
- Python (3.13 used to code this)
- Install requirements using pip install -r requirements.txt

# Usage

- Start Guitar Rig 7
- use python app.py to start the application

# Why did we choose this topic?

We looked up what kind of projects were done previously in the course.<br>
We found some interesting topics with keyboard input.<br>
Since nobody of us owns or plays keyboard we thought of using different instruments.<br>
So we thought of other instruments and since an electric guitar can be easily connected to a pc we decided on looking for papers using an guitar as an input.<br>
We found the paper on GuitarPie (https://dl.acm.org/doi/epdf/10.1145/3746059.3747799) and decided that we want to do something similar.<br>

# What we want to do different

GuitarPie focusses on viewing tabulature.<br>
From my experience Scrolling through transcripts is tedious while playing, but using the guitar as an input method while playing is obviously not gonna work.<br>
So we thought of other use cases.<br>
The main use case is changing AMP presets since we are already connected to a pc.

# Documentation

This program aims to help you play Guitar with an amp sim and use your Guitar to control your environment.<br>
We use notes on the guitar and map them to different key presses.<br><br>
The main functionality of this application is to change AMP preset in Guitar Rig 7.<br>
We chose Guitar Rig 7 because it is a free software with good presets.<br>
Once one preset is selected we simulate mouse input and text search to select it in the AMP sim<br>
Sadly there was no other way for a better implementation of this feature that was fast enough for good usage.<br>
So the user needs to not have any filters open in the program.<br>
This is a limitation we were willing to take for the sake of performance<br><br>
Another main functionality is the tuner.<br>
This seems necessary for using notes as inputs.<br>
During Tuning the Controller is paused for obvious reasons.<br><br>
Another important feature is the lock-mode.<br>
A certain note triggers the controls to freeze and lets the user play without triggering any side effects.<br><br>
A short demo funcitonality is a metronom.<br>
This is just a demo for showing how other functionalities could be implemented in the future.