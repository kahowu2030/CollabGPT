import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

def text_to_image(input_file, output_file, font_size=12, max_width=800, background_color=(255, 255, 255), text_color=(0, 0, 0), padding=10, supersampling_factor=4):
    # Open the text file and read its content
    with open(input_file, 'r', encoding='utf-8', errors='replace') as file:
        text_content = file.read()

    # Set the font style and size
    font_path = "/System/Library/Fonts/HelveticaNeue.ttc"  # Path to the desired font file
    font = ImageFont.truetype(font_path, font_size * supersampling_factor)  # Load the font using the given font path and size

    # Wrap the text to fit within the specified max width
    max_chars_per_line = (max_width - 2 * padding) // font_size
    wrapped_text = textwrap.fill(text_content, max_chars_per_line)
    lines = wrapped_text.splitlines()

    # Calculate the text dimensions
    max_line_width = 0
    total_height = 0
    for line in lines:
        line_width, line_height = font.getsize(line)
        max_line_width = max(max_line_width, line_width)
        total_height += line_height

    # Create a new high-resolution image with the calculated size and background color
    image = Image.new('RGB', (max_line_width + 2 * padding * supersampling_factor, total_height + 2 * padding * supersampling_factor), background_color)
    draw = ImageDraw.Draw(image)

    # Draw the text on the high-resolution image
    current_y = padding * supersampling_factor
    for line in lines:
        try:
            draw.text((padding * supersampling_factor, current_y), line, fill=text_color, font=font)
        except UnicodeEncodeError:
            # Handle encoding errors by replacing unsupported characters
            sanitized_line = ''.join(c if ord(c) < 128 else '' for c in line)
            draw.text((padding * supersampling_factor, current_y), sanitized_line, fill=text_color, font=font)
        current_y += font.getsize(line)[1]

    # Scale down the high-resolution image to the target resolution using a high-quality resampling method
    target_size = (max_line_width // supersampling_factor + 2 * padding, total_height // supersampling_factor + 2 * padding)
    image = image.resize(target_size, Image.ANTIALIAS)

    # Save the resulting image
    image.save(output_file)

# Get the current directory
directory = os.getcwd()

# Iterate over files in the directory
for file_name in os.listdir(directory):
    if file_name.endswith(".txt"):
        # Generate the input and output file paths
        input_file = os.path.join(directory, file_name)
        output_file = os.path.splitext(input_file)[0] + ".png"

        # Convert the text file to an image
        text_to_image(input_file, output_file, font_size=16)