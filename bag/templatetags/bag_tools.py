from django import template

register = template.Library()


@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    """
    Calculate the subtotal of items
    ref Boutique Ado lesson: https://tinyurl.com/2ktsebwu
    """
    return price * quantity
