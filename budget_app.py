#we could use round(variable, -n) in order to do the same thing approximating all numbers by 10 before the comma, this way is much easier
def drop(n):
  return int(n * 10) / 10

def get_total(categories):
  total = 0
  breakdown = []
  for category in categories:
    total += category.get_withdrawls()
    breakdown.append(category.get_withdrawls())
  res = list(map(lambda x: drop(x / total), breakdown))
  return res


def create_spend_chart(categories):
  """bar chart"""
  final = 'Percentage spent by category\n'
  i = 100
  total = get_total(categories)
  while i >= 0:
    space = ' '
    for t in total:
      if t * 100 >= i:
        space += 'o  '
      else:
        space += '   '
    final += str(i).rjust(3) + '|' + space + ('\n')
    i -= 10

  dashes = '-' + '---' * len(categories)
  names = []
  x_axis = ''
  for category in categories:
    names.append(category.name)

  maxi = max(names, key=len)

  for x in range(len(maxi)):
    nameStr = '     '
    for name in names:
      if x >= len(name):
        nameStr += '   '
      else:
        nameStr += name[x] + '  '
    if(x != len(maxi) - 1):
      nameStr += '\n'

    x_axis += nameStr

  final += dashes.rjust((len(dashes) + 4)) + '\n' + x_axis
  return final


class Category:

  def __init__(self, name):
    self.name = name
    self.ledger = []

  def __str__(self):
    total = 0
    title = f"{self.name:*^30}\n"
    items = ''
    for item in self.ledger:
      items += f"{item['description'][0:23]:23}" + \
          f"{item['amount']:>7.2f}" + '\n'
      total += item['amount']
    res = title + items + 'Total: ' + str(total)
    return res

  def deposit(self, amount, description=''):
    """ A deposit method that accepts an amount and description. If no description is given, it should default to an empty string. The method should append an object to the ledger list in the form of {"amount": amount, "description": description}."""
    self.ledger.append({"amount": amount, "description": description})

  def withdraw(self, amount, description=''):
    """
    A withdraw method that is similar to the deposit method, but the amount passed in should be stored in the ledger as a negative number. If there are not enough funds, nothing should be added to the ledger. This method should return True if the withdrawal took place, and False otherwise.
    """
    if self.check_funds(amount):
      self.ledger.append({"amount": -amount, "description": description})
      return True
    return False

  def get_balance(self):
    """A get_balance method that returns the current balance of the budget category based on the deposits and withdrawals that have occurred."""
    tot = 0
    for item in self.ledger:
      tot += item['amount']
    return tot

  def transfer(self, amount, category):
    """A transfer method that accepts an amount and another budget category as arguments. The method should add a withdrawal with the amount and the description "Transfer to [Destination Budget Category]". The method should then add a deposit to the other budget category with the amount and the description "Transfer from [Source Budget Category]". If there are not enough funds, nothing should be added to either ledgers. This method should return True if the transfer took place, and False otherwise."""
    if self.check_funds(amount):
      self.withdraw(amount, 'Transfer to ' + category.name)
      category.deposit(amount, 'Transfer from ' + self.name)
      return True
    return False

  def check_funds(self, amount):
    """A check_funds method that accepts an amount as an argument. It returns False if the amount is greater than the balance of the budget category and returns True otherwise. This method should be used by both the withdraw method and transfer method."""
    if self.get_balance() >= amount:
      return True
    return False

  # how much money are spent in each category
  def get_withdrawls(self):
    total = 0
    for item in self.ledger:
      if item['amount'] < 0:
        total += item['amount']
    return total
