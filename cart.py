class Cart:
    """Shopping cart model. Stores item snapshots and quantities."""
    def __init__(self, items=None):
        self.items = items or []

    @classmethod
    def from_dict(cls, data):
        return cls([dict(item) for item in data])

    def to_dict(self):
        return [dict(item) for item in self.items]

    def add(self, food):
        existing = next((item for item in self.items if item["id"] == food["id"]), None)
        if existing:
            existing["quantity"] += 1
        else:
            self.items.append({**food, "quantity": 1})

    def remove(self, item_id):
        self.items = [item for item in self.items if item["id"] != item_id]

    def change_quantity(self, item_id, delta):
        for item in self.items:
            if item["id"] == item_id:
                item["quantity"] += delta
                if item["quantity"] <= 0:
                    self.remove(item_id)
                return

    @property
    def total(self):
        return sum(item["price"] * item["quantity"] for item in self.items)

    @property
    def count(self):
        return sum(item["quantity"] for item in self.items)
