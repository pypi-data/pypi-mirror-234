from hashtagger import hashtagger

# Create an instance of YourLibrary
your_library = hashtagger()

# Specify the path to the image you want to process
image_path = "C:\\Users\\Tina\\OneDrive\\Desktop\\car.jpg"  # Replace with the path to your image

try:
    # Use the recognize_objects method to recognize objects in the image
    decoded_predictions = your_library.recognize_objects(image_path)

    # Use the generate_tags method to generate tags for the recognized objects
    tags = your_library.generate_tags(decoded_predictions)

    print("Recognized objects and tags:")
    for tag in tags:
        print(tag)

except Exception as e:
    print(f"An error occurred: {e}")
