# ideas/forms.py
from django import forms
from .models import Idea
from .models import Idea, Comment # ← Commentをインポート

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ('title', 'content', 'image', 'video') # ← imageとvideoを追加

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)