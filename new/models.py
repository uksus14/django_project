from django.db import models
from django import forms
from project_settings import *

class Tutor(): pass
class Club(): pass
class Faculty(): pass
class Course(): pass
class Subject(): pass

class User(models.Model):
    student_id = models.IntegerField(primary_key=True)
    email = models.EmailField()
    password = models.IntegerField()
    is_superuser = models.IntegerField()

    second_name = models.CharField(max_length=2**10)
    first_name = models.CharField(max_length=2**10)

    course = models.ForeignKey(Course, on_delete=models.SET_NULL)
    tutors = models.ManyToManyField(Tutor)
    clubs = models.ManyToManyField(Club, primary_key=True)


class Subject():
    subject_name = models.CharField(max_length=64)
    faculties = models.ManyToManyField(Faculty, )


class Course():
    faculty_name = models.ForeignKey(Faculty, on_delete=models.SET_NULL)
    year = models.IntegerField()
    group = models.IntegerField()
    students = models.ManyToManyField(User)


class Club():
    students = models.ManyToManyField(User)
    club_name = models.CharField(max_length=32, primary_key=True)


class Faculty():
    students = models.ManyToManyField(User)
    faculty_name = models.CharField(max_length=8)
    subjects = models.ManyToManyField(Subject, on_delete=models.DO_NOTHING)


class Tutor(models.Model):
    subject = forms.ChoiceField(choices=TUTOR_SUBJECTS)
    student_id = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    tuties = models.