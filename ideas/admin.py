from django.contrib import admin

# Register your models here.
from .models import Idea # Ideaモデルをインポート

admin.site.register(Idea) # Ideaモデルを管理サイトに登録