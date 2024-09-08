# Description
This project offers a user interface for [DIY Spacemouse](https://www.printables.com/de/model/864950-open-source-spacemouse-space-mushroom-remix) to control sensitivity parameters by app basis.
It's main purpose is to replace the sliders from 3DConnection software (3DConnection installation is mandatory).
<p float="left">
  <img src="https://github.com/user-attachments/assets/b068b5ea-63c1-4627-b437-04fd9366b2af" width=49%>
  <img src="https://github.com/user-attachments/assets/de639742-c974-4c94-8e47-98412571ab8a" width=49%>
</p>


# Installation
## Set up Spacemouse firmware
1. Clone this repository:  
`git clone https://github.com/raulpetru/SpacemouseProfiles`
1. Create a custom board in Arduino IDE using [these instructions](https://github.com/AndunHH/spacemouse/wiki/Creating-a-custom-board-for-Arduino-IDE).
2. Connect Spacemouse to PC and flash firmware from `spacemouse-keys`folder on Arduino.

## Set up Spacemouse Profiles application
1. Clone this repository (if you haven't cloned in previous step):  
`git clone https://github.com/raulpetru/SpacemouseProfiles`
2. Install Python 3.1x (3.11, 3.12, ...)
3. Make virtual environment:  
`python -m venv .venv`
4. Install dependencies:  
`pip install -r requirements.txt`

5. Run `Spacemose Profiles.bat` to launch the app.

This project is based on the work of [AndunHH](https://github.com/AndunHH/spacemouse), [TeachingTech](https://www.printables.com/de/model/864950-open-source-spacemouse-space-mushroom-remix) and many other contributors.
