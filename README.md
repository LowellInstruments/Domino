![Lowell Instruments LLC Logo](/images/LowellInstrumentsLLC_Logo.png)

# Domino
## Introduction
[Domino](https://lowellinstruments.com/products/domino/) is the unified application for data logging hardware from [Lowell Instruments LLC](https://lowellinstruments.com).  Domino is a user friendly tool for communicating with Lowell Instruments data loggers and current meters.

![Domino Status Screen](/images/Status_Screen.jpg)

## Major features
* Set recording parameters, enable/disable channels, set start/stop times etc.
* Check the status and current values, set and reset the real-time clock, start and stop recording
* Convert binary files (.lid) to text files (.csv) in various formats

## License
This project is released under the GPLv3 Liceense.

## Versions and Installers
For the current installer version see [releases](https://github.com/LowellInstruments/Domino/releases).

## Linux
Some (all?) versions of Linux require the user to be added to the "dialout" group. If you are having troubles connecting to your device, this is likely the problem.
To check if you are a member of that dialout group:
groups ${USER}

this will list all the groups the user belongs to. If the dialout group is not listed, execute the following command:

sudo gpasswd --add ${USER} dialout
Then log out and log back in.

## Installation from source
For instructions on installing a non-copiled version of Domino on visit [this link](https://docs.google.com/document/d/1XTJbaWQCGlz6biqpjBedaM95eXBzJDoDuvx9tnO_Ktc/edit?usp=sharing).
