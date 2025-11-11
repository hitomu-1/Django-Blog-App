from django import forms

from blog.models import Comment, Reply


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "text"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "名前",
                    "class": "form-control",
                    "id": "name",
                }
            ),
            "text": forms.Textarea(
                attrs={
                    "placeholder": "コメントを入力してください",
                    "class": "form-control",
                    "id": "text",
                }
            ),
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ["name", "text"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "名前",
                    "class": "form-control",
                    "id": "name",
                }
            ),
            "text": forms.Textarea(
                attrs={
                    "placeholder": "返信を入力してください",
                    "class": "form-control",
                    "id": "text",
                }
            ),
        }
