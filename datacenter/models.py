from datetime import datetime
from time import gmtime, strftime

from django.db import models


def get_duration(visit):
    if visit.leaved_at:
        duration = visit.leaved_at.replace(tzinfo=None) - visit.entered_at.replace(tzinfo=None)
        return duration.total_seconds()
    else:
        return (datetime.now() - visit.entered_at.replace(tzinfo=None)).total_seconds()


def format_duration(duration):
    return strftime("%H:%M", gmtime(duration))


def is_visit_long(visit, minutes=60):
    return True if get_duration(visit) // 60 > minutes else False


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved= 'leaved at ' + str(self.leaved_at) if self.leaved_at else 'not leaved'
        )
