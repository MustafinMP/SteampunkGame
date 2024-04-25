class Inventory:
    def __init__(self):
        self.inventory = dict()

    def __getitem__(self, item):
        return self.inventory[item]

    def add(self, item, count=1) -> None:
        if item in self.inventory.keys():
            self.inventory[item] += count
        else:
            self.inventory[item] = count

    def count(self, item) -> int:
        if item in self.inventory.keys():
            return self.inventory[item]

    def get(self, item, count) -> int:
        if item in self.inventory.keys():
            real_count = self.inventory[item]
            if real_count < count:
                self.inventory[item] = 0
                return real_count
            self.inventory[item] -= count
            return count
        raise KeyError
