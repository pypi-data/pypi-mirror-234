from django.conf import settings

ALUMNI_STATE_NAME = getattr(settings, 'ALUMNI_STATE_NAME', "Alumni")

ALUMNI_TASK_PRIORITY = getattr(settings, 'ALUMNI_TASK_PRIORITY', "7")
