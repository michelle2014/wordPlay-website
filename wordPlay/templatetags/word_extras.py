from django import template
from ..models import *
from django.core.paginator import Paginator
import collections

register = template.Library()

# Display categories on pages
@register.simple_tag
def category():
    categories = Category.objects.all()
    return categories


# Display words, bookmarks, likes, likeds counts on pages
@register.simple_tag(takes_context=True)
def count(context):

    user = context["user"]

    # Count words
    count = 0

    # ALl words
    words = Word.objects.all().order_by("-timestamp")

    # Current user's words
    user_words = Word.objects.filter(user=user.id).order_by("-timestamp")

    for user_word in user_words:
        count += 1

    # Count bookmarks
    bookmark_count = 0

    # Current user's bookmarks
    user_bookmarks = Bookmark.objects.filter(user=user.id)

    for user_bookmark in user_bookmarks:
        bookmark_count += 1

    # Count likes
    like_count = 0

    # Quotations liked by current user
    user_likes = Like.objects.filter(user=user.id)
    # print(user_likes)

    for user_like in user_likes:
        like_count += 1

    # Count likeds
    liked_count = 0

    all_users = User.objects.all()
    # print(all_users)

    # Quotations liked by current user
    liked_quotations = []
    for all_user in all_users:
        if all_user.id is not user.id:
            # print("true")
            other_likeds = Like.objects.filter(user=all_user)
            # print(other_likeds)
            for other_liked in other_likeds:
                liked_word = other_liked.title
                # print(word.title.user)
                # print("false")
                # print(request.user)
                if liked_word.title.user.id is user.id:
                    liked_quotations.append(liked_word)
                    liked_count += 1
    return {
        "count": count,
        "like_count": like_count,
        "bookmark_count": bookmark_count,
        "liked_count": liked_count,
    }


# Display words, bookmarks, likes, likeds counts on pages
@register.simple_tag(takes_context=True)
def trending(context, request):

    request = context["request"]
    # Trending quotations
    trending_quotes = Quotation.objects.all().order_by("-like_count")

    # Trending words
    trending_words = Word.objects.all().order_by("-bookmark_count")

    # Get three most liked quotations
    first_words = trending_words[:5]

    # Page pagination
    p_q = Paginator(trending_quotes, 10)
    page_number_q = request.GET.get("page")
    page_obj_q = p_q.get_page(page_number_q)

    # Get three most liked quotations
    first_quotes = trending_quotes[:3]

    # Page pagination
    p_w = Paginator(trending_words, 5)
    page_number_w = request.GET.get("page")
    page_obj_w = p_w.get_page(page_number_w)

    return {
        "trending_quotes": trending_quotes,
        "trending_words": trending_words,
        "first_quotes": first_quotes,
        "first_words": first_words,
        "page_obj_q": page_obj_q,
        "page_obj_w": page_obj_w,
    }


@register.simple_tag(takes_context=True)
def words(context, request):

    user = context["user"]

    words = context["words"]

    request = context["request"]

    synonyms = Synonym.objects.all()

    antonyms = Antonym.objects.all()

    quotations = Quotation.objects.all()

    word_synonyms = []

    word_antonyms = []

    word_quotations = []

    for word in words:
        for synonym in synonyms:
            if word.id == synonym.title.id:
                word_synonyms += Synonym.objects.filter(title=synonym.title.id)

    for word in words:
        for antonym in antonyms:
            if word.id == antonym.title.id:
                word_antonyms += Antonym.objects.filter(title=antonym.title.id)

    # Get the latest quotations
    ids = []
    for word in words:
        for quotation in quotations:
            if word.id == quotation.title.id:
                ids.append(word.id)
                word_quotations += Quotation.objects.filter(title=quotation.title.id)

    word_quotations.sort(key=lambda x: x.timestamp, reverse=True)
    word_quotations = set(word_quotations)

    repeats = [item for item, count in collections.Counter(ids).items() if count > 1]

    for repeat in repeats:
        repeat_word = Word.objects.get(pk=repeat)
        quotations = Quotation.objects.filter(title=repeat_word)
        for quotation in quotations:
            if len(quotation.quotation) < 1:
                repeats.remove(repeat)

    olders = []
    for repeat in repeats:
        repeat_word = Word.objects.get(pk=repeat)
        quotations = Quotation.objects.filter(title=repeat_word)
        timestamps = []
        for quotation in quotations:
            timestamps.append(quotation.timestamp)

        latest_q = Quotation.objects.get(timestamp=(max(timestamps)))

        other_q = quotations.exclude(title=repeat_word, pk=latest_q.id)
        olders.append(other_q)

    for word_quotation in word_quotations:
        for older in olders:
            for e in older:
                if e.id is word_quotation.id:
                    word_quotations = list(word_quotations)
                    word_quotations.remove(word_quotation)

    # Toggle like fontawsome color
    all_likings = []
    for quotation in quotations:
        likings = Like.objects.filter(title=quotation)
        for liking in likings:
            all_likings.append(liking)

    # Toggle bookmark fontawsome color
    all_bookmarks = Bookmark.objects.all()

    # Page pagination
    p = Paginator(words, 5)
    page_number = request.GET.get("page")
    page_obj = p.get_page(page_number)

    return {
        "user": user,
        "words": words,
        "word_synonyms": word_synonyms,
        "word_antonyms": word_antonyms,
        "word_quotations": word_quotations,
        "all_likings": all_likings,
        "all_bookmarks": all_bookmarks,
        "page_obj": page_obj,
    }
