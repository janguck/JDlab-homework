from django import forms
from board.models import board

class WriteFormView(forms.ModelForm):
    class Meta:
        model = board
        fields = ['board_description']