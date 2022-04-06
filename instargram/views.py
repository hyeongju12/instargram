from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
from .forms import PostForm, CommentForm
from django.contrib import messages
from .models import Tag, Post

@login_required
def index(request):
	timesince = timezone.now() - timedelta(days=3)
	post_list = Post.objects.all().filter(
		Q(author=request.user) | Q(author__in=request.user.following_set.all())
	).filter(
		created_at__gte=timesince
	)
	suggested_user_list = get_user_model().objects.all() \
							  .exclude(pk=request.user.pk) \
							  .exclude(pk__in=request.user.following_set.all())[:3]

	comment_form = CommentForm()

	return render(request, 'instargram/index.html', {
		'suggested_user_list' : suggested_user_list,
		'post_list' : post_list,
		'comment_form' : comment_form,
	})

@login_required
def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			post.tag_set.add(*post.extract_tag_list())
			messages.success(request, "포스팅을 저장했습니다.")
			return redirect(post) # TODO : get_absolute_url 활용
	else:
		form = PostForm()

	return render(request, "instargram/post_form.html", {
		"form" : form
	})

def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	comment_form = CommentForm()
	return render(request, "instargram/post_detail.html", {
		'post' : post,
		'comment_form' : comment_form,
	})

@login_required
def post_like(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.like_user_set.add(request.user)
	#TODO like 처리 필요
	messages.success(request, f"{post}를 좋아합니다.")
	redirect_url = request.META.get('HTTP_REFERER', 'root')
	return redirect(redirect_url)

@login_required
def post_unlike(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.like_user_set.remove(request.user)
	#TODO unlike 처리 필요
	messages.success(request, f"{post}를 좋아요를 취소합니다.")
	redirect_url = request.META.get('HTTP_REFERER', 'root')
	return redirect(redirect_url)


def user_page(request, username):
	page_user = get_object_or_404(get_user_model(), username=username, is_active=True)
	post_list = Post.objects.filter(author=page_user)
	post_list_count = post_list.count() # count쿼리 생성
	#len(post_list) --> 리스트를 다 가져와서 메모리에 올리고 메모리상에  리스트의 갯수를 반환
	if request.user.is_authenticated : #로그인O :User 객체, 로그인X : Anonymous
		is_follow = request.user.following_set.filter(pk=page_user.pk).exists()
	else:
		is_follow = False

	return render(request, "instargram/user_page.html", {
		'page_user' : page_user,
		'post_list' : post_list,
		'post_list_count' : post_list_count,
		'is_follow' : is_follow,
	})

@login_required
def comment_new(request, post_pk):
	post = get_object_or_404(Post, pk=post_pk)

	if request.method == 'POST':
		form = CommentForm(request.POST, request.FILES)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.author = request.user
			comment.save()
			if request.is_ajax():
				return render(request, 'instargram/_comment.html', {
					"comment" : comment
				})
			return redirect(comment.post)
	else:
		form = CommentForm()
	return render(request, 'instargram/comment_form.html', {
		'form' : form,
	})