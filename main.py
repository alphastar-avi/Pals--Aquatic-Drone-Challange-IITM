
MODEL_PATH = "path_to_your_new_model.h5"
LABELS_PATH = "path_to_your_labels.txt"


with open(LABELS_PATH, "r") as f:
    class_labels = [line.strip() for line in f.readlines()]


import cv2

def main():
    
    if not cv2.VideoCapture(0).isOpened():
        print("Error: Camera not accessible")
        return
    
    cap = cv2.VideoCapture(0)



def predict_on_image(model, image_path=None):
    """Run model prediction on an image or live feed frame."""
    try:
        
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

        
        predictions = model.predict(img_array)

       
        top_class_index = np.argmax(predictions[0])
        confidence = predictions[0][top_class_index]

       
        top_class_label = class_labels[top_class_index]
        
        if confidence > 0.6:  
            print(f"Predicted: {top_class_label} with confidence {confidence}")
            cv2.putText(img, f"Prediction: {top_class_label}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Display the frame
        cv2.imshow("Object Detection", img)

    except Exception as e:
        print(f"Error in predict_on_image: {str(e)}")



if __name__ == "__main__":
    # Initialize model loading
    try:
        model = load_model(MODEL_PATH) 
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        exit(1)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera not accessible")
        exit(1)

    while True:
      
        ret, frame = cap.read()

        if not ret:
            break


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
