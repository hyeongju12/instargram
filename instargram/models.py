import re

from django.db import models
from django.conf import settings
from django.urls import reverse

class BaseModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True
#user를 가져오는 방법
# -> Post.objects.filter(author=user)
# -> user.post_set.all() 리버스 네임을 이용해서 가져올 수 있음.
# model명_set이 기본 셋팅값이다. 아래는 충돌이 나지 않도록 이름을 별도로 지정

class Post(BaseModel):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='my_post_set'
							   					,on_delete=models.CASCADE)
	photo = models.ImageField(upload_to="instargram/post/%Y/%m/%d")
	caption = models.CharField(max_length=500)
	tag_set = models.ManyToManyField('Tag', blank=True)
	location = models.CharField(max_length=100)
	like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
										   related_name='like_post_set')

	def __str__(self):
		return self.caption

	class Meta:
		ordering=['-id']

	def extract_tag_list(self):
		tag_name_list = re.findall(r"#([a-zA-Z\dㄱ-힣]+)", self.caption)
		tag_list = []
		for tag_name in tag_name_list:
			tag, _ = Tag.objects.get_or_create(name=tag_name)
			tag_list.append(tag)
		return tag_list

	def get_absolute_url(self):
		return reverse('instargram:post_detail', args=[self.pk])

	def is_like_user(self, user):
		return self.like_user_set.filter(pk=user.pk).exists()

class Comment(BaseModel):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	message = models.TextField()

	class Meta:
		ordering = ['-id']

class Tag(models.Model):
	name = models.CharField(max_length=50, unique=True)

	def __str__(self):
		return self.name