from django import template

register = template.Library()

@register.filter
def is_admin(gym, user):
	if gym.members.filter(id=user.id).count():
		return True
	else:
		return False
