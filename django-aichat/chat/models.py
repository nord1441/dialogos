from django.db import models
from django.core.exceptions import ValidationError

# 画像・動画の拡張子チェック
def validate_image_or_video(file):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.mp4', '.webm', '.mov']
    import os
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError('画像または動画ファイル（jpg, png, mp4等）のみアップロードできます。')

class ChatModel(models.Model):
    system_dialogue = models.CharField(max_length=255)
    name = models.CharField(max_length=50)

class CharaimageModel(models.Model):
    charaimage = models.FileField(upload_to='images/', validators=[validate_image_or_video])

class ChatHistory(models.Model):
    session_id = models.CharField(max_length=128)
    role = models.CharField(max_length=16)  # 'user', 'assistant', 'system'
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.session_id} [{self.role}] {self.created_at}"