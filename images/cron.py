from django_cron import CronJobBase, Schedule
from images.models import ExpiringLink
from django.utils import timezone


class DeleteExpiredImages(CronJobBase):
    RUN_EVERY_MINUTES = 720

    schedule = Schedule(run_every_mins=RUN_EVERY_MINUTES)
    code = 'images.delete_expired_images'

    def do(self):
        ExpiringLink.objects.filter(valid_until__lt=timezone.now()).delete()
