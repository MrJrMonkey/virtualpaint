# Virtual Paint - Hand Gesture Drawing App

A real-time hand gesture-based drawing application using computer vision and hand tracking. Draw in the air using just your hand movements!

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-green.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10+-orange.svg)

## 📝 Description

This application uses your webcam and hand tracking to create a virtual drawing canvas. Simply point your index finger to draw, use two fingers to navigate, and select colors from the palette at the top of the screen.

## ✨ Features

- **Hand Gesture Drawing**: Draw using your index finger
- **Color Palette**: Choose from 6 different colors (Magenta, Blue, Green, Red, Yellow, Cyan)
- **Eraser Tool**: Erase your drawings
- **Selection Mode**: Move without drawing using two fingers
- **Clear Canvas**: Clear the entire canvas with one click
- **Save Drawing**: Save your artwork as an image file
- **Real-time Hand Tracking**: Smooth and responsive hand detection

## 🎮 Controls

| Gesture | Action |
|---------|--------|
| **Index finger up** | Draw on the canvas |
| **Index + Middle fingers up** | Selection mode (navigate without drawing) |
| **Click on color boxes** | Select drawing color |
| **Click 'E' button** | Activate eraser |
| **Click 'C' button** | Clear the canvas |
| **Press 'q'** | Quit the application |
| **Press 's'** | Save your drawing |
| **Press 'c'** | Clear canvas (keyboard shortcut) |

## 🔧 Dependencies

The application requires the following Python packages:

- **OpenCV (cv2)** - For video capture and image processing
- **MediaPipe** - For hand tracking and landmark detection
- **NumPy** - For array operations and canvas manipulation

## 📦 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/rahulkannan08/virtualpaint.git
cd virtualpaint
```

### Step 2: Create a Virtual Environment (Optional but Recommended)

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Dependencies

```bash
pip install opencv-python mediapipe numpy
```

Or install from requirements.txt:

```bash
pip install -r requirements.txt
```

## 🚀 Usage

1. **Make sure your webcam is connected and working**

2. **Run the application:**
   ```bash
   python virtualpaint.py
   ```

3. **Position your hand in front of the webcam:**
   - Make sure your hand is clearly visible
   - Keep your hand within the camera frame
   - Adequate lighting helps with detection

4. **Start drawing:**
   - Raise your **index finger** to start drawing
   - Move your hand to create your artwork
   - Raise **index and middle fingers** together to move without drawing

5. **Select colors:**
   - In selection mode (two fingers), move to the top of the screen
   - Click on any color box to change the drawing color

6. **Save your artwork:**
   - Press **'s'** to save your drawing as `hand_drawing.png`

7. **Exit:**
   - Press **'q'** to quit the application

## 📋 Requirements.txt

Create a `requirements.txt` file with:

```
opencv-python>=4.8.0
mediapipe>=0.10.0
numpy>=1.24.0
```

## 🛠️ Troubleshooting

### Webcam not detected
- Ensure your webcam is properly connected
- Check if other applications are using the webcam
- Try changing the camera index in the code: `cap = cv2.VideoCapture(1)` or `cap = cv2.VideoCapture(2)`

### Hand not detected
- Ensure proper lighting in your environment
- Keep your hand at a reasonable distance from the camera
- Make sure your palm is facing the camera
- Try adjusting the detection confidence values in the code

### Low performance
- Close other applications using the camera
- Reduce the frame resolution in the code
- The app processes every 2nd frame by default for better performance

## 🎯 How It Works

1. **Hand Detection**: Uses MediaPipe's hand tracking solution to detect hand landmarks
2. **Finger Counting**: Calculates which fingers are up based on landmark positions
3. **Gesture Recognition**: Interprets finger positions as drawing or selection gestures
4. **Canvas Drawing**: Creates a virtual canvas and draws lines based on finger movement
5. **Real-time Merging**: Combines the webcam feed with the drawing canvas

## 📸 Screenshots

The app displays:
- Live webcam feed with hand tracking
- Your drawings overlaid on the video
- Color palette at the top
- Current color indicator on the right
- Instructions at the bottom

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Rahul Kannan**
- GitHub: [@rahulkannan08](https://github.com/rahulkannan08)

## 🙏 Acknowledgments

- Google MediaPipe for the hand tracking solution
- OpenCV community for computer vision tools

---

**Enjoy drawing in the air! 🎨✨**
