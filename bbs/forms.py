from django import forms
from .models import Thread, Comment
from django.core.exceptions import ObjectDoesNotExist
from . import ngWordList

class CommentForm(forms.ModelForm):
    """コメント投稿用フォーム"""
    class Meta:
        # 利用するモデルを指定
        model = Comment

        # 利用するモデルのフィールドを指定
        fields = ('user_name', 'email', 'comment', 'comment_image',)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs = {'placeholder': '名無し太郎'}

        self.fields['email'].widget.attrs = {'placeholder': '○○○@○○○.○○○'}

        # comment に必須を設定
        self.fields['comment'].required = True
        self.fields['comment'].widget.attrs = {'placeholder': '本文を入力して下さい。'}

        for field in self.fields.values(): 
            field.widget.attrs["class"] = 'form-control'
            
        self.fields['comment'].widget.attrs["rows"] = "5"


    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        
        if comment in ngWordList.ng_word_list:
            raise forms.ValidationError('投稿に不適切な内容が含まれています。')
        
        return comment
    
    def clan(self):
        super().clean()
        
class ThreadCreateForm(forms.ModelForm):
    """スレッド作成画面用のフォーム"""
    class Meta:
        # 利用するモデルを指定
        model = Thread

        # 利用するモデルのフィールドを指定
        fields = ('name', )
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # name に必須を設定
        self.fields['name'].required = True

        # プレースホルダーをつける
        self.fields['name'].widget.attrs = {'placeholder': 'スレッドのタイトルを入力して下さい。', 'cols': '80', 'rows': '10'}
        
        
    def clean_name(self):
        # 入力値はcleaned_dataから取得する
        thread_name = self.cleaned_data.get('name')
        
        try:
            exists_thread_name = Thread.objects.filter(name=thread_name).exists()
        except ObjectDoesNotExist:
            raise forms.ValidationError('タイトルが正しく入力されていません。')

        if exists_thread_name:
            raise forms.ValidationError('入力されたタイトルのスレッドは既に存在します。')
        
        return thread_name

    # モデルの登録変更を伴うフォームでは、親クラスの clean() を明示的に呼び出すとよい
    def clean(self):

        super().clean()