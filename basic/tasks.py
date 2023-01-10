import logging

from celery import shared_task

from . import models


@shared_task()
def update_order_lines_total(order_id: int):
    order = models.Order.objects.get(pk=order_id)
    total = 0
    for order_line in order.order_lines.all():
        total += order_line.product.price * order_line.count

    order.total = total * 100  # converts to tiyn. 1 KZT = 100 TIYN
    order.save(update_fields=('total',))


@shared_task()
def my_periodic_task():
    logging.info('=========== PERIODIC TASK ==============')


@shared_task()
def my_scheduled_task():
    logging.info('=========== SCHEDULED TASK ==============')
