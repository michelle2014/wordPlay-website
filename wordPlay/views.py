from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import IntegrityError
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib import messages
import json
import collections
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import pyexcel as p
from pyexcel._compact import OrderedDict
from openpyxl import load_workbook
import pandas as pd
import math
from django.contrib import messages
from .models import *
import os
import csv


# Create your views here.
def index(request, category=None):

    # ALl words as context for custom template tag
    words = Word.objects.all().order_by("-timestamp")

    # All categorized words for custom template tag
    try:
        category_id = Category.objects.get(category=category).id
        words = Word.objects.filter(category=category_id).order_by("-timestamp")
    except Category.DoesNotExist:
        pass

    return render(
        request,
        "wordPlay/index.html",
        {
            "words": words,
        },
    )


def trending_quotes(request):

    # Trending quotations
    trending_quotes = Quotation.objects.all().order_by("-like_count")

    # Trending words
    words = Word.objects.all().order_by("-bookmark_count")

    # Get three most liked quotations
    first_words = words[:5]

    # Page pagination
    p = Paginator(trending_quotes, 10)
    page_number = request.GET.get("page")
    page_obj = p.get_page(page_number)

    return render(
        request,
        "wordPlay/trending_quotes.html",
        {
            "trending_quotes": trending_quotes,
            "words": words,
            "first_words": first_words,
            "page_obj": page_obj,
        },
    )


def trending_words(request):

    # Trending quotations
    trending_quotes = Quotation.objects.all().order_by("-like_count")

    # Trending words
    words = Word.objects.all().order_by("-bookmark_count")

    # Get three most liked quotations
    first_quotes = trending_quotes[:3]

    # Page pagination
    p = Paginator(words, 5)
    page_number = request.GET.get("page")
    page_obj = p.get_page(page_number)

    return render(
        request,
        "wordPlay/trending_words.html",
        {
            "words": words,
            "first_quotes": first_quotes,
            "page_obj": page_obj,
        },
    )


def quotations(request, word_id):

    # Words as context for custom template tag
    words = Word.objects.all().order_by("-timestamp")

    # Trending quotations
    trending_quotes = Quotation.objects.all().order_by("-like_count")

    # Trending words
    trending_words = Word.objects.all().order_by("-bookmark_count")

    # Get three most liked quotations
    first_words = trending_words[:5]

    # Get three most liked quotations
    first_quotes = trending_quotes[:3]

    word = Word.objects.get(pk=word_id)

    quotations = Quotation.objects.filter(title=word).order_by("-timestamp")

    # Page pagination
    p = Paginator(quotations, 10)
    page_number = request.GET.get("page")
    page_obj = p.get_page(page_number)

    return render(
        request,
        "wordPlay/quotations.html",
        {
            "word": word,
            "words": words,
            "quotations": quotations,
            "trending_quotes": trending_quotes,
            "first_words": first_words,
            "first_quotes": first_quotes,
            "page_obj": page_obj,
        },
    )


def search(request):
    # Get search input from user
    search_entry = request.GET["q"]

    entries = []
    # Get entries list
    words = Word.objects.all()
    for word in words:
        entries.append(word.title)

    # search list
    results = []

    # try to search if there is such entry in entries
    if request.method == "GET":
        if search_entry in entries:
            word_id = Word.objects.get(title=search_entry).id
            return HttpResponseRedirect("/wordPlay/word/" + str(word_id))

        else:
            for entry in entries:
                if search_entry in entry:
                    word = Word.objects.get(title=entry)
                    results.append(word)

                    return render(
                        request,
                        "wordPlay/search.html",
                        {
                            "results": results,
                        },
                    )


@login_required
def new(request):

    categories = Category.objects.all()

    if request.method == "POST":
        # Create a new word
        word = CreateWord(request.POST, request.FILES or None)

        category = request.POST.getlist("category")

        quotation = CreateQuotation(request.POST)

        synonym = CreateSynonym(request.POST)

        antonym = CreateAntonym(request.POST)

        user = User.objects.get(username=request.user)

        # Add user info

        if word.is_valid():
            user_word = word.save(commit=False)
            user_word.user = user
            user_word.save()
            word_instance = user_word
            user.word_count += 1
            user.save()

        category_string = "".join(category)

        try:
            category = Category.objects.get(category=category_string)
        except Category.DoesNotExist:
            pass

        if category:
            word_instance.category = category
            word_instance.save()

        if quotation.is_valid():
            title_quotation = quotation.save(commit=False)
            title_quotation.title = word_instance
            quotation.save()

        if synonym.is_valid():
            title_synonym = synonym.save(commit=False)
            title_synonym.title = word_instance
            synonym.save()

        if antonym.is_valid():
            title_antonym = antonym.save(commit=False)
            title_antonym.title = word_instance
            antonym.save()

        # Add success message
        messages.success(request, "A new word create successfully.")

        return HttpResponseRedirect(reverse("index"))

    return render(
        request,
        "wordPlay/new.html",
        {
            "new": CreateWord(),
            "quote": CreateQuotation(),
            "synonyms": CreateSynonym(),
            "antonyms": CreateAntonym(),
            "categories": categories,
        },
    )


