# HoverPad 🚀🪄

Ditch your physical mouse. HoverPad uses your webcam and real-time machine learning to turn your bare hand into a lightning-fast virtual trackpad for macOS and Windows.

## Features
- **Cross-Platform Support**: Works out-of-the box on both Mac and Windows! The code automatically detects your OS and triggers native commands (e.g., Mission Control on Mac, Task View on Windows).
- **Custom Neural Network**: Train the AI to recognize *your* exact hand shapes using the built-in data collector.
- **Scale Normalization**: Advanced spatial math ensures the AI recognizes your hand whether it is 2 inches or 5 feet away from the camera.
- **Anchor Swiping**: Dynamic anchor-point logic for flawless Desktop swiping (prevents accidental flickering by requiring deliberate physical distance).
- **Background Hotkey**: Press `Ctrl + Shift + H` at any time to pause the AI tracking so you can use your hands normally.

## Installation

1. Clone this repository to your machine:
```bash
git clone https://github.com/YOUR_USERNAME/HoverPad.git
cd HoverPad
```

2. Create and activate a Python Virtual Environment:
```bash
# On macOS/Linux:
python3 -m venv .venv
source .venv/bin/activate

# On Windows:
python -m venv .venv
.venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## How to Use (The 3 Phases)

**🚀 QUICK START:** Don't want to collect data and train the AI yourself? Skip straight to **Phase 3**! This repository includes a pre-trained `gesture_model.pkl` file so you can start controlling your computer instantly using the default gestures.

### Phase 1: Data Collection
Run the data collector to teach the AI your custom hand shapes:
```bash
python collect_data.py
```
Hold up the following shapes and press the corresponding number keys to record them (~150 frames each):
* `0` = Move Mouse (Open Hand)
* `1` = Left Click (OK Sign / Pinch)
* `2` = Right Click (Fist)
* `3` = Scroll (Peace Sign)
* `4` = Switch Desktops (Thumbs Up)
* `5` = Mission Control / Task View (Surfer / Shaka Sign)

### Phase 2: Train the Brain
Train the Machine Learning model on your collected data spreadsheet:
```bash
python train_brain.py
```
*This will generate a `gesture_model.pkl` file (your AI Brain) and output your model's accuracy score.*

### Phase 3: Run the Smart Mouse
Start the mouse and control your computer!
```bash
python smart_mouse.py
```
*(Press `q` on the video window to quit, or `Ctrl+Shift+H` to pause).*
