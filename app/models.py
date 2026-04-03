class ItemStore:
    def __init__(self):
        self.items = []
        self.counter = 1

    def add_item(self, name):
        item = {"id": self.counter, "name": name}
        self.items.append(item)
        self.counter += 1
        return item

    def get_all(self):
        return self.items

    def delete(self, item_id):
        for item in self.items:
            if item["id"] == item_id:
                self.items.remove(item)
                return True
        return False