@login_required
def upload(request):

    if request.method == "POST":

        excel_file = (
            request.FILES["fileToUpload"] if "filepath" in request.FILES else False
        )
        if excel_file:
            file_suffix = str(excel_file).split(".")[-1]

            # Get file with different suffix
            if file_suffix == "xls":
                data = pd.read_excel(excel_file, engine="xlrd")
            elif file_suffix == "xlsx":
                data = pd.read_excel(excel_file, engine="openpyxl")
            elif file_suffix == "ods":
                data = pd.read_excel(excel_file, engine="odf")
            elif file_suffix == "csv":
                data = pd.read_csv(excel_file, sep="\t")
            elif file_suffix == "tsv":
                data = pd.read_csv(excel_file, sep="\t")

            # If format of file to be uploaded not supported
            else:
                messages.error(
                    request,
                    "Unsupported file format. Please upload a file in formats listed above.",
                )
                return render(request, "wordPlay/import.html")

            # Create words from uploaded file
            titles = data.get("title")
            definitions = data.get("definition")
            categories = data.get("category")
            images = data.get("image")
            videos = data.get("video")
            synonyms = data.get("synonym")
            antonyms = data.get("antonym")
            quotations = data.get("quotation")
            cates = []
            words = []
            for category in categories:
                category = Category.objects.get(category=category)
                cates.append(category)

            for i in range(len(titles)):
                if images[i] == "" or (
                    isinstance(images[i], float) and math.isnan(images[i])
                ):
                    images[i] = None
                if videos[i] == "" or (
                    isinstance(videos[i], float) and math.isnan(videos[i])
                ):
                    videos[i] = None
                word = Word.objects.create(
                    user=request.user,
                    title=titles[i],
                    definition=definitions[i],
                    category=cates[i],
                    image_url=images[i],
                    video_url=videos[i],
                )
                word.save()
                words.append(word)

            # Create symnonym, antonym, quotation from file uploaded
            for i in range(len(words)):
                if synonyms[i] == "" or (
                    isinstance(synonyms[i], float) and math.isnan(synonyms[i])
                ):
                    synonyms[i] = None
                synonym = Synonym.objects.create(title=words[i], synonym=synonyms[i])
                synonym.save()
                if antonyms[i] == "" or (
                    isinstance(antonyms[i], float) and math.isnan(antonyms[i])
                ):
                    antonyms[i] = None
                antonym = Antonym.objects.create(title=words[i], antonym=antonyms[i])
                antonym.save()
                if quotations[i] == "" or (
                    isinstance(quotations[i], float) and math.isnan(quotations[i])
                ):
                    quotations[i] = None
                quotation = Quotation.objects.create(
                    title=words[i], quotation=quotations[i]
                )
                quotation.save()

            return HttpResponseRedirect(reverse("index"))

        # If no file is uploaded
        else:
            messages.error(
                request,
                "No file uploaded. Please upload a file in formats listed above.",
            )
            return render(request, "wordPlay/import.html")

    return render(request, "wordPlay/import.html")


def get_model_fields(model):
    return model._meta.fields


