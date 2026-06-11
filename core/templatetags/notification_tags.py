import re
from django import template
from django.utils.translation import gettext as _

register = template.Library()

@register.filter
def translate_notification(message):
    # 1. Task assigned
    match = re.match(r"You have been assigned to a new task: '(.+)' by (.+)\.", message)
    if match:
        title, creator = match.groups()
        return _("Sizga yangi vazifa biriktirildi: '%(title)s' (belgiladi: %(creator)s)") % {'title': title, 'creator': creator}
        
    # 2. Task completed
    match = re.match(r"Task '(.+)' has been marked as COMPLETED\.", message)
    if match:
        title = match.group(1)
        return _("Vazifa '%(title)s' TUGALLANGAN holatiga o'tkazildi") % {'title': title}
        
    # 3. Task due 24h
    match = re.match(r"NOTIFICATION: Task '(.+)' is due in 24 hours!", message)
    if match:
        title = match.group(1)
        return _("Ogohlantirish: '%(title)s' vazifasi muddati tugashiga 24 soat qoldi!") % {'title': title}
        
    # 4. Task due 1h
    match = re.match(r"NOTIFICATION: Task '(.+)' is due in 1 hour!", message)
    if match:
        title = match.group(1)
        return _("Ogohlantirish: '%(title)s' vazifasi muddati tugashiga 1 soat qoldi!") % {'title': title}
        
    return _(message)
