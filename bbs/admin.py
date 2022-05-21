from django.contrib import admin
from .models import Board, Thread, Comment

admin.site.register(Board)
admin.site.register(Thread)
admin.site.register(Comment)