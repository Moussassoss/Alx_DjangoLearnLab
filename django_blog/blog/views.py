# blog/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment, Tag
from .forms import PostForm, CommentForm, UserRegisterForm, ProfileForm
from django.contrib.auth import login
from django.db.models import Q

# Post list with simple search
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        tag = self.request.GET.get('tag')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q) | Q(author__username__icontains=q)).distinct()
        if tag:
            qs = qs.filter(tags__name__iexact=tag)
        return qs

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comment_form'] = CommentForm()
        return ctx

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        return response

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

# Comment create, edit, delete as simple function views (keeps templates easy)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def add_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect(post.get_absolute_url())

@login_required
def edit_comment(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.author != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect(comment.post.get_absolute_url())
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/comment_edit.html', {'form': form, 'comment': comment})

@login_required
def delete_comment(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.author != request.user:
        return HttpResponseForbidden()
    post = comment.post
    comment.delete()
    return redirect(post.get_absolute_url())

# Auth views: registration and profile
from django.views import View

class RegisterView(FormView):
    template_name = 'blog/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

class ProfileView(LoginRequiredMixin, View):
    template_name = 'blog/profile.html'

    def get(self, request):
        form = ProfileForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile')
        return render(request, self.template_name, {'form': form})
