from django import forms
from .models import TodoModel


class TodoModelForm(forms.ModelForm):
    class Meta:
        model = TodoModel
        fields = '__all__'

    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Task Name'})
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'Here can be your description'}
        )
    )
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'placeholder': 'mm/dd/yyyy hh:mm', 'type': 'datetime-local'})
    )
    repeat = forms.ChoiceField(
        choices=[('daily', 'Daily'), ('weekly', 'Weekly')],
        initial='daily',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    
    
