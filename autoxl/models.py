from django.db import models, IntegrityError
from django.shortcuts import get_object_or_404
from typing import Union


class Distributor(models.Model):
    name = models.CharField("Название дистрибьютора", max_length=100)
    recipient_first_name = models.CharField("Имя получателя", max_length=30)
    recipient_last_name = models.CharField("Фамилия получателя", max_length=30)
    recipient_patronymic = models.CharField("Отчество получателя", max_length=30, blank=True)
    shipping_address = models.CharField("Адрес отправки карты", max_length=150)
    telephone_number = models.CharField("Телефонный номер", max_length=25)
    external_id = models.CharField("Внешний ID из 1С", max_length=25, unique=True)
    add_date = models.DateTimeField("Дата и время добавления", auto_now_add=True)
    active = models.BooleanField("Статус удален/активен", default=True)


    def __str__(self):
        return self.name


    def kill(self):
        self.active = False
        self.save(update_fields=['active'])


    @staticmethod
    def save_distributor(request):
        try:
            distributor = Distributor(
                name=request.POST['name'],
                recipient_first_name=request.POST['first_name'],
                recipient_last_name=request.POST['last_name'],
                recipient_patronymic=request.POST['patronymic'],
                shipping_address=request.POST['address'],
                telephone_number=request.POST['telephone_number'],
                external_id=request.POST['external_id']
            )
            distributor.save()
        except IntegrityError:
            distributor_from_db = get_object_or_404(Distributor, external_id=request.POST['external_id'])
            return distributor_from_db.name
        except Exception:
            return False
        return distributor
