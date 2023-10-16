import cv2
import time
import os
import random
import string

def generate_random_filename(length=10, extension=""):
    """
    Generate a random filename.

    Parameters:
    - length: Length of the random part of the filename (excluding extension).
    - extension: File extension (e.g., ".txt").

    Returns:
    A random filename as a string.
    """
    # Define the character pool for generating the random part of the filename.
    characters = string.ascii_letters + string.digits

    # Generate a random filename with the specified length and extension.
    random_part = ''.join(str(random.choice(characters)) for _ in range(length))
    filename = random_part + extension

    return filename


def read_image(input_image_path):
    cv2_image = cv2.imread(input_image_path)
    return cv2_image


def load_labels(filename):
  with open(filename, 'r') as f:
    return [line.strip() for line in f.readlines()]


def draw_detections(detections, cv2_image, model_type):
    colors = [(61, 203, 0), (4, 39, 240), (255, 3, 0), (255, 126, 0), (41, 141, 172), (10, 255, 0)]
    if model_type == "ssd": 
        for index, detection in enumerate(detections.get("detection")):
            xmin = detection.get("label_bounding_box")[0].get("x")
            ymin = detection.get("label_bounding_box")[0].get("y")
            xmax = detection.get("label_bounding_box")[1].get("x")
            ymax = detection.get("label_bounding_box")[1].get("y")
            cv2.rectangle(cv2_image, (xmin, ymin), (xmax, ymax), colors[index], 2)
            # Draw label
            object_name = detection["label_class_name"]
            confidence = detection["confidence"]
            label = '%s: %d%%' % (object_name, int(confidence*100))
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
            label_ymin = max(ymin, labelSize[1] + 10)
            cv2.rectangle(cv2_image, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED)
            cv2.putText(cv2_image, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)    
    else:
        position = (30, 30)
        font_scale = 0.75
        color = (255, 255, 255)
        thickness = 2
        font = cv2.FONT_HERSHEY_SIMPLEX
        line_type = cv2.LINE_AA
        x, y0 = position
        for i, line in enumerate(detections.get("detection")):
            text_size, _ = cv2.getTextSize(line, font, font_scale, thickness)
            line_height = text_size[1] + 5
            y = y0 + i * line_height
            cv2.putText(cv2_image,
                        line,
                        (x, y),
                        font,
                        font_scale,
                        color,
                        thickness,
                        line_type)
    return cv2_image 


def save_detection_image(detections : dict, cv2_image, output_image_path: str, model_type: str = "ssd"):
    draw_detections(detections, cv2_image, model_type)
    cv2.imwrite(output_image_path, cv2_image)


def save_frame(frame, output_path: str, model_type: str = "ssd"):
    output_image_path = os.path.join(output_path, generate_random_filename(extension=".jpg"))
    cv2.imwrite(output_image_path, frame)


def show_detection_image(cv2_image):
    cv2.imshow('Detection', cv2_image)
    # Press any key to continue to next image, or press 'q' to quit
    if cv2.waitKey(0) == ord('q'):
        time.sleep(10)
    # Clean up
    cv2.destroyAllWindows()