def download(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=words.csv"
    writer = csv.writer(response)
    for model in [Word, Synonym, Antonym, Quotation]:
        # print(model)
        name = model.__name__
        # Write headers to CSV file
        fields = get_model_fields(model)
        if fields:
            headers = fields
        else:
            headers = []
            for field in model._meta.fields:
                headers.append(field.name)
        writer.writerow(headers)
        # Write data to CSV file
        for obj in model.objects.all():
            row = []
            for field in headers:
                if field in headers:
                    val = getattr(obj, field.name)
                    if callable(val):
                        val = val()
                    row.append(val)
            writer.writerow(row)
        # Return CSV file to browser as download
    return response


@login_required
def add_quotation(request, word_id):

    word = Word.objects.get(pk=word_id)

    if request.method == "POST":
        quotation = CreateQuotation(request.POST)

        if quotation.is_valid:
            word_quotation = quotation.save(commit=False)
            word_quotation.title = word
            word_quotation.save()

        return HttpResponseRedirect("/wordPlay/quotations/" + str(word_id))

    return render(
        request,
        "wordPlay/add_quotation.html",
        {
            "word": word,
            "quote": CreateQuotation(),
        },
    )


@login_required
def edit(request, word_id):

    # Query for requested word
    try:
        word = Word.objects.get(pk=word_id)
    except Word.DoesNotExist:
        pass

    try:
        quotations = Quotation.objects.filter(title=word)
    except Quotation.DoesNotExist:
        pass

    if quotations:
        timestamps = []
        for quotation in quotations:
            timestamps.append(quotation.timestamp)

        try:
            word_quotation = Quotation.objects.get(
                title=word, timestamp=(max(timestamps))
            )
        except Quotation.DoesNotExist:
            pass

    try:
        word_category = Word.objects.get(pk=word_id).category
        category_object = Category.objects.get(category=word_category)
    except Category.DoesNotExist:
        pass

    try:
        word_synonym = Synonym.objects.get(title=word)
    except Synonym.DoesNotExist:
        pass

    try:
        word_antonym = Antonym.objects.get(title=word)
    except Antonym.DoesNotExist:
        pass

    data = {
        "title": word.title,
        "definition": word.definition,
        "image_url": word.image_url or None,
        "video_url": word.video_url or None,
    }

    quote = {
        "quotation": word_quotation.quotation or None,
    }

    synonym = {
        "synonym": word_synonym.synonym or None,
    }

    antonym = {
        "antonym": word_antonym.antonym or None,
    }

    original_word = CreateWord(initial=data)
    original_quotation = CreateQuotation(initial=quote)
    original_category = word_category.category
    category_id = word_category.id
    original_synonym = CreateSynonym(initial=synonym)
    original_antonym = CreateAntonym(initial=antonym)

    if request.method == "POST":
        # Get edited word info
        edited_word = CreateWord(request.POST, request.FILES or None)

        edited_category = request.POST.getlist("category")

        edited_quotation = CreateQuotation(request.POST)

        edited_synonym = CreateSynonym(request.POST)

        edited_antonym = CreateAntonym(request.POST)

        # Update word
        if edited_word.is_valid():
            word.title = edited_word.cleaned_data["title"]
            word.definition = edited_word.cleaned_data["definition"]
            word.image_url = edited_word.cleaned_data["image_url"]
            word.image = edited_word.cleaned_data["image"]
            word.video_url = edited_word.cleaned_data["video_url"]
            word.video = edited_word.cleaned_data["video"]
            word.save()

        if edited_category:
            category_string = "".join(edited_category)

            try:
                category = Category.objects.get(category=category_string)
            except Category.DoesNotExist:
                pass

            word.category = category
            word.save()

        if edited_quotation.is_valid():
            word_quotation.quotation = edited_quotation.cleaned_data["quotation"]
            word_quotation.save()

        if edited_synonym.is_valid():
            word_synonym.synonym = edited_synonym.cleaned_data["synonym"]
            word_synonym.save()

        if edited_antonym.is_valid():
            word_antonym.antonym = edited_antonym.cleaned_data["antonym"]
            word_antonym.save()

        return HttpResponseRedirect(reverse("index"))

    return render(
        request,
        "wordPlay/edit.html",
        {
            "word": word,
            "original_word": original_word,
            "original_quotation": original_quotation,
            "original_synonym": original_synonym,
            "original_antonym": original_antonym,
            "original_category": original_category,
        },
    )


@login_required
def delete(request, word_id):

    if request.method == "POST":
        # Query for requested word
        try:
            word = Word.objects.get(pk=word_id)
        except Word.DoesNotExist:
            pass

        word.delete()

        return HttpResponseRedirect(reverse("index"))


@login_required
def create_category(request):

    if request.method == "POST":
        # Create a new category
        category = request.POST.get("category")
        new = Category(category=category)
        new.save()

    return render(
        request,
        "wordPlay/create_category.html",
        {
            "create": CreateCategory(),
        },
    )


@login_required
def profile(request, username):

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        pass

    if request.method == "POST":

        user = User.objects.get(username=request.user)
        image = UpdateUser(request.POST, request.FILES or None)

        if image.is_valid():
            if user.image:
                user.image.delete(save=True)

            image = UpdateUser(
                request.POST, request.FILES or None, instance=user
            ).save()

        return HttpResponseRedirect(reverse("profile", args=(username,)))

    return render(
        request,
        "wordPlay/profile.html",
        {
            "update_user": UpdateUser(),
            "user": user,
        },
    )


def words_view(request, username):

    user_id = User.objects.get(username=username).id
    user = User.objects.get(username=username)

    # Currnet user's words as context for custom template tag
    words = Word.objects.filter(user=user_id).order_by("-timestamp")

    return render(
        request,
        "wordPlay/my_words.html",
        {
            "update_user": UpdateUser(),
            "words": words,
            "user": user,
        },
    )


def word(request, word_id):

    # Currnet user's words as context for custom template tag
    words = Word.objects.all().order_by("-timestamp")

    try:
        word_id = int(word_id)
        word = Word.objects.get(pk=int(word_id))
    except ValueError:
        try:
            word = Word.objects.get(title=word_id)
        except Word.DoesNotExist:
            return HttpResponseRedirect(reverse("new"))

    # Count likeds
    liked_count = 0

    all_users = User.objects.all()

    # Quotations liked by current user
    quotations = []
    for all_user in all_users:
        if all_user.id is not request.user.id:
            other_likeds = Like.objects.filter(user=all_user)
            for other_liked in other_likeds:
                w = other_liked.title
                if w.title.user.id is request.user.id:
                    quotations.append(w)
                    liked_count += 1

    # Toggle bookmark fontawsome color
    all_bookmarks = Bookmark.objects.all()

    # Toggle like fontawsome color
    all_likings = []
    for quotation in quotations:
        likings = Like.objects.filter(title=quotation)
        for liking in likings:
            all_likings.append(liking)

    try:
        word_synonym = Synonym.objects.get(title=word)
    except Synonym.DoesNotExist:
        pass

    try:
        word_antonym = Antonym.objects.get(title=word)
    except Antonym.DoesNotExist:
        pass

    # Try to get the latest quotation of the word
    try:
        word_quotations = Quotation.objects.filter(title=word)
        word_quotation = word_quotations.order_by("-timestamp")[0]
    except Quotation.DoesNotExist:
        word_quotation = word_quotations = None

    add_comment = CreateComment()

    comments = Comment.objects.filter(title=word).order_by("-comment_at")

    # Page pagination
    p = Paginator(comments, 5)
    page_number = request.GET.get("page")
    page_obj = p.get_page(page_number)

    # Add comment
    if request.method == "POST":

        # Get comment text
        comment = request.POST.get("comment")
        new = Comment(comment=comment, user=request.user, title=word)
        new.save()

        return HttpResponseRedirect(reverse("word", args=(word_id,)))

    return render(
        request,
        "wordPlay/word.html",
        {
            "word": word,
            "words": words,
            "word_synonym": word_synonym,
            "word_antonym": word_antonym,
            "word_quotation": word_quotation,
            "page_obj": page_obj,
            "all_bookmarks": all_bookmarks,
            "all_likings": all_likings,
            "add_comment": add_comment,
            "comments": comments,
        },
    )


def bookmarks_view(request, username):

    user = User.objects.get(username=username)
    # Currnet user's bookmarked words as context for custom template tag
    user_bookmarks = Bookmark.objects.filter(user=user)

    words = []
    for user_bookmark in user_bookmarks:
        word = user_bookmark.title
        words.append(word)

    words.sort(key=lambda x: x.timestamp, reverse=True)

    return render(
        request,
        "wordPlay/bookmarks.html",
        {
            "update_user": UpdateUser(),
            "words": words,
            "user": user,
        },
    )


@login_required
def leaderboard(request, username):
    word_counting = []
    users = User.objects.all()
    for user in users:
        word_counting.append(user.word_count)

    max_word = max(word_counting)
    top_users = User.objects.filter(word_count=max_word)

    return render(
        request,
        "wordPlay/leaderboard.html",
        {
            "max_word": max_word,
            "top_users": top_users,
        },
    )


@login_required
def likes(request, quotation_id, user_id):

    # Likes API
    if request.method == "POST":
        # Get JS word data
        data = json.loads(request.body)

        if data.get("quotation") is not None:
            quotation_id = data.get("quotation")

        if data.get("user") is not None:
            user_id = data.get("user")

        quotation = Quotation.objects.get(pk=quotation_id)
        user = User.objects.get(pk=user_id)

        quotation_likes = Like.objects.filter(title=quotation)
        likers = []
        if quotation_likes:
            for e in quotation_likes:
                likers.append(e.user)

            if user not in likers:
                like = Like(title=quotation, user=user)
                like.save()

                quotation.like_count += 1
                quotation.save()

            else:
                e.delete()
                quotation.like_count -= 1
                quotation.save()

        else:
            like = Like(title=quotation, user=user)
            quotation.like_count += 1

            like.save()
            quotation.save()

        likes = Like.objects.filter(title=quotation)
        user_likes = Like.objects.filter(user=request.user.id)

        content = {
            "likes": [like.serialize() for like in likes],
            "user_likes": [user_like.serialize() for user_like in user_likes],
        }

        return JsonResponse(
            content,
            safe=False,
        )

    # Post must be via GET or PUT
    else:
        return JsonResponse({"error": "GET or POST request required."}, status=400)


def add_bookmarks(request, word_id, user_id):

    # Bookmark API
    if request.method == "POST":
        # Get JS word data
        data = json.loads(request.body)

        if data.get("word") is not None:
            word_id = data.get("word")

        if data.get("user") is not None:
            user_id = data.get("user")

        word = Word.objects.get(pk=word_id)
        user = User.objects.get(pk=user_id)

        bookmarks = Bookmark.objects.filter(title=word)
        bookmakers = []
        if bookmarks:
            for e in bookmarks:
                bookmakers.append(e.user)

            if user not in bookmakers:
                bookmark = Bookmark(title=word, user=user)
                bookmark.save()
                word.bookmark_count += 1
                word.save()

            else:
                e.delete()
                word.bookmark_count -= 1
                word.save()

        else:
            bookmark = Bookmark(title=word, user=user)
            word.bookmark_count += 1
            bookmark.save()
            word.save()

        bookmarks = Bookmark.objects.filter(title=word)
        user_bookmarks = Bookmark.objects.filter(user=request.user.id)
        content = {
            "bookmarks": [bookmark.serialize() for bookmark in bookmarks],
            "user_bookmarks": [
                user_bookmark.serialize() for user_bookmark in user_bookmarks
            ],
        }

        return JsonResponse(content, safe=False)

    # Post must be via GET or PUT
    else:
        return JsonResponse({"error": "GET or POST request required."}, status=400)


def likes_view(request, username):

    user = User.objects.get(username=username)

    # For words context
    words = Word.objects.filter(user=user).order_by("-timestamp")

    # Quotations liked by current user
    user_likes = Like.objects.filter(user=user)

    quotations = []
    for user_like in user_likes:
        word = user_like.title.id
        quotation = Quotation.objects.get(pk=word)
        if quotation not in quotations:
            quotations.append(quotation)

    quotations.sort(key=lambda x: x.title.timestamp, reverse=True)

    # Page pagination
    p = Paginator(quotations, 5)
    page_number = request.GET.get("page")
    page_obj = p.get_page(page_number)

    return render(
        request,
        "wordPlay/likes.html",
        {
            "update_user": UpdateUser(),
            "words": words,
            "quotations": quotations,
            "page_obj": page_obj,
            "user": user,
        },
    )


def likeds_view(request, username):

    user = User.objects.get(username=username)

    # For words context
    words = Word.objects.filter(user=user).order_by("-timestamp")

    # Count likeds
    liked_count = 0

    other_users = User.objects.exclude(pk=user.id)

    # Quotations liked by current user
    quotations = []

    for other_user in other_users:
        # if all_user.id is not request.user.id:
        other_likeds = Like.objects.filter(user=other_user)
        for other_liked in other_likeds:
            word = other_liked.title
            if word.title.user.id is user.id:
                liked_count += 1

                if word not in quotations:
                    quotations.append(word)

    quotations.sort(key=lambda x: x.title.timestamp, reverse=True)

    # Page pagination
    p = Paginator(quotations, 5)
    page_number = request.GET.get("page")
    page_obj = p.get_page(page_number)

    return render(
        request,
        "wordPlay/likeds.html",
        {
            "update_user": UpdateUser(),
            "words": words,
            "quotations": quotations,
            "page_obj": page_obj,
            "user": user,
        },
    )


def about(request):
    return render(request, "wordPlay/about.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "wordPlay/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "wordPlay/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Validate email
        try:
            validate_email(email)
        except ValidationError as message:
            return render(
                request,
                "wordPlay/register.html",
                {
                    "message": message,
                },
            )

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "wordPlay/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "wordPlay/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "wordPlay/register.html")
