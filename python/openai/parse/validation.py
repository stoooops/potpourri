class Validation:
    def evaluate(self, text: str) -> bool:
        return True


class StartsWithRobotEmoji(Validation):
    def evaluate(self, text: str) -> bool:
        return text.startswith("🤖")

    def no(self, text: str) -> bool:
        if not self.evaluate(text):
            return True
        raise ValueError(f"Expected text to start with '🤖', but got '{text}'")

    def yes(self, text: str) -> bool:
        if self.evaluate(text):
            return True
        raise ValueError(f"Expected text to start with '🤖', but got '{text}'")
