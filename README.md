# LabUI
A Python-based GUI to control the FLAIR Lab experimental setup
## Overview:
As part of my Final Year Project as a Mechatronics student, I was assigned the task to develop a graphical user interface (GUI) for Monash’s University’s FLAIR Lab. Dr.Jisheng Zhao was investigating flow induced vibrations (FIVs) of 3D buff bodies and required an application that could communicate with the lab hardware. The application needed to handle raw experimental data, provide notifications to the user and display a live data feed. 

The lab setup consisted of an air-bearing system attached with a servo motor submerged in a water channel. By varying the water channel velocity and motor movement, the FIVs of the system were to be measured. The servo motor was controlled by Beckhoff Automation GmbH Hardware which was interfaced with the Beckhoff TwinCAT 3 software. 

To control this setup, I developed a Python-based GUI using PyQt5 called LabUI (LUI). LUI is capable of displaying live experimental data to the user while logging the raw data to a local csv file. LUI communicates with TwinCAT 3 to control the experimental setup and retrieve the data from it. Upon completion of the experiment, LUI can notify the user via email with any additional notes attached in the body of the email. 

*Due to the COVID-19 lockdown restrictions and the FLAIR Lab being used for various projects, LUI is yet to be tested with the actual setup in the lab. The files in this repository essentially simulate an ideal working case, however once the hardware is interfaced with TwinCAT 3, LUI should run smoothly.
