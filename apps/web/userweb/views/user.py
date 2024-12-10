# -*- coding: utf-8 -*-
# @Time        : 2023/03/01
# @Author      : MA Jared (BD/PIO3)
# @Bitbucket   : https://sourcecode.socialcoding.bosch.com/users/maa9szh/repos/goc_automation/browse
# @Application : User
# @Project     : GOC Automation Platform

from resource_base.modules.importModules import *
from resource_base.modules import basetools
from userweb.models import Account
from django.views.decorators.csrf import csrf_exempt
import logging

# Get the django logger
logger = logging.getLogger('django')

@csrf_exempt
def profile_index(request):
    return render(request, 'user/profile.html')


def change_profile(request):
    """Change personal information
            Args:
                request
            Returns:
                JsonResponse:
                    status: Saving personal info result, successful or failed
    """
    # Get the request data
    rec = request.POST
    files = request.FILES
    upload_avatar = files.get('uploadAvatar', None)

    try:
        # Get current user
        obj_user = Account.objects.filter(loginid=rec.get('loginid')).first()
        # Change user information
        obj_user.name = rec.get('name')
        obj_user.department = rec.get('department')
        obj_user.email = rec.get('email')
        obj_user.location = rec.get('location')
        old_avatar_url = obj_user.avatar.url
        if upload_avatar:
            obj_user.avatar = upload_avatar
            obj_user.avatar.name = basetools.custom_file_name(obj_user.avatar)

        if rec.get('newpwd'):
            obj_user.loginpwd = basetools.md5(rec.get('newpwd'))

        # Change the update time
        obj_user.edit_time = time.time()

        # Save to database
        obj_user.save()

        # Delete old avatar
        if old_avatar_url and files.get('uploadAvatar'):
            avatar_url_list = old_avatar_url.split('/')
            old_avatar_url = settings.MEDIA_ROOT
            for item in avatar_url_list:
                old_avatar_url = os.path.join(old_avatar_url, item)
            if os.path.exists(old_avatar_url):
                os.remove(old_avatar_url)

        name_abb = ''
        for item in obj_user.name.split(' '):
            name_abb += item[0].upper()

        # Save user data to session
        request.session['user_account']['name'] = obj_user.name
        request.session['user_account']['department'] = obj_user.department
        request.session['user_account']['email'] = obj_user.email
        request.session['user_account']['location'] = obj_user.location
        request.session['user_account']['avatar'] = obj_user.avatar.url if obj_user.avatar else ''
        request.session['user_account']['name_abb'] = name_abb

        # Ask for session update
        request.session.modified = True

        logger.info('%s changed profile successfully.' % (obj_user.loginid,))
        return JsonResponse({'status': True})
    except Exception as e:
        logger.error('%s Error changed profile: %s' % (obj_user.loginid, str(e)))
        return JsonResponse({'status': False, 'error': 'Error saving the profile:' + str(e)})


def user_logout(request):
    """User logout"""
    # Clear Session
    request.session.flush()
    # Jump to login page
    return redirect(reverse('login'))


def teammates_index(request):
    return render(request, 'user/teammates.html')


@csrf_exempt
def teammates_list(request):
    """Query all users"""

    # Get all users
    obj_users = list(Account.objects.filter(status__icontains='1').values())

    for user in obj_users:
        name_abb = ''
        for item in user['name'].split(' '):
            name_abb += item[0].upper()
        user['name_abb'] = name_abb

    return JsonResponse({'status': True, 'data': obj_users})


def teammates_add(request):
    """ Add new user"""
    rec = request.POST

    # logging the action
    logger.info(request.session.get('user_account')['loginid'] + ' is adding new user: ' + rec.get('newLoginid'))

    try:

        Account.objects.create(
            loginid=rec.get('newLoginid'),
            loginpwd=basetools.md5(rec.get('newLoginpwd')),
            status=1,
            admin=1 if rec.get('newUserType') == 'admin' else 0,
            guest_account=1 if rec.get('newUserType') == 'guest' else 0,
            name=rec.get('newUserName'),
            department=rec.get('newUserDepartment'),
            email=rec.get('newUserEmail'),
            location=rec.get('newUserLocation')
        )

    except Exception as e:
        logger.error('Error creating new user account: ' + str(e))
        return JsonResponse({'status': False, 'error': str(e)})

    return JsonResponse({'status': True})
