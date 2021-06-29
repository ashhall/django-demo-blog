from datetime import datetime, timedelta
from django import template
from django.utils.timesince import timesince
from django.utils.timezone import utc

register = template.Library()


@register.filter(name='trunc_naturaltime')
def truncate_naturaltime(value):
    now = datetime.now().utcnow().replace(tzinfo=utc)
    try:
        difference = now - value
    except TypeError as e:
        print(e)
        return value

    if difference <= timedelta(minutes=1):
        return 'just now'
    else:
        time = timesince(value).split(',')[0]
        return f'{time} ago'
