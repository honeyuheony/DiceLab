from django import forms
from .models import Course

MY_CHOICES = (('2018_Spring', '2018_Spring'),
              ('2019_Spring', '2019_Spring'),
              ('2020_Spring', '2020_Spring'),
              ('2021_Spring', '2021_Spring'),
              ('2018_Fall', '2018_Fall'),
              ('2019_Fall', '2019_Fall'),
              ('2020_Fall', '2020_Fall'),
              ('2021_Fall', '2021_Fall'),)


class CoursesCreationForm(forms.ModelForm):
    code = forms.CharField(
        max_length=10,
        label=('코스 코드'),
    )
    name = forms.CharField(
        max_length=200,
        label=('코스 이름')
    )
    semester = forms.MultipleChoiceField(
        choices=MY_CHOICES
    )

    class Meta:
        model = Course
        fields = (
            'code',
            'name',
            'semester',
        )
