from .models import Mailing, Client
from celery import shared_task
from datetime import datetime
from django.db.models import Q


@shared_task
def mailing():
    mailing_selection = Mailing.objects.all()
    return mailing_selection


@shared_task
def mailing():
    first_mailing = Mailing.objects.get(pk=1)
    time_start = first_mailing.time_start.strftime('%H:%M:%S')
    time_stop = first_mailing.time_stop.strftime('%H:%M:%S')
    time_now = datetime.now().strftime('%H:%M:%S')

    if time_start <= time_now <= time_stop:
        selection = Client.objects.filter(Q(mobile_operator_code__exact=first_mailing.mobile_operator_code) &
                                          Q(tag__exact=first_mailing.tag)).values_list('phone_number')

        for client in selection:
            print(client_message(first_mailing.message_text, client))
        return 'ok'


@shared_task
def client_message(message_text, phone_number):
    return f'Сообщение: {message_text} для пользователя: {phone_number}'






