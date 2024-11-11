import cv2
import numpy as np


class Detection():
    def detectgun(image=None):
        classes = ['weapon']
        model = cv2.dnn.readNet('Client_Side/yolov4.weights','Client_Side/yolov4.cfg')
        height,width,channel = image.shape

        blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        model.setInput(blob)

        layer_names = model.getLayerNames()
        output_layers = [layer_names[i - 1] for i in model.getUnconnectedOutLayers()]
        colors = np.random.uniform(0, 255, size=(len(classes), 3))
        outs = model.forward(output_layers)

        class_ids = []
        confidences = []
        boxes = []
        
        for out in outs:
            for detection in out:
                scores = detection[5:]  
                class_id = np.argmax(scores)
                confidence = detection[4]
                if confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    
                    h = int(detection[3] * height)
                    w = int(detection[2] * width)

                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    
                    # Clip bounding box to stay within the image dimensions, with 20px margin
                    x = max(0, x)
                    y = max(0, y)
                    w = min(width - x - 20, w)
                    h = min(height - y - 20, h)

                    # Recalculate the center after clipping the width and height
                    center_x = x + w // 2
                    center_y = y + h // 2

                    # Adjust the top-left corner to keep the bounding box centered
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        font = cv2.FONT_HERSHEY_PLAIN
        
        flag = 0
        
        for i in range(len(boxes)):
            if i in indexes:
                flag = 1
                x, y, w, h = boxes[i]                
                label = str(classes[class_ids[i]])
                color = colors[class_ids[i]]
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                cv2.putText(image, label, (x, y + 30), font, 3, color, 3)
                
        return image,flag
