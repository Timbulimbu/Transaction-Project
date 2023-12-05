from django.db import models
from django.contrib.auth.models import User
from .utils import validate_phone_number
from django.forms import ValidationError


class Profile(models.Model):
    image = models.ImageField(upload_to='profile_image/', blank=True, null=True, verbose_name="Фотография", help_text="Вставьте фото")
    phone = models.CharField(max_length=20, verbose_name="Номер телефона", unique=True, validators=[validate_phone_number],)
    balance = models.PositiveIntegerField(default=100, verbose_name="Текущий баланс для этого профиля")
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text="Связанный пользователь для этого профиля")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания профиля")
    
    def __str__(self) -> str:
        return f"Профиль пользователя: {self.user.username}"
    
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
        ordering = ['-created_at']


class Transaction(models.Model):
    sender_phone = models.CharField(max_length=20, verbose_name="Номер отправителя", validators=[validate_phone_number])
    recipient_phone = models.CharField(max_length=20, verbose_name="Номер получателя", validators=[validate_phone_number])
    amount = models.PositiveBigIntegerField(verbose_name="Сумма перевода")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания транзакции")
    
    def save(self, *args, **kwargs):
        try:
            sender_profile = Profile.objects.get(phone=self.sender_phone)
        except Profile.DoesNotExist:
           return ValidationError("Профиль отправителя не найден")
       
        try:
            recipient_profile = Profile.objects.get(phone=self.recipient_phone)
        except Profile.DoesNotExist:
            return ValidationError("Профиль получателя не найден")
        
        if self.sender_phone == self.recipient_phone:
            return ValidationError("Нельзя перевести деньги самому себе")

        if sender_profile.balance < self.amount:
            return ValidationError("Недостаточно средств для перевода")
        
        if self.amount < 100:
            return ValidationError("Минимальная сумма перевода - 100 тенге")
        
        sender_profile.balance -= self.amount
        recipient_profile.balance += self.amount
        
        sender_profile.save()
        recipient_profile.save()
        
        
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f"Транзакция от {self.sender_phone} для {self.recipient_phone} - сумма {self.amount}"
    
    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"
        ordering = ['-created_at']
        
        

class AddBalance(models.Model):
    phone = models.CharField(max_length=20, verbose_name="Номер телефона", help_text="Укажите свой номер телефона для пополнения баланса", validators=[validate_phone_number])
    amount = models.PositiveBigIntegerField(verbose_name="Сумма добавления")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата пополнения")
    
    def save(self, *args, **kwargs):
        try:
            profile = Profile.objects.get(phone=self.phone)
        except Profile.DoesNotExist:
            return ValidationError("Абонент не найден")
        
        if self.amount < 100:
            return ValidationError("Минимальная сумма добавления - 100 тенге")
        
        profile.balance += self.amount
        profile.save()
        
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f"{self.phone} - сумма {self.amount}"
    
    class Meta:
        verbose_name = "Пополнение баланса"
        verbose_name_plural = "Пополнения баланса"
        ordering = ['-created_at']
        
    