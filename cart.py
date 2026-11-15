class Cart:
    """Keeps the food lines currently selected by the customer."""

    def __init__(self, items=None):
        self.items = [dict(item) for item in (items or [])]

    @classmethod
    def from_dict(cls, data):
        return cls(data)

    def to_dict(self):
        return [dict(item) for item in self.items]

    def add(self, food):
        self.items.append(dict(food))

    def remove(self, line_id):
        self.items = [item for item in self.items if item["id"] != line_id]

    def change_quantity(self, line_id, delta):
        for item in self.items:
            if item["id"] == line_id:
                item["quantity"] += delta
                if item["quantity"] <= 0:
                    self.remove(line_id)
                return

    @property
    def total(self):
        return sum(item["price"] * item["quantity"] for item in self.items)

    @property
    def count(self):
        return sum(item["quantity"] for item in self.items)
