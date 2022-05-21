from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    """コメント投稿用フォーム"""
    class Meta:
        # 利用するモデルを指定
        model = Contact

        # 利用するモデルのフィールドを指定
        fields = ('contact_type', 'user_name', 'user_mail', 'contact')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['contact_type'].required = True
        self.fields['contact_type'].label = 'お問合せの種類'
        
        self.fields['user_name'].required = True
        self.fields['user_name'].widget.attrs = {'placeholder': '名前を入力して下さい。'}

        self.fields['user_mail'].required = True
        self.fields['user_mail'].widget.attrs = {'placeholder': '○○○@○○○.○○○'}

        self.fields['contact'].required = True
        self.fields['contact'].widget.attrs = {'placeholder': '本文を入力して下さい。'}

        for field in self.fields.values(): 
            field.widget.attrs["class"] = 'form-control'
            
        self.fields['contact'].widget.attrs["rows"] = "5"
        
    def clan(self):
        super().clean()