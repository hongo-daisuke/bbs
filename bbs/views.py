from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import Thread, Board, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm, ThreadCreateForm
from django.db.models import Q, Prefetch, Count, FilteredRelation
import sqlalchemy as sa
from sqlalchemy import func, desc


# Create your views here.

class IndexView(TemplateView):
    def get(self, request):
        t1 = Thread.sa.table.alias('t1')
        t2 = Comment.sa.table.alias('t2')
        queryset = Board.sa.query(
            Board.sa.name,
            Board.sa.id,
            t1.c.name.label('threadName'),
            t1.c.id.label('threadId')
        ).select_from(
            Board.sa.table.
            outerjoin(t1, sa.and_(t1.c.board_id == Board.sa.id)).
            outerjoin(t2, sa.and_(t2.c.threads_id == t1.c.id))
        ).group_by(t2.c.threads_id).order_by(desc(func.count(t2.c.threads_id)))
        #queryset = queryset.statement
        queryset = queryset.all()

        params = {}
        for query in queryset:
            if params.get(query[0]):
                params[query[0]][query[1]].update({query[2]:query[3]})
            else:
                params[query[0]] = {query[1]:{query[2]:query[3]}}

        context = {
            'object' : params,
        }
        return render(request, 'bbs/thread_home.html', context)
    
class BoardListView(ListView):
    model = Board

class ThreadMenuView(TemplateView):
    def get(self, request, pk, *args, **kwargs):
        queryset = Thread.objects.only('id', 'name').filter(board_id=pk)

        context = {
            'object_list' : queryset,
            'thread_id' : pk,
            'form':ThreadCreateForm()
        }
        # スレッド作成画面用のテンプレートの値が空のフォームをレンダリング
        return render(request, 'bbs/thread_menu.html', context)
    
    def post(self, request, *args, **kwargs):
        
        form = ThreadCreateForm(request.POST)
        thread_id = request.POST.get('thread_id')

        queryset = Thread.objects.filter(board_id=thread_id)
        context = {
            'object_list' : queryset,
            'thread_id' : thread_id,
            'form':ThreadCreateForm()
        }

        if not form.is_valid():
            context['form'] = form
            return render(request, 'bbs/thread_menu.html', context)
        
        save_comment = form.save(commit=False)
        save_comment.board = Board.objects.get(id=thread_id)
        save_comment.save()
        return render(request, 'bbs/thread_menu.html', context)

class ThreadDetailView(DetailView):
    def get(self, request, pk, *args, **kwargs):
        queryset = Comment.objects.filter(threads_id=pk)
        context = {
            'object_list' : queryset,
            'form':CommentForm()
        }

        return render(request, 'bbs/thread_detail.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        
        form = CommentForm(request.POST, request.FILES)
        queryset = Comment.objects.filter(threads_id=pk)
        context = {
            'object_list' : queryset,
            'form':CommentForm()
        }

        if not form.is_valid():
            context['form'] = form
            return render(request, 'bbs/thread_detail.html', context)

        save_comment = form.save(commit=False)
        save_comment.threads = Thread.objects.get(id=pk)
        save_comment.save()
        return render(request, 'bbs/thread_detail.html', context)



class ThreadSearchView(ListView):
    def get(self, request, *args, **kwargs):
        
        queryset = Thread.objects.all()
        
        # 検索ワードを取得
        keyword = request.GET.get('keyword')
                
        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword)
            )

        context = {
            'keyword' : keyword,
            'object_list' : queryset
        }

        return render(request, 'bbs/thread_search.html', context)