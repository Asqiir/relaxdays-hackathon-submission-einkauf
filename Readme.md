This project was created in the Relaxdays Code Challenge Vol. 1. See https://sites.google.com/relaxdays.de/hackathon-relaxdays/startseite for more information. My participant ID in the challenge was: CC-VOL1-37.

# How to run this project

## Prerequisites

* Docker
* Port 8080 is used here, so it shouldn't be already used
* This program uses the file `data.json`. (So this name shouldn't be used for anything else in the same direction.)

## Commands to run

```bash
git clone https://github.com/Asqiir/relaxdays-hackathon-submission-einkauf.git
cd relaxdays-hackathon-submission-einkauf
docker build -t einkauf .
docker run -p 8080:8080 einkauf
```
