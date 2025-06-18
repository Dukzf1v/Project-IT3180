from django import template

register = template.Library()

# Custom filter to get an item from a list or dictionary
@register.filter(name='get_item')
def get_item(value, key):
    """Returns the item at `key` index or dictionary key."""
    try:
        return value[key]
    except (KeyError, IndexError):
        return None  # Return None or a default value if the key/index doesn't exist

@register.filter(name='get_payment_status')
def get_payment_status(value, key):
    """Lấy phần tử từ dictionary hoặc list theo key/index"""
    try:
        return value[key]
    except (KeyError, IndexError):
        return None  # Nếu không tìm thấy, trả về None