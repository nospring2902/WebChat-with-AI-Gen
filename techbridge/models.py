from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    main_language = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class Group(models.Model):
    group_name = models.CharField(max_length=255)
    latest_message_id = models.ForeignKey('GroupMessage', on_delete=models.SET_NULL, null=True, blank=True, related_name='latest_message_in_group')

    def __str__(self):
        return self.group_name

class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('group', 'user')

    def __str__(self):
        return f"{self.user.username} in {self.group.group_name}"

class GroupThread(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    first_message = models.ForeignKey('GroupMessage', on_delete=models.CASCADE, related_name='first_message_in_thread')

    def __str__(self):
        return f"Thread in {self.group.group_name}"

class GroupMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(GroupThread, on_delete=models.CASCADE)
    message_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    japanese = models.TextField(null=True, blank=True)
    vietnamese = models.TextField(null=True, blank=True)
    english = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Message by {self.sender.username} in thread {self.thread.id}"
