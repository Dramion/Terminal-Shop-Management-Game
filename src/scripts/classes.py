class Store:
  inventory = {"Sponge": {"price": 2, "quantity": 1}}
  def __init__(self, store_name, store_funds):
    self.name = store_name
    self.balance = store_funds

  def __repr__(self):
    return "{} has an inventory of {}, and a total balance of ${}.".format(self.name, self.inventory, self.balance)

  def add_inv(self, item):
    if type(item) is Item and item.name in self.inventory:
      self.inventory[item.name]["quantity"] += 1
    elif type(item) is Item and item.name not in self.inventory:
      self.inventory.update(item.dict)
      self.inventory[item.name]["quantity"] = 1
    else:
      print("'{}' is not a valid item.".format(item))

class Item:
  def __init__(self, item_name, item_price):
    self.name = item_name
    self.price = item_price
    self.dict = {self.name: {"price": self.price}}

  def __repr__(self):
    return "{} costs ${} per item.".format(self.name, self.price)

class Customer:
  cart = {}

  def __init__(self, customer_name, customer_balance):
    self.name = customer_name
    self.balance = customer_balance

  def __repr__(self):
    return "{} has ${} in their wallet and {} in their cart.".format(self.name, self.balance, self.cart)