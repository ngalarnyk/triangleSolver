import tkinter as tk
from tkinter import messagebox
import math
import random

class TriangleCalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Triangle Angle and Side Calculator")
        self.geometry("400x350")

        # Initialize variables for progress tracking
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.consecutive_correct = 0
        self.total_exercises = 0

        # Create GUI widgets
        self.create_widgets()

    def create_widgets(self):
        # Create sliders for adjusting angle measurements
        self.angle1_label = tk.Label(self, text="Angle 1:")
        self.angle1_label.grid(row=0, column=0)
        self.angle1_slider = tk.Scale(self, from_=0, to=180, orient=tk.HORIZONTAL)
        self.angle1_slider.grid(row=0, column=1)

        self.angle2_label = tk.Label(self, text="Angle 2:")
        self.angle2_label.grid(row=1, column=0)
        self.angle2_slider = tk.Scale(self, from_=0, to=180, orient=tk.HORIZONTAL)
        self.angle2_slider.grid(row=1, column=1)

        # Create sliders for adjusting side lengths
        self.side1_label = tk.Label(self, text="Side 1:")
        self.side1_label.grid(row=2, column=0)
        self.side1_slider = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL)
        self.side1_slider.grid(row=2, column=1)

        self.side2_label = tk.Label(self, text="Side 2:")
        self.side2_label.grid(row=3, column=0)
        self.side2_slider = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL)
        self.side2_slider.grid(row=3, column=1)

        # Create a button to generate a random triangle
        self.generate_button = tk.Button(self, text="Generate Triangle", command=self.generate_triangle)
        self.generate_button.grid(row=4, column=0, columnspan=2)

        # Create a button to calculate the unknown angle
        self.calculate_button = tk.Button(self, text="Calculate Angle", command=self.calculate_unknown_angle)
        self.calculate_button.grid(row=5, column=0, columnspan=2)

        # Create a button to calculate the missing side
        self.calculate_side_button = tk.Button(self, text="Calculate Side", command=self.calculate_missing_side)
        self.calculate_side_button.grid(row=6, column=0, columnspan=2)

        # Create an entry field for users to input their solution
        self.unknown_angle_entry_label = tk.Label(self, text="Enter unknown angle:")
        self.unknown_angle_entry_label.grid(row=7, column=0)
        self.unknown_angle_entry = tk.Entry(self)
        self.unknown_angle_entry.grid(row=7, column=1)

        # Create a label to provide feedback on the user's solution
        self.feedback_label = tk.Label(self, text="")
        self.feedback_label.grid(row=8, column=0, columnspan=2)

        # Create a label to display the result
        self.result_label = tk.Label(self, text="")
        self.result_label.grid(row=9, column=0, columnspan=2)

        # Create a label to display progress
        self.progress_label = tk.Label(self, text="Progress: 0/0")
        self.progress_label.grid(row=10, column=0, columnspan=2)

        # Create a label to display scoreboard
        self.scoreboard_label = tk.Label(self, text="Scoreboard: Correct: 0, Incorrect: 0, Consecutive: 0")
        self.scoreboard_label.grid(row=11, column=0, columnspan=2)

    def generate_triangle(self):
        # Generate random angles and side lengths for a triangle
        angle1 = random.randint(1, 179)
        angle2 = random.randint(1, 179 - angle1)
        side1 = random.randint(1, 100)
        side2 = random.randint(1, 100)

        # Set the values on the sliders
        self.angle1_slider.set(angle1)
        self.angle2_slider.set(angle2)
        self.side1_slider.set(side1)
        self.side2_slider.set(side2)

    def calculate_unknown_angle(self):
        # Get the known angles and sides from the input fields
        try:
            angle1 = self.angle1_slider.get()
            angle2 = self.angle2_slider.get()
            side1 = self.side1_slider.get()
            side2 = self.side2_slider.get()
        except ValueError:
            self.result_label.config(text="Please enter valid numbers")
            return

        # Method 1: Angle Sum Property
        unknown_angle_sum_property = 180 - angle1 - angle2
        
        # Method 2: Trigonometric Calculation (Law of Sines)
        if side1 != 0 and side2 != 0:
            unknown_angle_trig = math.degrees(math.asin((side1 * math.sin(math.radians(angle1))) / side2))
        else:
            unknown_angle_trig = None

        # Display the results
        result_text = "Results:\n"
        result_text += f"Angle Sum Property: {unknown_angle_sum_property} degrees\n"
        result_text += f"Trigonometric Calculation (Law of Sines): {unknown_angle_trig} degrees" if unknown_angle_trig is not None else ""
        self.result_label.config(text=result_text)

        # Check if the user's solution is correct
        correct_angle = 180 - angle1 - angle2
        user_angle = self.unknown_angle_entry.get()
        if user_angle.strip() != "":
            try:
                user_angle = float(user_angle)
                if abs(user_angle - correct_angle) < 1e-6:
                    self.feedback_label.config(text="Correct!", fg="green")
                    self.correct_answers += 1
                    self.consecutive_correct += 1
                else:
                    self.feedback_label.config(text="Incorrect, try again.", fg="red")
                    self.incorrect_answers += 1
                    self.consecutive_correct = 0
            except ValueError:
                self.feedback_label.config(text="Please enter a valid number.", fg="red")

        # Update progress
        self.total_exercises += 1
        self.progress_label.config(text=f"Progress: {self.correct_answers}/{self.total_exercises}")

        # Update scoreboard
        self.update_scoreboard()

    def calculate_missing_side(self):
        # Get the known angles and sides from the input fields
        try:
            angle1 = self.angle1_slider.get()
            angle2 = self.angle2_slider.get()
            side1 = self.side1_slider.get()
            side2 = self.side2_slider.get()
        except ValueError:
            self.result_label.config(text="Please enter valid numbers")
            return

        # Calculate the missing side using the law of sines
        if angle1 != 0 and angle2 != 0:
            if side1 != 0:
                missing_side = side1 * math.sin(math.radians(angle2)) / math.sin(math.radians(angle1))
                result_text = f"Missing side (calculated using Law of Sines): {missing_side:.2f} units"
            elif side2 != 0:
                missing_side = side2 * math.sin(math.radians(angle1)) / math.sin(math.radians(angle2))
                result_text = f"Missing side (calculated using Law of Sines): {missing_side:.2f} units"
            else:
                result_text = "Please specify at least one known side to calculate the missing side."
        else:
            result_text = "Please specify at least one known angle to calculate the missing side."

        # Display the result
        self.result_label.config(text=result_text)

    def update_scoreboard(self):
        # Update the scoreboard label
        scoreboard_text = f"Scoreboard: Correct: {self.correct_answers}, Incorrect: {self.incorrect_answers}, Consecutive: {self.consecutive_correct}"
        self.scoreboard_label.config(text=scoreboard_text)

def show_help():
    # Display educational content
    help_content = """
    Triangle Geometry Principles:
    - The sum of angles in a triangle is always 180 degrees.
    - Types of triangles:
        - Equilateral: All sides are equal.
        - Isosceles: Two sides are equal.
        - Scalene: No sides are equal.
        
    Methods for Calculating Unknown Angles:
    - Angle Sum Property: Subtract the sum of known angles from 180 degrees.
    - Trigonometric Calculation (Law of Sines): Use the Law of Sines to calculate unknown angles based on side lengths and known angles.
    """
    messagebox.showinfo("Help", help_content)

if __name__ == "__main__":
    app = TriangleCalculatorApp()
    app.mainloop()
