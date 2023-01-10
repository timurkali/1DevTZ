from django.db.models import signals
from django.dispatch import receiver

from . import models, tasks


@receiver(signals.post_delete, sender=models.OrderLine, dispatch_uid='post_delete_order_line')
def post_delete_order_line(sender, instance, using, **kwargs):
    tasks.update_order_lines_total.delay(instance.order.pk)
