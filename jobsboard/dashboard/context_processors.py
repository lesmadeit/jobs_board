from jobs.models import Message



def messages_context(request):
    if request.user.is_authenticated and hasattr(request.user, 'company_profile'):
        company = request.user.company_profile
        unread_count = Message.objects.filter(recipient_company=company, is_read=False).count()
        recent_messages = Message.objects.filter(recipient_company=company, parent_message__isnull=True).order_by('-created_at')[:3]
        return {
            'unread_count': unread_count,
            'recent_messages': recent_messages,
        }
    return {}