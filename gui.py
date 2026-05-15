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
        # Image loading 
    def load_image(self) -> None:
        try:
            file_path = filedialog.askopenfilename(
                title="Select an image",
                filetypes=[
                    ("Image files", "*.jpg *.jpeg *.png *.bmp"),
                    ("JPEG files", "*.jpg *.jpeg"),
                    ("PNG files", "*.png"),
                    ("BMP files", "*.bmp"),
                ],
            )

            if not file_path:
                return

            image = self.processor.load_image(file_path)
            resized_img = self.processor.resize_keep_aspect_ratio(image)
            changed_img, boxes = self.processor.generate_modified_image(resized_img)

            self.original_img = resized_img
            self.modified_img = changed_img
            self.diff_boxes = boxes

            self.state.reset_game()
            self.reveal_btn.config(state=tk.NORMAL)

            self.show_images()
            self.update_text()

            self.msg_label.config(
                text="Find all 5 differences. You can make 3 mistakes."
            )

        except (FileNotFoundError, ValueError, RuntimeError) as error:
            messagebox.showerror("Image Error", str(error))
        except Exception as error:
            messagebox.showerror("Error", f"Something went wrong:\n{error}")

    def check_click(self, event: tk.Event) -> None:
        # check the clicks
        if self.original_img is None:
            messagebox.showinfo("No Image", "Please load an image first.")
            return

        if self.state.game_over:
            self.msg_label.config(
                text="Load a new image to play again."
            )
            return

        img_x, img_y = self.canvas_to_image(event.x, event.y)
        clicked_index = self.find_difference(img_x, img_y)

        if clicked_index is not None:
            self.state.add_found(clicked_index)
            self.draw_circle(clicked_index, "red")
            self.msg_label.config(text="Nice! You found a difference.")

            if self.state.finished():
                self.state.game_over = True
                self.msg_label.config(text="Congratulations! You found all 5 differences.")
                messagebox.showinfo(
                    "Round Complete",
                    "Congratulations! You found all 5 differences."
                )

        else:
            self.state.add_wrong()
            left_chance = self.state.max_wrong - self.state.wrong

            if self.state.game_over:
                self.msg_label.config(
                    text="Game over! Press Reveal or load a new image."
                )
                messagebox.showwarning(
                    "Game Over",
                    "You made 3 mistakes. No more guesses allowed."
                )
            else:
                self.msg_label.config(
                    text=f"Wrong spot. You have {left_chance} mistake(s) left."
                )

        self.update_text()

    def canvas_to_image(self, canvas_x: int, canvas_y: int) -> tuple[int, int]:
        # Convert canvas position to image position.
        img_h, img_w = self.modified_img.shape[:2]

        x_gap = (520 - img_w) // 2
        y_gap = (390 - img_h) // 2

        return canvas_x - x_gap, canvas_y - y_gap

    def image_to_canvas(self, img_x: int, img_y: int) -> tuple[int, int]:
        # Convert image position to canvas position.
        img_h, img_w = self.modified_img.shape[:2]

        x_gap = (520 - img_w) // 2
        y_gap = (390 - img_h) // 2

        return img_x + x_gap, img_y + y_gap

    def find_difference(self, click_x: int, click_y: int) -> int | None:
        # Find the clicked differences
        tolerance = 12

        for index, (x, y, w, h) in enumerate(self.diff_boxes):
            if self.state.already_found(index):
                continue

            inside_box = (
                x - tolerance <= click_x <= x + w + tolerance
                and y - tolerance <= click_y <= y + h + tolerance
            )

            if inside_box:
                return index

        return None

    def draw_circle(self, index: int, color: str) -> None:
        # Display circles on images
        x, y, w, h = self.diff_boxes[index]

        center_x = x + w // 2
        center_y = y + h // 2
        radius = max(w, h) // 2 + 10

        canvas_x, canvas_y = self.image_to_canvas(center_x, center_y)

        for canvas in (self.left_canvas, self.right_canvas):
            canvas.create_oval(
                canvas_x - radius,
                canvas_y - radius,
                canvas_x + radius,
                canvas_y + radius,
                outline=color,
                width=3
            )

    def reveal_differences(self) -> None:
        # display the not found differences.
        if self.original_img is None:
            messagebox.showinfo("No Image", "Please load an image first.")
            return

        try:
            for index in range(len(self.diff_boxes)):
                if not self.state.already_found(index):
                    self.draw_circle(index, "blue")
                    self.state.add_found(index)

            self.state.game_over = True
            self.state.reveal_used = True

            self.msg_label.config(text="Remaining differences are shown in blue.")
            self.update_text()

        except Exception as error:
            messagebox.showerror(
                "Reveal Error",
                f"Could not reveal differences:\n{error}"
            )
