### Step 1: Update Model Paths
#Modify the `MODEL_PATH` and `LABELS_PATH` variables in your main script to point to your new model files.


# Update paths for the new model
MODEL_PATH = "path_to_your_new_model.h5"
LABELS_PATH = "path_to_your_labels.txt"


### Step 2: Update Label Mapping
#Ensure that `class_labels` in your code reflects the four categories:

with open(LABELS_PATH, "r") as f:
    class_labels = [line.strip() for line in f.readlines()]
# class_labels should now be ['0', '1', '2', '3']


### Step 3: Import OpenCV for Webcam Access
#At the top of your script, import OpenCV and set up webcam access:


import cv2

def main():
    # Check if webcam is accessible
    if not cv2.VideoCapture(0).isOpened():
        print("Error: Camera not accessible")
        return
    
    cap = cv2.VideoCapture(0)


### Step 4: Modify the Predict Function for the New Model
#Update your prediction function to handle the new model and labels:


def predict_on_image(model, image_path=None):
    """Run model prediction on an image or live feed frame."""
    try:
        # For live feed, use cap.read()
        if image_path is not None:
            img = cv2.imread(image_path)
        else:
            ret, img = cap.read()

        # Preprocess the frame
        if not ret:
            raise ValueError("Failed to capture frame from webcam")
        
        img = cv2.resize(img, (224, 224))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_array = np.asarray(img, dtype=np.float32) / 127.5 - 1
        img_array = img_array[None, :, :, :]  # Add batch dimension

        # Run prediction
        predictions = model.predict(img_array)

        # Get the index of the highest probability class
        top_class_index = np.argmax(predictions[0])
        confidence = predictions[0][top_class_index]

        # Map to actual label (assuming labels are 0-based)
        top_class_label = class_labels[top_class_index]
        
        if confidence > 0.6:  # Only show predictions above 60% confidence
            print(f"Predicted: {top_class_label} with confidence {confidence}")
            cv2.putText(img, f"Prediction: {top_class_label}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Display the frame
        cv2.imshow("Object Detection", img)

    except Exception as e:
        print(f"Error in predict_on_image: {str(e)}")


### Step 5: Modify Main Loop to Process Frames Continuously
#Update your main function to continuously capture and process frames:

if __name__ == "__main__":
    # Initialize model loading
    try:
        model = load_model(MODEL_PATH)  # Ensure this is a function that loads your model correctly
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        exit(1)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera not accessible")
        exit(1)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            break

        # Process the frame (already done in predict_on_image above)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
