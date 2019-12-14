from django.db import models


class Distributor(models.Model):
    name = models.CharField("Название дистрибьютора", max_length=100)
    recipient_first_name = models.CharField("Имя получателя", max_length=30)
    recipient_last_name = models.CharField("Фамилия получателя", max_length=30)
    recipient_patronymic = models.CharField("Отчество получателя", max_length=30, blank=True)
    shipping_address = models.CharField("Адрес отправки карты", max_length=150)
    telephone_number = models.CharField("Телефонный номер", max_length=25)
    active = models.BooleanField("Статус удален/активен", default=True)


    def __str__(self):
        return self.name


    def kill(self):
        self.active = False


