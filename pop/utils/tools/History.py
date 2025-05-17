class History:
    def __init__(self):
        self.entries = []

    def add(self, action, total_prize):
        self.entries.append((action, total_prize))

    def get(self):
        return self.entries

    def __repr__(self):
        return f"History({self.entries})"
