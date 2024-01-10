from survey_managment.models import ContactUs , UserResponse , Survey , CustomUser

def unread_messages(request):
    unread_count = ContactUs.objects.filter(status='inbox', read=False).count()
    pending_responses = UserResponse.objects.filter(status='pending').count()
    unread = ContactUs.objects.filter(status='inbox', read=False)
    user = request.user 
   
   
    

    return {'unread_count': unread_count , "unread" : unread  ,"pending_responses" : pending_responses }