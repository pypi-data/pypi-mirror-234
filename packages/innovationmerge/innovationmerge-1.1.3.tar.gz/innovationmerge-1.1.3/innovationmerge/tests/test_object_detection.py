import os
from innovationmerge import EdgeObjectDetectionTfLite
from innovationmerge.src.utils.responses import load_labels, read_image

# Declare paths
cwd = os.getcwd()

input_image_path = os.path.join(cwd, "data", "testdata", "images.jpg")


# edge object detection ssd
def test_edge_object_detect_ssd():
    threshold = 0.6
    model_type="ssd"
    model_path = os.path.join(cwd, "models", "edge", "ssd_mobilenet_v3_large_coco_2020_01_14")
    model_file_path = os.path.join(model_path, "model.tflite")
    labels_path = os.path.join(model_path, "labels.txt")
    labels = load_labels(labels_path)
    cv2_image = read_image(input_image_path)
    detect_objects = EdgeObjectDetectionTfLite(model_file_path)
    detection_result = detect_objects.detect(cv2_image, labels, threshold, model_type)
    print(detection_result)
    assert detection_result.get('detection')[0].get('label_class_name') == "cat"


# edge object detection mobilenet
def test_edge_object_detect_mobilenet():
    threshold = 0.6
    model_type="mobilenet"
    model_path = os.path.join(cwd, "models", "edge", "mobilenet_v2_1.0_224_quant")
    model_file_path = os.path.join(model_path, "model.tflite")
    labels_path = os.path.join(model_path, "labels.txt")
    labels = load_labels(labels_path)
    cv2_image = read_image(input_image_path)
    detect_objects = EdgeObjectDetectionTfLite(model_file_path)
    detection_result = detect_objects.detect(cv2_image, labels, threshold, model_type)
    print(detection_result)
    assert len(detection_result.get('detection')) > 0