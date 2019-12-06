from django.shortcuts import redirect,render

#验证用户是否登录
def auto_session(func):
    def check_session(request,*args,**kwargs):
        flag = request.session.get("loginflag")
        if not flag:
            return render(request, "home_application/index.html")
        request.session.set_expiry(60)
        request.session.clear_expired()
        return func(request, *args, **kwargs)
    return check_session

