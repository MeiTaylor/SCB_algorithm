import cv2
import numpy as np

# Load the image
image = cv2.imread('1.jpg')

# Load the EAST text detector
net = cv2.dnn.readNet('frozen_east_text_detection.pb')

# Get the image dimensions
height, width, _ = image.shape

# Resizing the image
# The EAST text detector requires that our input image dimensions be multiples of 32
# So, we need to resize our images keeping this in mind
new_width = (width + 31) // 32 * 32
new_height = (height + 31) // 32 * 32

# Resize the image
image = cv2.resize(image, (new_width, new_height))

# Get the new image dimensions
height, width, _ = image.shape

# Create a blob from the image
blob = cv2.dnn.blobFromImage(image, 1.0, (width, height), (123.68, 116.78, 103.94), True, False)

# Set the input blob for the EAST text detector
net.setInput(blob)

# Get the output layers of the EAST text detector
output_layers = [
    'feature_fusion/Conv_7/Sigmoid',
    'feature_fusion/concat_3'
]

# Forward pass through the EAST text detector
scores, geometry = net.forward(output_layers)

# Threshold for scores
score_threshold = 0.5

# Resize factor
resized_factor = (width / new_width, height / new_height)

# Create an empty list for the detected boxes
boxes = []
confidences = []

# Loop over the rows
for y in range(0, scores.shape[2]):
    # Extract the scores (probabilities), followed by the geometrical
    # data used to derive potential bounding box coordinates that
    # surround text
    scores_data = scores[0, 0, y]
    x0_data = geometry[0, 0, y]
    x1_data = geometry[0, 1, y]
    x2_data = geometry[0, 2, y]
    x3_data = geometry[0, 3, y]
    angles_data = geometry[0, 4, y]

    # Loop over the number of columns
    for x in range(0, scores_data.shape[0]):
        # If our score does not have sufficient probability, ignore it
        if scores_data[x] < score_threshold:
            continue

        # Compute the offset factor as our resulting feature maps will
        # be 4x smaller than the input image
        offset_x, offset_y = x * 4.0, y * 4.0

        # Extract the rotation angle for the prediction and then
        # compute the sin and cosine
        angle = angles_data[x]
        cos = np.cos(angle)
        sin = np.sin(angle)

        # Use the geometry volume to derive the width and height of
        # the bounding box
        h = x0_data[x] + x2_data[x]
        w = x1_data[x] + x3_data[x]

        # Compute both the starting and ending (x, y)-coordinates for
        # the text prediction bounding box
        end_x = int(offset_x + (cos * x1_data[x]) + (sin * x2_data[x]))
        start_x = int(offset_x - (sin * x2_data[x]) + (cos * x1_data[x]))
        end_y = int(offset_y - (sin * x0_data[x]) + (cos * x3_data[x]))
        start_y = int(offset_y - (cos * x2_data[x]) - (sin * x0_data[x]))

        # Add the bounding box coordinates and probability score to
        # our respective lists
        boxes.append((start_x, start_y, end_x, end_y, scores_data[x]))
        confidences.append(scores_data[x])

# Apply non-maximum suppression
indices = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold, 0.4)

# Check if there is at least one detected bounding box
if len(indices) > 0:
    # Loop over the indices
    for i in indices.flatten():
        # Get the bounding box
        (start_x, start_y, end_x, end_y, score) = boxes[i]

        # Scale the bounding box coordinates based on the respective ratios
        start_x = int(start_x * resized_factor[0])
        start_y = int(start_y * resized_factor[1])
        end_x = int(end_x * resized_factor[0])
        end_y = int(end_y * resized_factor[1])

        # Draw the bounding box on the image
        cv2.rectangle(image, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

        # Extract the ROI
        roi = image[start_y:end_y, start_x:end_x]

        # Check if the ROI is not empty
        if roi.size != 0:
            # Save the ROI
            cv2.imwrite('./picture/roi_{}.jpg'.format(i), roi)

# Show the image
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
