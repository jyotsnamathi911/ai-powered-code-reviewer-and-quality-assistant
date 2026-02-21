def process_order(price, tax, discount):
    '''"""Summary of the function.

Args:
    price: Description of price.
    tax: Description of tax.
    discount: Description of discount.

"""'''
    total = price + tax
    if discount > 0:
        total = total - discount
    if total > 1000:
        print('High value order')
    return total

class Invoice:

    def generate(self, amount):
        '''"""Summary of the function.

Args:
    self: Description of self.
    amount: Description of amount.

"""'''
        final = amount * 1.18
        return final