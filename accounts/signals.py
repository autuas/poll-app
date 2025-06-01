
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_login_failed, user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver

# ###
# FLAW 4: OWASP A09:2021-Security Logging and Monitoring Failures
# See poll_project/settings.py line 138 for logging definitions
# #
# Vulnerable version (of no logging):
class DummyLogger:
    def info(self, *args, **kwargs): pass
    def warning(self, *args, **kwargs): pass
logger = DummyLogger()

# Safe version (with proper logging):
# import logging
# logger = logging.getLogger("security")
# ###

@receiver(user_logged_in)
def log_logged_in(sender, request, user, **kwargs):
    logger.info(f"Login for username '{user.username}' from IP address {get_client_ip_address(request)}.")

@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    logger.warning(f"Failed login attempt for username '{credentials.get('username')}' from IP address {get_client_ip_address(request)}.")

@receiver(user_logged_out)
def log_logged_out(sender, request, user, **kwargs):
    logger.info(f"Logout for username '{user.username}' from IP address {get_client_ip_address(request)}.")

@receiver(post_save, sender=User)
def log_user_registered(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New username '{instance.username}' registered.")

def get_client_ip_address(request):
    return request.META.get('REMOTE_ADDR', '')