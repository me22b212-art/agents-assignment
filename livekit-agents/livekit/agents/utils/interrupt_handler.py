import re

class InterruptHandler:
    def __init__(self):
        self.ignore_list = ["yeah", "ok", "okay", "hmm", "uh-huh", "right"]
        self.command_list = ["stop", "wait", "no", "pause", "hold on"]

    def normalize(self, text: str) -> str:
        return text.lower().strip()

    def contains_command(self, text: str) -> bool:
        text = self.normalize(text)
        return any(cmd in text for cmd in self.command_list)

    def is_soft_ack(self, text: str) -> bool:
        text = self.normalize(text)
        return any(re.fullmatch(rf"{w}[\.\!\?]?", text) for w in self.ignore_list)

    def evaluate(self, text: str, agent_is_speaking: bool):
        text = self.normalize(text)

        if self.contains_command(text):
            return "interrupt"

        if agent_is_speaking and self.is_soft_ack(text):
            return "ignore"

        if not agent_is_speaking and self.is_soft_ack(text):
            return "respond"

        return "respond"
