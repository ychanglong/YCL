# -*- coding: utf-8 -*-
# @Time        : 2023/03/01
# @Author      : MA Jared (BD/PIO3)
# @Bitbucket   : https://sourcecode.socialcoding.bosch.com/users/maa9szh/repos/goc_automation/browse
# @Application : User
# @Project     : GOC Automation Platform

from resource_base.modules.importModules import *
from resource_base.modules.basetools import md5
from userweb.models import Account
import logging
import jwt

# Get the django logger
logger = logging.getLogger('django')


def index(request):
    """Return login page
    Args:
        request
    Returns:
        Render to login.html
    """
    return render(request, 'user/login.html')


def login_handle(request):
    """Handle user login request
    Args:
        request
    Returns:
        Login failed code and reason:
        'code': 1, 'error': 'User ID or Password could not be empty'
        'code': 2, 'error': 'Wrong User ID or Password'
        'code': 3, 'error': 'This user has been disabled'
        'code': 4, 'error': 'Unknown Exception:' + str(e)
        'code': 5, 'error': 'User has no permission to login'
        Login successfully:
        'code': 0
    """



    # Get POST data
    loginid = request.POST.get('loginid')
    loginpwd = request.POST.get('loginpwd')
    id_token = request.POST.get('SSOIdToken')
    remember_flag = request.POST.get('rememberme')
    logger.info('ID_TOKEN DEBUG: ' + id_token)

    try:
        # Check if login input is empty
        if not loginid and not loginpwd and not id_token:
            logger.info('%s login failed, User ID or Password could not be empty.' % (loginid,))
            return JsonResponse({'code': 1, 'error': 'User ID or Password could not be empty'})
        
        # Get the user profile from AD when using SSO
        if id_token:
            sso_user_profile = jwt.decode(id_token, options={"verify_signature": False})
            loginid = sso_user_profile['user_profile_ntid']

        # Query user according loginid from DB
        obj_user = Account.objects.filter(Q(loginid=loginid) | Q(email=loginid))[0]

        # Check if user exist
        if not obj_user:
            logger.info('%s login failed, access denied.' % (loginid,))
            return JsonResponse({'code': 2, 'error': 'Access denied'})
        
        # Check the user's status
        if not obj_user.status:
            logger.info('%s login failed, user has been disabled.' % (loginid,))
            return JsonResponse({'code': 3, 'error': 'This user has been disabled'})

        # If not SSO login, then validate the password
        if not id_token and not obj_user.loginpwd == md5(loginpwd):
            logger.info('%s login failed, wrong User ID or Password.' % (loginid,))
            return JsonResponse({'code': 2, 'error': 'Wrong User ID or Password'})

        # Save the login time
        obj_user.last_login = time.time()
        obj_user.save()

        name_abb = ''
        for item in obj_user.name.split(' '):
            name_abb += item[0].upper()

        # Save session data
        res_data = {
            'loginid': obj_user.loginid, 'name': obj_user.name,
            'department': obj_user.department, 'email': obj_user.email, 'pmc_coordinator': 1 if obj_user.pmc_coordinator else 0, 'pmc_operator': 1 if obj_user.pmc_operator else 0,
            'guest_account': 1 if obj_user.guest_account else 0, 'avatar': 'empty.empty' if obj_user.avatar == 'empty.empty' else obj_user.avatar.url, 'admin': 1 if obj_user.admin else 0,
            'create_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(obj_user.create_time)), 'location': obj_user.location,
            'last_login': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(obj_user.last_login)),
            'last_loginid': loginid,
            'name_abb': name_abb
        }
        # Add edit time
        if obj_user.edit_time:
            res_data['edit_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(obj_user.edit_time))
        else:
            res_data['edit_time'] = "No History"

        # Check if select remember me option
        if remember_flag:
            # Keep the session for 14 days
            request.session.set_expiry(14 * 24 * 3600)
        else:
            # Not keep the session
            request.session.set_expiry(0)
        # Save user data to session
        request.session['user_account'] = res_data

        # Login successfully
        logger.info('%s successfully login.' % (loginid,))
        return JsonResponse({'code': 0})
    except Exception as e:
        logger.info('%s login failed, got an Exception: %s.' % (loginid, str(e)))
        return JsonResponse({'code': 4, 'error': 'Unknown Exception:' + str(e)})
