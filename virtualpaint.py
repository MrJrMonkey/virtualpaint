import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Create a blank canvas for drawing
canvas = None

# Drawing settings
draw_color = (255, 0, 255)  # Magenta (BGR format)
brush_thickness = 8
eraser_thickness = 50

# Previous point for smooth drawing
prev_x, prev_y = 0, 0

# Color palette (BGR format)
colors = [
    (255, 0, 255),   # Magenta
    (255, 0, 0),     # Blue
    (0, 255, 0),     # Green
    (0, 0, 255),     # Red
    (0, 255, 255),   # Yellow
    (255, 255, 0),   # Cyan
]

def fingers_up(hand_landmarks):
    """Check which fingers are up"""
    tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky finger tips
    fingers = []
    
    # Thumb (special case - check x position)
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers.append(1)
    else:
        fingers.append(0)
    
    # Other fingers (check y position)
    for tip in tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    
    return fingers

def draw_color_palette(img):
    """Draw color selection palette on the image"""
    palette_y = 10
    palette_size = 40
    spacing = 60
    
    for i, color in enumerate(colors):
        x_start = 10 + i * spacing
        cv2.rectangle(img, (x_start, palette_y), (x_start + palette_size, palette_y + palette_size), color, -1)
        cv2.rectangle(img, (x_start, palette_y), (x_start + palette_size, palette_y + palette_size), (255, 255, 255), 2)
    
    # Eraser button
    eraser_x = 10 + len(colors) * spacing
    cv2.rectangle(img, (eraser_x, palette_y), (eraser_x + palette_size, palette_y + palette_size), (50, 50, 50), -1)
    cv2.putText(img, "E", (eraser_x + 12, palette_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    
    # Clear button
    clear_x = eraser_x + spacing
    cv2.rectangle(img, (clear_x, palette_y), (clear_x + palette_size, palette_y + palette_size), (0, 0, 128), -1)
    cv2.putText(img, "C", (clear_x + 12, palette_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

print("Hand Drawing App Started!")
print("Controls:")
print("  - Index finger up: Draw")
print("  - Index + Middle fingers up: Selection mode (move without drawing)")
print("  - Move to top to select colors")
print("  - 'E' button: Eraser")
print("  - 'C' button: Clear canvas")
print("  - Press 'q' to quit")
print("  - Press 's' to save your drawing")

frame_count = 0
while True:
    success, frame = cap.read()
    if not success:
        print("Failed to capture frame")
        break
    
    frame_count += 1
    
    # Flip the frame horizontally for a mirror effect
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape
    
    # Initialize canvas if not created
    if canvas is None:
        canvas = np.zeros((h, w, 3), dtype=np.uint8)
    
    # Convert BGR to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame (only every 2nd frame for better performance)
    results = None
    if frame_count % 2 == 0:
        try:
            results = hands.process(rgb_frame)
        except Exception as e:
            print(f"Hand processing error: {e}")
            results = None
    
    if results and results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks on frame
            mp_drawing.draw_landmarks(
                frame, 
                hand_landmarks, 
                mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
            )
            
            # Get finger positions
            fingers = fingers_up(hand_landmarks)
            
            # Get index finger tip position
            index_tip = hand_landmarks.landmark[8]
            x = int(index_tip.x * w)
            y = int(index_tip.y * h)
            
            # Selection mode (index + middle finger up)
            if fingers[1] == 1 and fingers[2] == 1:
                prev_x, prev_y = 0, 0  # Reset previous point
                
                # Check if in palette area
                if y < 60:
                    spacing = 60
                    palette_size = 40
                    
                    # Check color selection
                    for i, color in enumerate(colors):
                        x_start = 10 + i * spacing
                        if x_start < x < x_start + palette_size:
                            draw_color = color
                    
                    # Check eraser
                    eraser_x = 10 + len(colors) * spacing
                    if eraser_x < x < eraser_x + palette_size:
                        draw_color = (0, 0, 0)  # Black for eraser
                    
                    # Check clear
                    clear_x = eraser_x + spacing
                    if clear_x < x < clear_x + palette_size:
                        canvas = np.zeros((h, w, 3), dtype=np.uint8)
                
                # Draw selection circle
                cv2.circle(frame, (x, y), 15, draw_color, 2)
            
            # Drawing mode (only index finger up)
            elif fingers[1] == 1 and fingers[2] == 0:
                # Draw circle at fingertip
                thickness = eraser_thickness if draw_color == (0, 0, 0) else brush_thickness
                cv2.circle(frame, (x, y), thickness // 2, draw_color, -1)
                
                if prev_x == 0 and prev_y == 0:
                    prev_x, prev_y = x, y
                
                # Draw line on canvas
                cv2.line(canvas, (prev_x, prev_y), (x, y), draw_color, thickness)
                prev_x, prev_y = x, y
            
            else:
                prev_x, prev_y = 0, 0
    
    # Merge canvas with frame
    # Create a mask where canvas has drawings
    gray_canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray_canvas, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    
    # Black out area of drawing in frame
    frame_bg = cv2.bitwise_and(frame, frame, mask=mask_inv)
    
    # Take only drawing from canvas
    canvas_fg = cv2.bitwise_and(canvas, canvas, mask=mask)
    
    # Combine
    combined = cv2.add(frame_bg, canvas_fg)
    
    # Draw color palette
    draw_color_palette(combined)
    
    # Show current color indicator
    cv2.rectangle(combined, (w - 60, 10), (w - 10, 60), draw_color, -1)
    cv2.rectangle(combined, (w - 60, 10), (w - 10, 60), (255, 255, 255), 2)
    cv2.putText(combined, "Current", (w - 70, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # Display instructions
    cv2.putText(combined, "Index finger: Draw | Two fingers: Select | 'q': Quit | 's': Save", 
                (10, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Display FPS indicator
    cv2.putText(combined, f"Frame: {frame_count}", (10, h - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    
    # Show the frame
    cv2.imshow("Hand Drawing App", combined)
    
    # Key controls
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        cv2.imwrite("hand_drawing.png", canvas)
        print("Drawing saved as 'hand_drawing.png'")
    elif key == ord('c'):
        canvas = np.zeros((h, w, 3), dtype=np.uint8)
        print("Canvas cleared")

# Cleanup
cap.release()
cv2.destroyAllWindows()
hands.close()
print("Application closed")