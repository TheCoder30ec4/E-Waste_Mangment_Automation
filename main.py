import time
import ultralytics
import cv2
import socket

host = "192.168.130.3"
port = 5003


# Establish socket connection
client_socket = socket.socket()
client_socket.connect((host, port))

# Function to capture and predict
def capture_and_predict(model_path):
    """
    Captures an image in real-time, saves it on spacebar press,
    performs object detection using the specified model, and prints the detected class.

    Args:
        model_path (str): Path to the YOLO model file.

    Returns:
        None
    """

    try:
        # Load the model
        model = ultralytics.YOLO(model_path)

        # Capture video
        cap = cv2.VideoCapture(1)

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            # BGR to RGB conversion
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Display the frame
            cv2.imshow('YOLO V8 Capture', img)

            # Check for spacebar press
            key = cv2.waitKey(1) & 0xFF
            if key == ord(' '):
                # Capture image and filename
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"capture_{timestamp}.jpg"

                # Save the image
                cv2.imwrite(filename, img)

                print("Image captured and saved:", filename)

                # Perform object detection on the saved image
                results = model(filename)

                # Extract and print class number(s)
                for r in results:
                    for box in r.boxes:
                        class_id = int(box.cls)
                        print(f"Detected object: {model.names[class_id]}")

                        # Send class information to server
                        client_socket.sendall(f"Detected object: {model.names[class_id]}\n".encode())


                # Optional: Option to break after capturing an image
                # break

            # Exit on 'q' press
            if key == ord('q'):
                break

        # Release resources
        cap.release()
        cv2.destroyAllWindows()

    except FileNotFoundError:
        print(f"Error: Model file not found at '{model_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        # Close the socket connection
        client_socket.close()

# Replace with your model path
model_path = "C:/Users/varun/Downloads/last (1).pt"

if __name__ == "__main__":
    capture_and_predict(model_path)
