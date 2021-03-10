from complaint.models import Vote, Complaint

from django import template

register = template.Library()

@register.filter(name="vote_count")
def vote_count(complaint, vote_type):
    return len(Vote.objects.filter(complaint=complaint, vote=int(vote_type)))

@register.filter(name="voted")
def voted(voter, complaint_id):
    complaint = Complaint.objects.filter(id=int(complaint_id)).first()
    return len(Vote.objects.filter(complaint=complaint, voter=voter))

@register.filter(name="user_complaint")
def user_complaint(user, complaint_id):
    return len(Complaint.objects.filter(id=int(complaint_id), author=user))
