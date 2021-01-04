from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Word)
admin.site.register(Like)
admin.site.register(Synonym)
admin.site.register(Antonym)
admin.site.register(Quotation)
admin.site.register(Bookmark)
admin.site.register(Category)
admin.site.register(Comment)