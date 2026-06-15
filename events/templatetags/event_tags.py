from django import template

register = template.Library()

@register.filter
def is_registered(event, user):
    """Check if a user is registered for an event."""
    return event.registrations.filter(user=user).exists()