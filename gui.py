# This file creates the game window and handles the player actions

import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk
from game_state import GameState
from image_processor import ImageProcessor


class GameApp(tk.Tk):                         # Main window

    def __init__(self) -> None:
        super().__init__()

        self.title("Spot the Difference Game")
        self.geometry("1180x700")
        self.resizable(False, False)
        self.configure(bg="#1e1e2f")

        self.processor = ImageProcessor()
        self.state = GameState(total_diff=5, max_wrong=3)

        self.original_img = None
        self.modified_img = None
        self.diff_boxes = []

        self.left_photo = None
        self.right_photo = None

        self.make_window()

    # visual design of the game window

    def make_window(self) -> None:
        title = tk.Label(
            self,
            text="Spot the Difference Game",
            font=("Arial", 24, "bold"),
            bg="#1e1e2f",
            fg="#ffffff"
        )
        title.pack(pady=(18, 4))

        subtitle = tk.Label(
            self,
            text="Find all 5 hidden differences before making 3 mistakes!",
            font=("Arial", 12),
            bg="#1e1e2f",
            fg="#c7c7ff"
        )
        subtitle.pack(pady=(0, 12))

        top_area = tk.Frame(self, bg="#2d2d44", padx=14, pady=12)
        top_area.pack(pady=5)

        self.load_btn = tk.Button(
            top_area,
            text="Load Image",
            width=18,
            font=("Arial", 11, "bold"),
            bg="#4e79e6",
            fg="white",
            activebackground="#45a049",
            activeforeground="white",
            relief=tk.RAISED,
            command=self.load_image
        )
        self.load_btn.grid(row=0, column=0, padx=10)

        self.reveal_btn = tk.Button(
            top_area,
            text="Reveal",
            width=18,
            font=("Arial", 11, "bold"),
            bg="#057d35",
            fg="white",
            activebackground="#1976d2",
            activeforeground="white",
            relief=tk.RAISED,
            command=self.reveal_differences,
            state=tk.DISABLED
        )
        self.reveal_btn.grid(row=0, column=1, padx=10)

        self.left_label = tk.Label(
            top_area,
            text="Remaining: 0",
            font=("Arial", 12, "bold"),
            bg="#2d2d44",
            fg="#ffeb3b"
        )
        self.left_label.grid(row=0, column=2, padx=20)

        self.wrong_label = tk.Label(
            top_area,
            text="Mistakes: 0 / 3",
            font=("Arial", 12, "bold"),
            bg="#2d2d44",
            fg="#ff7675"
        )
        self.wrong_label.grid(row=0, column=3, padx=20)

        self.msg_label = tk.Label(
            self,
            text="Load an image to start.",
            font=("Arial", 13, "bold"),
            bg="#1e1e2f",
            fg="#ffffff"
        )
        self.msg_label.pack(pady=12)

        image_area = tk.Frame(self, bg="#1e1e2f")
        image_area.pack(pady=10)

        left_area = tk.Frame(
            image_area,
            bg="#2d2d44",
            padx=12,
            pady=12,
            highlightbackground="#6c63ff",
            highlightthickness=3
        )
        left_area.grid(row=0, column=0, padx=18)

        right_area = tk.Frame(
            image_area,
            bg="#2d2d44",
            padx=12,
            pady=12,
            highlightbackground="#00cec9",
            highlightthickness=3
        )
        right_area.grid(row=0, column=1, padx=18)

        tk.Label(
            left_area,
            text="Original Image",
            font=("Arial", 14, "bold"),
            bg="#2d2d44",
            fg="#ffffff"
        ).pack(pady=(0, 8))

        self.left_canvas = tk.Canvas(
            left_area,
            width=520,
            height=390,
            bg="#111111",
            highlightthickness=2,
            highlightbackground="#ffffff"
        )
        self.left_canvas.pack()

        tk.Label(
            right_area,
            text="Modified Image - Click Here",
            font=("Arial", 14, "bold"),
            bg="#2d2d44",
            fg="#ffffff"
        ).pack(pady=(0, 8))

        self.right_canvas = tk.Canvas(
            right_area,
            width=520,
            height=390,
            bg="#111111",
            highlightthickness=2,
            highlightbackground="#ffffff",
            cursor="crosshair"
        )
        self.right_canvas.pack()

        self.right_canvas.bind("<Button-1>", self.check_click)

    def show_images(self) -> None: # Showing the original and modified image
        if self.original_img is None or self.modified_img is None:
            return

        self.left_canvas.delete("all")
        self.right_canvas.delete("all")

        original_rgb = cv2.cvtColor(self.original_img, cv2.COLOR_BGR2RGB)
        modified_rgb = cv2.cvtColor(self.modified_img, cv2.COLOR_BGR2RGB)

        original_pil = Image.fromarray(original_rgb)
        modified_pil = Image.fromarray(modified_rgb)

        self.left_photo = ImageTk.PhotoImage(original_pil)
        self.right_photo = ImageTk.PhotoImage(modified_pil)

        self.left_canvas.create_image(260, 195, image=self.left_photo, anchor=tk.CENTER)
        self.right_canvas.create_image(260, 195, image=self.right_photo, anchor=tk.CENTER)

    def update_text(self) -> None:   # Update the counters
        self.left_label.config(text=f"Remaining: {self.state.left_diff()}")
        self.wrong_label.config(text=f"Mistakes: {self.state.wrong} / {self.state.max_wrong}")
