# This file is for thr track of the game progress

class GameState: # Handles game state

    def __init__(self, total_diff: int = 5, max_wrong: int = 3) -> None:
        self.total_diff = total_diff
        self.max_wrong = max_wrong
        self.reset_game()

    def reset_game(self) -> None: # Reset the game
        self.found = set()
        self.wrong = 0
        self.game_over = False
        self.reveal_used = False

    def add_found(self, index: int) -> None: # Save a found difference
        self.found.add(index)

    def already_found(self, index: int) -> bool: # Checking the difference was already found
        return index in self.found

    def add_wrong(self) -> None: # Adding one wrong click
        self.wrong += 1

        if self.wrong >= self.max_wrong: # Stop the game after 3 wrong clicks
            self.game_over = True

    def left_diff(self) -> int:  # remaining differences
        return self.total_diff - len(self.found)

    def finished(self) -> bool: # Checking all differences are found
        return len(self.found) == self.total_diff
