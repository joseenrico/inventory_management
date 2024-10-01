# Models for Categories and Items
class Category:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Item:
    def __init__(self, id, category_id, name, description, price):
        self.id = id
        self.category_id = category_id
        self.name = name
        self.description = description
        self.price = price
