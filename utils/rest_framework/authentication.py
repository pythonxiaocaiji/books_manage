from django.conf import settings
from django.middleware.csrf import CsrfViewMiddleware
from django.contrib.auth.models import AnonymousUser
from django.utils.timezone import now
from rest_framework import authentication


from Apps.books.models import User, UserSession


class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        return reason


class UserAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        user_id = request.session.get('id')
        if user_id:
            if settings.DEBUG:
                try:
                    user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    request.session.flush()
                    user = AnonymousUser()
            else:
                session_key = request.session.session_key
                user_session = UserSession.objects.select_related('user').filter(
                    user_id=user_id,
                    session__session_key=session_key,
                    session__expire_date__gt=now()
                ).first()
                if user_session:
                    user = user_session.user
                else:
                    request.session.flush()
                    user = AnonymousUser()
            self.enforce_csrf(request)
            if not user:
                request.session.flush()
                user = AnonymousUser()
        else:
            user = AnonymousUser()
        return (user, None)

    def enforce_csrf(self, request):
        pass
        # reason = CSRFCheck().process_view(request, None, (), {})
        # if reason:
        #     raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)

def _get_user_session_key(session):
    user_id = session.get('id')
    if user_id:
        if settings.DEBUG:
            try:
                user = User.objects.get(id=user_id, is_active=True)
            except User.DoesNotExist:
                session.flush()
                user = AnonymousUser()
        else:
            session_key = session.session_key
            user_session = UserSession.objects.select_related('user').filter(
                user_id=user_id, user__is_active=True,
                session__session_key=session_key,
                session__expire_date__gt=now()
            ).first()
            if user_session:
                user = user_session.user
            else:
                session.flush()
                user = AnonymousUser()
        if not user or not user.is_active:
            session.flush()
            user = AnonymousUser()
    else:
        user = AnonymousUser()
    return user