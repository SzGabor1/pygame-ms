from PIL import Image
import os

# Load the image
image_path = "Sprite-0003.png"
image = Image.open(image_path)

# Get the size of the image
width, height = image.size

# Define the size of the small images
size = 64

# Loop through the image, cropping and saving small images
count = 0  # start from 0
for y in range(0, height, size):
    for x in range(0, width, size):
        # Crop the image
        box = (x, y, x + size, y + size)
        cropped_image = image.crop(box)

        # Save the image with a sequential number
        filename = f"{count}.png"  # PNG format
        cropped_image.save(filename)

        count += 1

print("Done splitting image!")
