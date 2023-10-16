import tensorflow as tf
import cv2
import numpy as np
import time
from innovationmerge.configurations.constants import DETECTION_RESPONSE_BB, DETECTION_RESPONSE

class EdgeObjectDetectionTfLite():
    """
    Object detection inference using Tensorflow Lite models. 
    This class includes loading the model, preparing input data, invoking the interpreter, and extracting output results. 
    """
    def __init__(self, model_file_path):
        # Load the TensorFlow Lite model
        self.interpreter = tf.lite.Interpreter(model_path=model_file_path)
        self.interpreter.allocate_tensors()

        # Set input normalization parameters
        self.input_mean = 127.5
        self.input_std = 127.5

    def detect(self, cv2_image, labels_list, threshold, model_type="ssd"):
        """
        Parameters:
            cv2_image: OpenCV 2 Image
            labels_list: labels list
            threshold: minimum score
        Returns:
            Array of Detections(Label, Bounding Box, Confidence score)
        """
        # # Get input and output details from the interpreter
        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()

        # Convert the input image to RGB format
        normalize_height = input_details[0]['shape'][1]
        normalize_width = input_details[0]['shape'][2]

        # convert input image to gray scale
        image_rgb = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
        input_img_height, input_img_width, _ = image_rgb.shape

        # Resize the input image to match the model's input requirements
        image_resized = cv2.resize(image_rgb, (normalize_width, normalize_height))

        # Add an extra dimension to the input data
        input_data = np.expand_dims(image_resized, axis=0)

        # Check if the model expects floating-point input
        floating_model = (input_details[0]['dtype'] == np.float32)
        if input_details[0]['dtype'] == type(np.float32(1.0)):
            floating_model = True

        # Normalize the input data if floating_model is True
        if floating_model:
            input_data = (np.float32(input_data) - self.input_mean) / self.input_std
        
        # Set the input tensor for the interpreter
        self.interpreter.set_tensor(input_details[0]['index'], input_data)

        # Perform the model inference
        start_time = time.time()
        self.interpreter.invoke()
        stop_time = time.time()

        # Determine the indices for accessing the output tensor.The specific indices for accessing the output tensors depend on whether the model is a TensorFlow 1.x or TensorFlow 2.x model.
        out_name = output_details[0]['name']
        if ('StatefulPartitionedCall' in out_name): # This is a TF2 model
            boxes_idx, classes_idx, scores_idx = 1, 3, 0
        else: # This is a TF1 model
            boxes_idx, classes_idx, scores_idx = 0, 1, 2

        if model_type == "ssd":
            # Retrieve detection results
            boxes = self.interpreter.get_tensor(output_details[boxes_idx]['index'])[0] # Bounding box coordinates of detected objects
            classes = self.interpreter.get_tensor(output_details[classes_idx]['index'])[0] # Class index of detected objects
            scores = self.interpreter.get_tensor(output_details[scores_idx]['index'])[0] # Confidence of detected objects

            # Create custom response
            detection_response = {}
            detection_list = []
            for i in range(len(scores)):
                label_dict = DETECTION_RESPONSE_BB.copy()
                if ((scores[i] > threshold) and (scores[i] <= 1.0)):
                    ymin = int(max(1,(boxes[i][0] * input_img_height)))
                    xmin = int(max(1,(boxes[i][1] * input_img_width)))
                    ymax = int(min(input_img_height,(boxes[i][2] * input_img_height)))
                    xmax = int(min(input_img_width,(boxes[i][3] * input_img_width)))
                    label_dict["confidence"] = scores[i]
                    label_dict["label_bounding_box"] = [{"x": xmin, "y": ymin}, {"x": xmax, "y": ymax}]
                    label_dict["label_class_name"] = labels_list[int(classes[i])]
                    detection_list.append(label_dict)
            processing_time = stop_time - start_time
            detection_response= {"detection": detection_list, "processing_time": processing_time}
            return detection_response
        else:
            output_data = self.interpreter.get_tensor(output_details[0]['index'])
            results = np.squeeze(output_data)
            top_k = results.argsort()[-5:][::-1]
            detection_list = []
            for i in top_k:
                print(labels_list[i])
                detection_list.append(' '.join(labels_list[i].split()[1:]))
            processing_time = stop_time - start_time
            detection_response = {"detection": detection_list, "processing_time": processing_time}
            return detection_response
