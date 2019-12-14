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


    @staticmethod
    def save_distributor(request):
        distributor = Distributor(
            name=request.POST.get('name'),
            recipient_first_name=request.POST.get('first_name'),
            recipient_last_name=request.POST.get('last_name'),
            recipient_patronymic=request.POST.get('patronymic'),
            shipping_address=request.POST.get('address'),
            telephone_number=request.POST.get('telephone_number'),
        )
        distributor.save()
        return distributor
