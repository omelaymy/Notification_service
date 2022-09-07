from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
from backports import zoneinfo


# Модель тэг создана для группировки клиентов в пуллы различных тэгов
class Tag(models.Model):
    tag = models.CharField(max_length=25)

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Mailing(models.Model):
    date_start = models.DateTimeField(verbose_name='Дата запуска рассылки')
    date_stop = models.DateTimeField(verbose_name='Дата окончания рассылки')
    time_start = models.TimeField(verbose_name='Время запуска рассылки')
    time_stop = models.TimeField(verbose_name='Время окончания рассылки')
    message_text = models.TextField(verbose_name='Текст сообщения для доставки клиенту')
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)
    mobile_operator_code = models.CharField(verbose_name='Код мобильного оператора', max_length=3, blank=True)

    def __str__(self):
        return f'Рассылка {self.pk} начиная с: {self.date_start}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


# Предусмотрен выбор временой зоны
class Client(models.Model):
    TIMEZONE_CHOICES = ((x, x) for x in sorted(zoneinfo.available_timezones(), key=str.lower))

    phone_number = PhoneNumberField()
    mobile_operator_code = models.CharField(verbose_name='Код мобильного оператора', max_length=3, editable=False)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)
    timezone = models.CharField(max_length=250, verbose_name='Часовой пояс', choices=TIMEZONE_CHOICES)

    def save(self, *args, **kwargs):
        self.mobile_operator_code = str(self.phone_number)[2:5]
        return super(Client, self).save(*args, **kwargs)

    def __str__(self):
        return f'ID клиента: {self.pk}, {self.phone_number}, Тэг: {self.tag}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    SENT = 'Отправлена'
    NO_SENT = 'Не отправлена'

    STATUS_CHOICES = [
        (SENT, 'Отправлена'),
        (NO_SENT, 'Не отправлена'),
    ]

    time_create = models.DateTimeField(verbose_name='Дата и время создания (отправки)', auto_now_add=True)
    sending_status = models.CharField(verbose_name='Статус отправки', max_length=15, choices=STATUS_CHOICES)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='messages')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return f'Сообщение {self.pk} с текстом {self.mailing} для {self.client}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
