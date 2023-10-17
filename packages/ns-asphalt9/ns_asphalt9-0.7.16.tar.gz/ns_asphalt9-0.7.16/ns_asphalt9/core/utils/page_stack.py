class PageStack:
    def __init__(self, max_length: int = 10):
        self.max_length = max_length
        self.items = []

    def add_item(self, item):
        if len(self.items) < self.max_length:
            self.items.append(item)
        else:
            self.items.pop(0)
            self.items.append(item)

    def check_uniform(self) -> bool:
        if len(self.items) <= 9:
            return False

        first_item = self.items[0]
        return all(item == first_item for item in self.items)


page_stack = PageStack()
