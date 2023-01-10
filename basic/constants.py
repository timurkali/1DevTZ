class CURRENCIES:
    TIYN = 'TIYN'

    choices = (
        (TIYN, 'Тиын'),
    )


class ORDER_STATUSES:
    NEW = 'NEW'
    PENDING = 'PENDING'
    PAID = 'PAID'

    choices = (
        (NEW, 'NEW'),
        (PENDING, 'PENDING'),
        (PAID, 'PAID'),
    )
