from django.shortcuts import render
from django.utils.timezone import localtime

from datacenter.models import format_duration, get_duration, is_visit_long
from datacenter.models import Passcard, Visit


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.get(passcode=passcode)
    passcard_visits_query = Visit.objects.filter(passcard=passcard)

    this_passcard_visits = []
    for visit in passcard_visits_query:
        visit_record = {
            'entered_at': localtime(visit.entered_at).strftime('%d-%m-%Y'),
            'duration': format_duration(get_duration(visit)),
            'is_strange': is_visit_long(visit, minutes=60)
        }
        this_passcard_visits.append(visit_record)

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }

    return render(request, 'passcard_info.html', context)
