from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm, Textarea, TextInput
from django import forms
from django.core.files import File
import urllib
import os
from datetime import datetime
from socket import error as SocketError
import errno

# Receive the pre_delete signal and delete the file associated with the model instance.
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

# Create your models here.


class User(AbstractUser):
    image = models.ImageField(upload_to="profiles/", blank=True, null=True)
    word_count = models.IntegerField(default=0)


class Word(models.Model):
    user = models.ForeignKey("User", on_delete=models.PROTECT, related_name="words")
    title = models.CharField(max_length=255)
    definition = models.TextField()
    category = models.ForeignKey(
        "Category",
        on_delete=models.PROTECT,
        related_name="categories",
        blank=True,
        null=True,
    )
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    video = models.FileField(upload_to="videos/", blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    bookmark_count = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.username,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
            "bookmark_count": self.like_count,
        }

    def get_remote_image(self):
        if self.image_url and not self.image:
            try:
                result = urllib.urlretrieve(self.image_url)
            except SocketError as e:
                if e.errno != errno.ECONNRESET:
                    raise  # Not error we are looking for
                pass  # Handle error here.
            # result = urllib.urlretrieve(self.image_url)
            self.image.save(os.path.basename(self.image_url), File(open(result[0])))
            self.save()

    def get_remote_video(self):
        if self.video_url and not self.video:
            try:
                result = urllib.urlretrieve(self.video_url)
            except SocketError as e:
                if e.errno != errno.ECONNRESET:
                    raise  # Not error we are looking for
                pass  # Handle error here.
            # result = urllib.urlretrieve(self.video_url)
            self.video.save(os.path.basename(self.video_url), File(open(result[0])))
            self.save()


class Category(models.Model):
    category = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.category}"


class Synonym(models.Model):
    title = models.ForeignKey(
        "Word", on_delete=models.CASCADE, related_name="originals"
    )
    synonym = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )


class Antonym(models.Model):
    title = models.ForeignKey(
        "Word", on_delete=models.CASCADE, related_name="original_words"
    )
    antonym = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )


class Quotation(models.Model):
    title = models.ForeignKey("Word", on_delete=models.CASCADE, related_name="quotes")
    quotation = models.TextField(null=True, blank=True)
    like_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
    )


class Like(models.Model):
    title = models.ForeignKey(
        "Quotation", on_delete=models.CASCADE, related_name="likes"
    )
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="liking_users"
    )

    def serialize(self):
        return {
            "title": self.id,
            "user": self.id,
        }


class Bookmark(models.Model):
    title = models.ForeignKey(
        "Word", on_delete=models.CASCADE, related_name="bookmarks"
    )
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="bookmarking_users"
    )

    def serialize(self):
        return {
            "title": self.id,
            "user": self.id,
        }


class Comment(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="user_comments"
    )
    title = models.ForeignKey("Word", on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    comment_at = models.DateTimeField(auto_now_add=True)


class UpdateUser(ModelForm):
    class Meta:
        model = User
        fields = ["image"]


class CreateWord(ModelForm):
    class Meta:
        model = Word
        fields = [
            "title",
            "definition",
            "image",
            "image_url",
            "video",
            "video_url",
        ]
        # widgets = {
        #     "title": TextInput(attrs={"id": "new-title"}),
        #     "definition": Textarea(attrs={"id": "new-definition"}),
        #     "image_url": TextInput(attrs={"placeholder": "image URL"}),
        #     "video_url": TextInput(attrs={"placeholder": "video URL"}),
        # }


class CreateCategory(ModelForm):
    class Meta:
        model = Category
        fields = ["category"]
        # widgets = {
        #     "category": TextInput(attrs={"id": "new-category"}),
        # }


class CreateQuotation(ModelForm):
    class Meta:
        model = Quotation
        fields = ["quotation"]
        # widgets = {"quotation": Textarea}


class CreateSynonym(ModelForm):
    class Meta:
        model = Synonym
        fields = ["synonym"]


class CreateAntonym(ModelForm):
    class Meta:
        model = Antonym
        fields = ["antonym"]


class CreateComment(ModelForm):
    class Meta:
        model = Comment
        fields = [
            "comment",
        ]
        widgets = {
            "comment": Textarea(
                attrs={"cols": 5, "style": "height: 8em", "id": "new-comment"}
            ),
        }
