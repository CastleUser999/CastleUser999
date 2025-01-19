import tkinter as tk
import random

class ClickerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Clicker Game")
        self.score = 0
        self.multiplier = 1
        self.multiplier_cost = 10
        self.auto_clicker_count = 0
        self.auto_clicker_cost = 50
        self.auto_clicker_interval = 1  # seconds for auto-clicker to increment the score
        self.golden_cursor_active = False
        self.golden_cursor_interval = 9  # Time in seconds for the Golden Cursor to appear
        self.golden_cursor_clicks = 0
        self.achievements = []  # Track unlocked achievements
        self.manual_clicks = 0  # Count manual clicks to check for Diamond Click

        # Create and place the score label
        self.score_label = tk.Label(root, text=f"Score: {self.score}", font=("Arial", 24))
        self.score_label.pack(pady=20)

        # Create and place the multiplier label
        self.multiplier_label = tk.Label(root, text=f"Multiplier: x{self.multiplier}", font=("Arial", 18))
        self.multiplier_label.pack(pady=10)

        # Create and place the auto-clicker label
        self.auto_clicker_label = tk.Label(root, text=f"Auto-Clickers: {self.auto_clicker_count}", font=("Arial", 18))
        self.auto_clicker_label.pack(pady=10)

        # Create and place the achievements label
        self.achievement_label = tk.Label(root, text="Achievements:", font=("Arial", 18))
        self.achievement_label.pack(pady=10)
        self.achievement_list = tk.Text(root, height=6, width=40, font=("Arial", 12))
        self.achievement_list.pack(pady=10)

        # Create and place the click button
        self.click_button = tk.Button(root, text="Click Me!", font=("Arial", 18), command=self.increment_score_manually)
        self.click_button.pack(pady=10)

        # Create and place the buy multiplier button
        self.buy_multiplier_button = tk.Button(
            root,
            text=f"Buy Multiplier (Cost: {self.multiplier_cost})",
            font=("Arial", 18),
            command=self.buy_multiplier
        )
        self.buy_multiplier_button.pack(pady=10)

        # Create and place the buy auto-clicker button
        self.buy_auto_clicker_button = tk.Button(
            root,
            text=f"Buy Auto-Clicker (Cost: {self.auto_clicker_cost})",
            font=("Arial", 18),
            command=self.buy_auto_clicker
        )
        self.buy_auto_clicker_button.pack(pady=10)

        # Create and place the reset button
        self.reset_button = tk.Button(root, text="Reset", font=("Arial", 18), command=self.reset_game)
        self.reset_button.pack(pady=10)

        # Golden Cursor Button
        self.golden_cursor_button = tk.Button(
            root,
            text="Golden Cursor!",
            font=("Arial", 18),
            bg="gold",
            command=self.click_golden_cursor
        )
        self.golden_cursor_button.place_forget()  # Hide it initially

        # Start timers
        self.start_auto_clickers()
        self.spawn_golden_cursor()

    def increment_score_manually(self):
        """Increments the score based on the multiplier (manual click)."""
        self.score += self.multiplier
        self.manual_clicks += 1
        self.check_achievements()
        self.update_labels()

    def buy_multiplier(self):
        """Allows the player to buy a multiplier if they have enough points."""
        if self.score >= self.multiplier_cost:
            self.score -= self.multiplier_cost
            self.multiplier += 1
            self.multiplier_cost += 10  # Increase the cost of the next multiplier
            self.check_achievements()
            self.update_labels()
        else:
            self.show_message("Not enough points to buy a multiplier!")

    def buy_auto_clicker(self):
        """Allows the player to buy an auto-clicker if they have enough points."""
        if self.score >= self.auto_clicker_cost:
            self.score -= self.auto_clicker_cost
            self.auto_clicker_count += 1
            self.auto_clicker_cost += 50  # Increase the cost of the next auto-clicker
            self.check_achievements()
            self.update_labels()
        else:
            self.show_message("Not enough points to buy an auto-clicker!")

    def start_auto_clickers(self):
        """Automatically increases the score based on the number of auto-clickers."""
        if self.auto_clicker_count > 0:
            self.score += self.auto_clicker_count * self.multiplier
            self.check_achievements()
            self.update_labels()
        self.root.after(int(self.auto_clicker_interval * 1000), self.start_auto_clickers)

    def spawn_golden_cursor(self):
        """Spawns the Golden Cursor every set interval (now 9 seconds)."""
        if not self.golden_cursor_active:
            self.golden_cursor_active = True
            self.golden_cursor_clicks = 0  # Reset click count
            # Randomize the position
            x = random.randint(50, 300)
            y = random.randint(50, 300)
            self.golden_cursor_button.place(x=x, y=y)
            self.root.after(10000, self.hide_golden_cursor)  # Hide it after 10 seconds
        self.root.after(self.golden_cursor_interval * 1000, self.spawn_golden_cursor)

    def hide_golden_cursor(self):
        """Hides the Golden Cursor."""
        self.golden_cursor_button.place_forget()
        self.golden_cursor_active = False

    def click_golden_cursor(self):
        """Handles clicking the Golden Cursor."""
        if self.golden_cursor_active:
            self.golden_cursor_clicks += 1
            bonus = (self.golden_cursor_clicks * self.multiplier) * 2
            self.score += bonus
            self.show_message(f"Golden Cursor clicked! Bonus: {bonus}")
            self.hide_golden_cursor()  # Hide after clicking
            self.check_achievements()
            self.update_labels()

    def reset_game(self):
        """Resets the game to its initial state."""
        self.score = 0
        self.multiplier = 1
        self.multiplier_cost = 10
        self.auto_clicker_count = 0
        self.auto_clicker_cost = 50
        self.golden_cursor_active = False
        self.achievements = []
        self.manual_clicks = 0
        self.update_achievements_list()
        self.update_labels()

    def check_achievements(self):
        """Checks if any achievements are unlocked and adds them to the list."""
        achievement_milestones = [
            (100, "Reached 100 Points!"),
            (500, "Reached 500 Points!"),
            (1000, "Reached 1000 Points!"),
            (10, "Bought 10 Multipliers!"),
            (5, "Bought 5 Auto-Clickers!"),
            (1, "Clicked the Golden Cursor!"),
            (100, "Diamond Click (100 Points Without Clicking)")
        ]

        for milestone, achievement in achievement_milestones:
            if achievement not in self.achievements:
                if (
                    (achievement == "Diamond Click (100 Points Without Clicking)" and self.score >= milestone and self.manual_clicks == 0)
                    or (achievement.startswith("Reached") and self.score >= milestone)
                    or (achievement.startswith("Bought 10") and self.multiplier >= milestone)
                    or (achievement.startswith("Bought 5") and self.auto_clicker_count >= milestone)
                    or (achievement.startswith("Clicked") and self.golden_cursor_clicks >= milestone)
                ):
                    self.achievements.append(achievement)
                    self.show_message(f"Achievement Unlocked: {achievement}")
                    self.update_achievements_list()

    def update_labels(self):
        """Updates all the labels in the game."""
        self.score_label.config(text=f"Score: {self.score}")
        self.multiplier_label.config(text=f"Multiplier: x{self.multiplier}")
        self.auto_clicker_label.config(text=f"Auto-Clickers: {self.auto_clicker_count}")
        self.buy_multiplier_button.config(text=f"Buy Multiplier (Cost: {self.multiplier_cost})")
        self.buy_auto_clicker_button.config(text=f"Buy Auto-Clicker (Cost: {self.auto_clicker_cost})")

    def update_achievements_list(self):
        """Updates the list of unlocked achievements."""
        self.achievement_list.delete(1.0, tk.END)
        if self.achievements:
            for achievement in self.achievements:
                self.achievement_list.insert(tk.END, f"{achievement}\n")
        else:
            self.achievement_list.insert(tk.END, "No achievements unlocked yet.")

    def show_message(self, message):
        """Displays a temporary message in the window."""
        popup = tk.Toplevel(self.root)
        popup.title("Achievement!")
        tk.Label(popup, text=message, font=("Arial", 16)).pack(pady=10)
        tk.Button(popup, text="OK", command=popup.destroy).pack(pady=5)


# Main loop to run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = ClickerGame(root)
    root.mainloop()
