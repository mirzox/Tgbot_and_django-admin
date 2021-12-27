from django.db import models

# Create your models here.


class TgUser(models.Model):
    chat_id = models.PositiveBigIntegerField(
        verbose_name='ID пользователя',
        primary_key=True,
        unique=True
    )
    firstname = models.CharField(max_length=64, null=True, blank=True)
    username = models.CharField(max_length=32, null=True, blank=True)
    language = models.CharField(max_length=3, default='ru')
    phone = models.CharField(max_length=12, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    stage = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.chat_id} - {self.firstname} - {self.username}"


class FoodType(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True, auto_created=True)
    text = models.CharField(max_length=50)
    calldata = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'FoodType'
        verbose_name_plural = 'FoodTypes'

    def __str__(self):
        return f"{self.text} - {self.calldata}"


class Food(models.Model):
    type = models.ForeignKey(FoodType, on_delete=models.CASCADE)
    text = models.CharField(max_length=50)
    calldata = models.CharField(max_length=50)
    price = models.FloatField()

    class Meta:
        verbose_name = 'Food'
        verbose_name_plural = 'Foods'

    def __str__(self):
        return f"{self.type} - {self.text} - {self.price}"


class Order(models.Model):
    chat_id = models.ForeignKey(TgUser, on_delete=models.CASCADE)
    type = models.ForeignKey(FoodType, on_delete=models.CASCADE, null=True, blank=True)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=50, default='in progress')

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"{self.chat_id} - {self.type} - {self.status}"
