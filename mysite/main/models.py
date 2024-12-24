from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # связь с моделью User
    bio = models.TextField(blank=True, null=True)  # Пример дополнительного поля (биография)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Поле для фото профиля

    def __str__(self):
        return f'{self.user.username} Profile'

class Poll(models.Model):
    question = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def has_voted(self, user):
        return Vote.objects.filter(user=user, poll=self).exists()

    def __str__(self):
        return self.question


class PollOption(models.Model):
    poll = models.ForeignKey(Poll, related_name="options", on_delete=models.CASCADE)  # Варианты для голосования
    option_text = models.CharField(max_length=255)  # Текст варианта
    votes = models.IntegerField(default=0)  # Количество голосов

    def __str__(self):
        return self.option_text

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'poll')  # Ограничение, чтобы каждый пользователь мог голосовать только один раз за опрос

    def __str__(self):
        return f"{self.user.username} voted on poll {self.poll.id} with option {self.option.option_text}"

