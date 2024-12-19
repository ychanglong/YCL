from resource_base.modules.importModules import *
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from userweb.models import Account

class Auth_Md(MiddlewareMixin):

    def process_request(self, request):

        # Get the request URL
        current_url = request.path_info

        for item in settings.WHITE_URL_LIST:
            if item == current_url:
                # Skip this middleware validation
                return None

        # Get user's session
        obj_user = request.session.get('user_account')

        if obj_user:
            login_user = Account.objects.get(loginid=obj_user['loginid'])
            login_user.last_login = time.time()
            login_user.save()
            request.user_account = obj_user
        else:
            return redirect(reverse('login'))
        
        # Get the user's permission list and check if the request url in the list
        
