import os
import random
import cv2
import numpy as np

from alterations import ColourShift, BlurPatch, BrightnessChange, InvertPatch
class ImageProcessor:
    SUPPORTED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp")

    def __init__(self, display_width: int = 520, display_height: int = 390) -> None:
        self.display_width = display_width
        self.display_height = display_height
        self.alterations = [
            ColourShift(),
            BlurPatch(),
            BrightnessChange(),
            InvertPatch(),
        ]

    # Load an image from disk with exception handling.
    def load_image(self, file_path: str) -> np.ndarray:  
        if not file_path:
            raise ValueError("No image file was selected.")

        if not os.path.exists(file_path):
            raise FileNotFoundError("The selected image file does not exist.")

        if not file_path.lower().endswith(self.SUPPORTED_EXTENSIONS):
            raise ValueError("Unsupported file type. Please select JPG, PNG, or BMP.")

        image = cv2.imread(file_path)

        if image is None:
            raise ValueError("OpenCV could not read this image. Please try another file.")

        return image
    # Resize image to fit the display area
    def resize_keep_aspect_ratio(self, image: np.ndarray) -> np.ndarray: 
        if image is None or image.size == 0:
            raise ValueError("Cannot resize an empty image.")

        height, width = image.shape[:2]

        scale = min(self.display_width / width, self.display_height / height)
        new_width = max(1, int(width * scale))
        new_height = max(1, int(height * scale))

        return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

    def generate_modified_image(self, original: np.ndarray) -> tuple[np.ndarray, list[tuple[int, int, int, int]]]:
       #create the modified image
        if original is None or original.size == 0:
            raise ValueError("Cannot process an empty image.")

        modified = original.copy()
        regions: list[tuple[int, int, int, int]] = []

        image_height, image_width = original.shape[:2]
        min_size = max(25, min(image_width, image_height) // 14)
        max_size = max(40, min(image_width, image_height) // 7)

        attempts = 0
        max_attempts = 1000

        while len(regions) < 5 and attempts < max_attempts:
            attempts += 1

            w = random.randint(min_size, max_size)
            h = random.randint(min_size, max_size)

            if image_width <= w + 2 or image_height <= h + 2:
                raise ValueError("Image is too small to place five differences properly.")

            x = random.randint(0, image_width - w - 1)
            y = random.randint(0, image_height - h - 1)
            candidate = (x, y, w, h)

            if not self._overlaps_existing(candidate, regions, padding=15):
                alteration = random.choice(self.alterations)
                alteration.apply(modified, candidate)
                regions.append(candidate)

        if len(regions) != 5:
            raise RuntimeError("Could not generate 5 non-overlapping differences. Try a larger image.")

        return modified, regions

    def _overlaps_existing(
        self,
        candidate: tuple[int, int, int, int],
        existing_regions: list[tuple[int, int, int, int]],
        padding: int = 10,
    ) -> bool:
        
        #Check overlapping rectangles
        x1, y1, w1, h1 = candidate

        for x2, y2, w2, h2 in existing_regions:
            if not (
                x1 + w1 + padding < x2
                or x2 + w2 + padding < x1
                or y1 + h1 + padding < y2
                or y2 + h2 + padding < y1
            ):
                return True

        return False
