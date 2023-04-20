from django import forms


class CommentForm(forms.Form):

    about_driver = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'about driver',
            })
    )
    about_car = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'about car',
            })
    )
