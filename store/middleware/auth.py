from django.shortcuts import redirect


def auth_middleware(get_response):
    def middleware(request):
        returnUrl = request.META['PATH_INFO']
        # print(request.META['PATH_INFO']) # it gave the path which your redirect to another page
        if not request.session.get('customer_id'):
            return redirect(f'Login?return_url={returnUrl}')
        response = get_response(request)
        return response

    return middleware
