from django.db import models


class UserSession(models.Model):
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        verbose_name='User',
    )
    session_key = models.CharField(
        'Session Key',
        max_length=40,
        unique=True,
    )
    created_at = models.DateTimeField('Created At', auto_now_add=True)
    expires_at = models.DateTimeField('Expires At')

    class Meta:
        verbose_name = 'User Session'
        verbose_name_plural = 'User Sessions'

    def __str__(self):
        return f"Session for {self.user.username}"


class PasswordResetToken(models.Model):
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        verbose_name='User',
    )
    token = models.CharField('Token', max_length=64, unique=True)
    created_at = models.DateTimeField('Created At', auto_now_add=True)
    used = models.BooleanField('Used', default=False)

    class Meta:
        verbose_name = 'Password Reset Token'
        verbose_name_plural = 'Password Reset Tokens'

    def __str__(self):
        return f"Reset token for {self.user.username}"