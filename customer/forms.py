from django import forms

class TicketsForm(forms.Form):
    students = forms.IntegerField(min_value=0)
    children = forms.IntegerField(min_value=0)
    adults = forms.IntegerField(min_value=0)
    class Meta:
        fields=('students', 'children', 'adults', )
        labels = {
            'students': "Students:",
            "children": "Children:",
            'adults': "Adults: " ,
        }
