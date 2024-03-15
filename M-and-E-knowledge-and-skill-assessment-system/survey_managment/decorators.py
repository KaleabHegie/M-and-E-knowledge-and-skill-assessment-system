from django.http import HttpResponse
from django.shortcuts import redirect



# def mopd_user_requierd():
    
def admin_user_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_mopd_head:            
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('You are not authorized to access this content.')
    return wrapper_func  


def ministry_user_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_line_minister_head:            
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('You are not authorized to access this content.')
    return wrapper_func    