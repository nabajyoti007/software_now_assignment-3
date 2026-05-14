# This file is for the different image changes used in the game

from abc import ABC, abstractmethod
import random
import cv2
import numpy as np

class ImageAlteration(ABC):            # Abstract base class

    @abstractmethod                    #Apply a change to a selected part of the image
    def apply(self, image: np.ndarray, region: tuple[int, int, int, int]) -> None:
        raise NotImplementedError

class ColourShift(ImageAlteration):     #changes the colour of a selected image region

    def apply(self, image: np.ndarray, region: tuple[int, int, int, int]) -> None:
        x, y, w, h = region
        roi = image[y:y + h, x:x + w]

        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        hue_shift = random.randint(8, 18)
        hsv[:, :, 0] = (hsv[:, :, 0].astype(int) + hue_shift) % 180

        image[y:y + h, x:x + w] = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

class BlurPatch(ImageAlteration):       #Applies Gaussian blur to a selected image region

    def apply(self, image: np.ndarray, region: tuple[int, int, int, int]) -> None:
        x, y, w, h = region
        roi = image[y:y + h, x:x + w]

        blurred = cv2.GaussianBlur(roi, (9, 9), 0)
        image[y:y + h, x:x + w] = blurred

class BrightnessChange(ImageAlteration): #changes the brightness of a selected image region

    def apply(self, image: np.ndarray, region: tuple[int, int, int, int]) -> None:
        x, y, w, h = region
        roi = image[y:y + h, x:x + w]

        change = random.choice([-35, -25, 25, 35])
        adjusted = np.clip(roi.astype(np.int16) + change, 0, 255).astype(np.uint8)

        image[y:y + h, x:x + w] = adjusted

class InvertPatch(ImageAlteration):      #inverts a region

    def apply(self, image: np.ndarray, region: tuple[int, int, int, int]) -> None:
        x, y, w, h = region
        roi = image[y:y + h, x:x + w]

        inverted = cv2.bitwise_not(roi)
        blended = cv2.addWeighted(roi, 0.75, inverted, 0.25, 0)

        image[y:y + h, x:x + w] = blended

