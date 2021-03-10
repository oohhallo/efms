from complaint.models import Vote

from django import template

register = template.Library()

@register.filter(name="vote_count")
def vote_count(complaint, vote_type):
    return len(Vote.objects.filter(complaint=complaint, vote=int(vote_type)))
