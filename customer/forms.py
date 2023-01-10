from django import forms

# This is a custom form used in the tempate where the user is prompted to input how many tickets they want
# There are three fields, one for each type of ticket (student, adults, children). The user can input how many tickets
# of each type they would like to have
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
