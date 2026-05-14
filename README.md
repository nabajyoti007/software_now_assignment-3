# Spot the Difference Game – HIT137 Assignment 3

## Project Overview

This project is a desktop-based "Spot the Difference" game developed using Python, Tkinter, and OpenCV. The program automatically creates a modified version of an image with hidden differences, and the player must identify those differences by clicking on the modified image.

The application was developed using Object-Oriented Programming (OOP) concepts including encapsulation, inheritance, and polymorphism.

---

## Features

- Load images using a file selection dialog
- Supports JPG, JPEG, PNG, and BMP images
- Displays original and modified images side by side
- Automatically generates exactly 5 hidden differences
- Random position and random difference type on every image load
- Prevents overlapping difference regions
- Uses multiple image alteration techniques:
  - Colour Shift
  - Blur Patch
  - Brightness Change
  - Invert Patch
- Correct clicks are marked with red circles
- Reveal button shows remaining differences in blue
- Mistake counter with maximum 3 attempts
- Game ends after 3 mistakes
- Game resets when a new image is loaded
- Basic exception handling for invalid files and unexpected errors

---

## Project Structure

```text
SpotTheDifference/
│
├── main.py
├── gui.py
├── image_processor.py
├── alterations.py
├── game_state.py
├── README.md
├── requirements.txt
├── github_link.txt
├── sample_images/
└── screenshots/
