import random
import string
from flask_mail import Message
from . import mail


def generate_two_factor_code():
    return ''.join(random.choices(string.digits, k=6))

def send_two_factor_code(email, code, mail):
    msg = Message('Your 2FA Verification Code', recipients=[email])
    msg.body = f'Your two‑factor authentication code is: {code}'
    mail.send(msg)


def send_order_confirmation(email, order, details):
    """
    Send an order confirmation email.
    
    :param email: The recipient's email address (provided by the user).
    :param order: The Order object.
    :param details: A dictionary containing shipping and payment details.
    """
    msg = Message("Order Confirmation - EOW Ltd.",
                  recipients=[email])
    msg.body = f"""
Dear {details.get('full_name')},

Thank you for your order from EOW Ltd.

Order Details:
---------------
Order ID: {order.id}
Total Amount: ${order.total}

Shipping Address:
{details.get('shipping_address')}
{details.get('city')}, {details.get('state')} {details.get('zip_code')}
{details.get('country')}

Payment Information:
PayPal Email: {details.get('paypal_email')}

We will process your order soon. If you have any questions, feel free to contact us.

Thank you for shopping with us!

Best regards,
EOW Ltd.
"""
    mail.send(msg)