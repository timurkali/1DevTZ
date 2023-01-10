from django.contrib.auth import get_user_model

User = get_user_model()


def get_wallet(user: User, currency: str):
    return user.wallets.filter(currency=currency).first()
