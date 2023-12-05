from  django.contrib.auth.models import User
from django.db.models.signals import post_save 
from django.dispatch import receiver
from .models import Profile
import random

def create_phone():
    all_phones = []
    users =Profile.objects.all()
    
    for user in users:
        all_phones.append(user.phone)
        
    new_phone  = "+7" + str(random.randint(7000000000, 9999999999))
    if new_phone in all_phones:
        return new_phone
    else:
        return create_phone()
 
    
# post_save, который срабатывает после того, как объект User был сохранен. 
# sender: Класс модели, который отправил сигнал (в данном случае, User).
# instance: Сам объект User, который был сохранен.
# created: Флаг, который указывает, 
# был ли объект создан (иначе, это обновление).

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created: 
        Profile.objects.create(user=instance, phone=create_phone(), balance=0)
        
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()