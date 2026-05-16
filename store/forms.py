from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, f'{i} yulduz') for i in range(1, 6)],
        widget=forms.RadioSelect,
        label="Reyting"
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        labels = {
            'comment': 'Sharh'
        }
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Kitob haqida fikringizni yozing...'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs['class'] = 'form-control'