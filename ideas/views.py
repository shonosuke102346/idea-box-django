from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from .models import Idea
from .forms import IdeaForm
from django.views.generic import DetailView # ← DetailViewをインポート
from django.views.generic import UpdateView # ← UpdateViewをインポート
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # ← アクセス制限用のMixinをインポート
from django.views.generic import DeleteView # ← DeleteViewをインポート
from .forms import CommentForm # ← CommentFormをインポート
from django.views.generic import DetailView, UpdateView, DeleteView # ← DeleteViewを追加
from django.db.models import Q # ← Qオブジェクトをインポート



def idea_list(request):
    query = request.GET.get('q')
    
    if query:
        # Qオブジェクトを使って、タイトルまたは内容にキーワードを含むものを検索
        ideas = Idea.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).select_related('author').prefetch_related('likes').order_by('-created_at')
    else:
        # キーワードがなければ、全件取得
        ideas = Idea.objects.select_related('author').prefetch_related('likes').all().order_by('-created_at')
        
    return render(request, 'ideas/idea_list.html', {'ideas': ideas})

@login_required
def idea_create(request):
    if request.method == "POST":
        form = IdeaForm(request.POST, request.FILES) # ← 修正後の行
        if form.is_valid():
            new_idea = form.save(commit=False)
            new_idea.author = request.user
            new_idea.save()
            return redirect('idea_list')
    else:
        form = IdeaForm()
    return render(request, 'ideas/idea_form.html', {'form': form})

@login_required
def like_idea(request, idea_id):
    idea = get_object_or_404(Idea, pk=idea_id)
    # ↓ここからが新しいロジックです
    if request.user in idea.likes.all():
        # 既にいいねしていたら、いいねを外す
        idea.likes.remove(request.user)
    else:
        # いいねしていなければ、いいねを付ける
        idea.likes.add(request.user)
    return redirect('idea_list')

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class IdeaDetailView(DetailView):
    model = Idea
    template_name = 'ideas/idea_detail.html'

class IdeaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Idea
    fields = ['title', 'content']
    template_name = 'ideas/idea_form.html'
    
    def get_success_url(self):
        return reverse_lazy('idea_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        idea = self.get_object()
        return self.request.user == idea.author
    
class IdeaDetailView(DetailView):
    model = Idea
    template_name = 'ideas/idea_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        idea = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.idea = idea
            comment.author = request.user
            comment.save()
            return redirect('idea_detail', pk=idea.pk)
        
        # フォームが無効な場合は、エラーメッセージ付きで再度ページを表示
        context = self.get_context_data()
        context['comment_form'] = form
        return self.render_to_response(context)
    
class IdeaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Idea
    template_name = 'ideas/idea_confirm_delete.html'
    success_url = reverse_lazy('idea_list')

    def test_func(self):
        idea = self.get_object()
        return self.request.user == idea.author
    
from django.http import HttpResponse

def create_superuser_view(request):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
        return HttpResponse("管理者アカウント 'admin' が作成されました。パスワードは 'adminpass' です。")
    return HttpResponse("管理者アカウントは既に存在します。")