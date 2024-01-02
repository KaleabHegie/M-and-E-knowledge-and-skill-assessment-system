from survey_managment.models import ContactUs , UserResponse , Survey , CustomUser

def unread_messages(request):
    unread_count = ContactUs.objects.filter(status='inbox', read=False).count()
    pending_responses = UserResponse.objects.filter(status='pending').count()
    unread = ContactUs.objects.filter(status='inbox', read=False)
    line_ministry = request.user.Line_ministry
    user = request.user 
    user = CustomUser.objects.get(username = user)
    surveys_count = Survey.objects.filter(userresponse__status='recomended', for_line_ministry = line_ministry , userresponse__submitted_by = user).count()


    return {'unread_count': unread_count , "unread" : unread  ,"pending_responses" : pending_responses , "surveys_count" : surveys_count}