# AI Hand Mouse for macOS 🪄🖱️

A completely touchless, AI-powered virtual trackpad for Mac. This project uses your webcam, **MediaPipe** for skeletal hand tracking, and a custom **Machine Learning model (Random Forest)** to recognize highly specific hand gestures and control your computer natively.

## Features
- **Custom Neural Network**: Train the AI to recognize *your* exact hand shapes using the built-in data collector.
- **Scale Normalization**: Advanced spatial math ensures the AI recognizes your hand whether it is 2 inches or 5 feet away from the camera.
- **Anchor Swiping**: Dynamic anchor-point logic for flawless Desktop swiping (prevents accidental flickering by requiring deliberate physical distance).
- **Native Mac Integration**: Uses native AppleScript to trigger Mission Control and Desktop Spaces, bypassing macOS Python keyboard simulation security blocks.
- **Background Hotkey**: Press `Ctrl + Shift + H` at any time to pause the AI tracking so you can use your hands normally.

## Installation

1. Clone this repository to your machine:
```bash
git clone https://github.com/YOUR_USERNAME/AI_Hand_Mouse.git
cd AI_Hand_Mouse
```

2. Create and activate a Python Virtual Environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## How to Use (The 3 Phases)

**🚀 QUICK START:** Don't want to collect data and train the AI yourself? Skip straight to **Phase 3**! This repository includes a pre-trained `gesture_model.pkl` file so you can start controlling your Mac instantly using the default gestures.

### Phase 1: Data Collection
Run the data collector to teach the AI your custom hand shapes:
```bash
python3 collect_data.py
```
Hold up the following shapes and press the corresponding number keys to record them (~150 frames each):
* `0` = Move Mouse (Open Hand)
* `1` = Left Click (OK Sign / Pinch)
* `2` = Right Click (Fist)
* `3` = Scroll (Peace Sign)
* `4` = Switch Desktops (Thumbs Up)
* `5` = Mission Control (Surfer / Shaka Sign)

### Phase 2: Train the Brain
Train the Machine Learning model on your collected data spreadsheet:
```bash
python3 train_brain.py
```
*This will generate a `gesture_model.pkl` file (your AI Brain) and output your model's accuracy score.*

### Phase 3: Run the Smart Mouse
Start the mouse and control your Mac!
```bash
python3 smart_mouse.py
```
*(Press `q` on the video window to quit, or `Ctrl+Shift+H` to pause).*
