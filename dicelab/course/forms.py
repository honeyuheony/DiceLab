from django import forms
from .models import Course, Semester


class CoursesCreationForm(forms.ModelForm):
    code = forms.CharField(
        max_length=10,
        label=('코스 코드'),
    )
    name = forms.CharField(
        max_length=200,
        label=('코스 이름')
    )
    semester = forms.ModelMultipleChoiceField(
        Semester.objects.all(),
    )

    class Meta:
        model = Course
        fields = (
            'code',
            'name',
            'semester',
        )


class SemesterCreationForm(forms.ModelForm):
    title = forms.CharField(
        max_length=20,
        required=True
    )

    class Meta:
        model = Semester
        fields = (
            'title',
        )
