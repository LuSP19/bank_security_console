from django.shortcuts import render
from django.utils.timezone import localtime

from datacenter.models import format_duration, get_duration
from datacenter.models import Passcard, Visit


def storage_information_view(request):
    non_closed_visits = []
    non_closed_visits_query = Visit.objects.filter(leaved_at=None)

    for visit in non_closed_visits_query:
        non_closed_visit = {
            'who_entered': visit.passcard.owner_name,
            'entered_at': localtime(visit.entered_at).strftime('%d-%m-%Y %H:%M'),
            'duration': format_duration(get_duration(visit)),    
        }
        non_closed_visits.append(non_closed_visit)

    context = {
        'non_closed_visits': non_closed_visits,
    }

    return render(request, 'storage_information.html', context)
