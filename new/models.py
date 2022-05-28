from msvcrt import open_osfhandle
from django.db import models
from django import forms
from project_settings import *

class Tutor(): pass
class Club(): pass
class Faculty(): pass
class Course(): pass

class User(models.Model):
    student_id = models.IntegerField(primary_key=True)
    email = models.EmailField()
    password = models.IntegerField()
    is_superuser = models.IntegerField()
    is_tutor = models.IntegerField()

    first_name = models.CharField(max_length=2**10)
    second_name = models.CharField(max_length=2**10)

    course = models.ForeignKey(Course, on_delete=models.SET_NULL)
    tutors = models.ManyToManyField(Tutor)
    clubs = models.ManyToManyField(Club, primary_key=True)

    def get_year(self):
        from datetime import datetime
        year = self.course.starting_year
        if datetime.now().month < 8:
            year -= datetime.now().year
        else:
            year -= datetime.now().year - 1
        return year
    
    def get_tutors(self):
        return self.tutors.all()
    
    def get_clubs(self):
        return self.clubs.all()
    
    def get_full_name(self):
        return f"{self.first_name} {self.second_name}"
    
    def get_short_name(self):
        return f"{self.first_name} {self.second_name[0]}."
    
    def get_full_info(self):
        if self.is_superuser:
            return f"{self.get_full_name()} (superuser)"
        elif self.is_tutor:
            is_tutor = "tutor"
        else:
            is_tutor = "not tutor"
        if self.get_tutors():
            tutors = "тьюторы: " + ", ".join(map(str, self.get_tutors()))
        else: tutors = "Тьюторов нет"
        if self.get_clubs():
            clubs = "клубы: " + ", ".join(map(str, self.get_clubs()))
        else: clubs = "Клубов нет"
        return f"({self.student_id}) {self.get_full_name()} {self.course}, {is_tutor}\n{clubs}\n{tutors}\n "
    
    def __str__(self):
        return f"{self.get_full_name()}, {self.course}"

class Course():
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL)
    starting_year = models.IntegerField()
    group = models.IntegerField()
    students = models.ManyToManyField(User)

    def get_students(self):
        return self.students.all()

    def __str__(self):
        return f"{self.faculty}-{self.group}-{self.starting_year}"


class Club():
    students = models.ManyToManyField(User)
    club_name = models.CharField(max_length=32, primary_key=True)
    club_leader = models.ForeignKey(User, on_delete=models.SET_NULL)
    club_description = models.CharField(max_length=2**10)
    club_logo = models.ImageField(upload_to='club_logos')

    def get_students(self):
        return self.students.all()
    
    def __str__(self):
        return f"{self.club_name}-лидер – {self.club_leader.get_full_name()}\n({self.club_description})"

class Faculty():
    students = models.ManyToManyField(User)
    faculty_name = models.CharField(max_length=8)

    def __str__(self):
        return self.faculty_name

class Tutor(models.Model):
    TUTOR_SUBJECTS = ("Математика", "Физика", "Химия", "Информатика", "Английский язык")
    student = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    subject = forms.ChoiceField(choices=TUTOR_SUBJECTS)
    tuties = models.ManyToManyField(User, primary_key=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.student.get_full_name()}, преподаёт {self.subject}"