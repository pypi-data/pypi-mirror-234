import argparse
import re
from io import BytesIO
from pathlib import Path
from random import randrange

from PIL import Image


def degrade(image: Image, passes: int) -> Image:
    # Store the original image dimensions
    orig_w = image.width
    orig_h = image.height

    # Create in-memory buffer to save temporary files to
    buffer = BytesIO()

    for _ in range(passes):
        # Calculate a random new size to distort the image
        skew_w = randrange(orig_w // 2, orig_w * 2)
        skew_h = randrange(orig_h // 2, orig_h * 2)

        skewed = image.resize((skew_w, skew_h), Image.NEAREST)

        # Save and reopen the image to create artifacts
        buffer.seek(0)
        skewed.save(buffer, "JPEG", quality=randrange(5, 30))

        buffer.seek(0)
        image = Image.open(buffer)

    # Resize the image to its original dimensions
    return image.resize((orig_w, orig_h), Image.NEAREST)


def main():
    parser = argparse.ArgumentParser(description="Add comical JPEG compression to an image.")
    parser.add_argument("image", type=Path, help="Path to the input image.")
    parser.add_argument("-p", "--passes", type=int, default=1, help="Number of degradation passes.")

    args = parser.parse_args()

    infile = args.image
    passes = args.passes

    # Parse the filename and possible previous passes value from the filename
    match = re.search(r"^(.*?)(?:\.(\d+))?$", infile.stem)
    filename, level = match.groups()

    # Get the current level (or 0) and add the passes
    level = int(level) if level else 0
    level += passes

    # Degrade the image
    image = Image.open(infile)
    comically_degraded_image = degrade(image, passes)

    # Build the outfile name ([name].[passes].jpeg) and save the image
    outfile = infile.with_name(f"{filename}.{level}.jpeg")
    comically_degraded_image.save(outfile, "JPEG", quality=20)


if __name__ == "__main__":
    main()
