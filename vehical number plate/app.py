import cv2

try:
    yolo_weights_path = 'path_to_yolo_weights'
    yolo_cfg_path = 'path_to_yolo_cfg'
    
    net = cv2.dnn.readNet(yolo_weights_path, yolo_cfg_path)
    layer_names = net.getLayerNames()
    
    # Ensure net.getUnconnectedOutLayers() returns a list of integers
    unconnected_layers = net.getUnconnectedOutLayers()
    if isinstance(unconnected_layers, list) and all(isinstance(i, int) for i in unconnected_layers):
        output_layers = [layer_names[i - 1] for i in unconnected_layers]
        print("YOLO model loaded successfully")
    else:
        raise ValueError("Unexpected output from net.getUnconnectedOutLayers()")
    
except cv2.error as e:
    print(f"OpenCV Error: {e}")
except Exception as e:
    print(f"Error: {e}")
