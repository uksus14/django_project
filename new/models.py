from django.db import models

class Course(models.Model):
    FACULTIES = (
    ("SFHT", "Startup Finance & High Technologies"),
    ("IBHT", "Innovative Banking & High Technologies"),
    ("DHT", "Design & High Technologies"),
    ("SEST", "Software Engineering & Social Transformations"),
    ("ECOL", "Ecology & Energy Efficiency"),
    ("DMDT", "Design management & Digital Technologies"),
    ("EHI", "Engineering & Humanities probably?"),
    ("MIX", "Mix"))
    faculty = models.CharField(max_length=2**8, choices = FACULTIES)
    starting_year = models.IntegerField()
    group = models.IntegerField()

    def get_students(self):
        return self.students.all()

    def __str__(self):
        return f"{self.faculty}-{self.group}-{self.starting_year}"


class User(models.Model):
    student_id = models.IntegerField(primary_key = True)
    email = models.EmailField(max_length=254, unique=True,blank=True,null=True)
    password = models.CharField(max_length=16)
    is_superuser = models.IntegerField(default=0)

    first_name = models.CharField(max_length=2**10, default="")
    second_name = models.CharField(max_length=2**10, default="")

    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, related_name="course")

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
            is_tutor = "???????????????? ????????????????"
        else:
            is_tutor = "???? ???????????????? ????????????????"
        if self.get_tutors():
            tutors = "??????????????: " + ", ".join(map(str, self.get_tutors()))
        else: tutors = "???????????????? ??????"
        if self.get_clubs():
            clubs = "??????????: " + ", ".join(map(str, self.get_clubs()))
        else: clubs = "???????????? ??????"
        return f"({self.student_id}) {self.get_full_name()} {self.course}, {is_tutor}\n{clubs}\n{tutors}\n "

    def __str__(self):
        return f"{self.get_full_name()}, {self.course}"

class Club(models.Model):
    club_name = models.CharField(max_length=32)
    club_leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="club_leader")
    club_description = models.CharField(max_length=2**10)
    club_logo = models.ImageField()
    participants = models.ManyToManyField(User, related_name="clubs_participants")

    @property
    def imageURL(self):
        try:
            url = self.club_logo.url
        except:
            url = ''
        return url
    
    def get_students(self):
        return self.students.all()
    
    def __str__(self):
        return f"{self.club_name}-?????????? ??? {self.club_leader.get_full_name()}\n({self.club_description})"


class Tutor(models.Model):
    TUTOR_SUBJECTS = (
        ("????????????????????", "Math"),
        ("????????????", "Phys"),
        ("??????????", "Chem"),
        ("??????????????????????", "Info"),
        ("???????????????????? ????????", "Engl"))
    subject = models.CharField(max_length=2**8, choices=TUTOR_SUBJECTS)
    student = models.OneToOneField(User, related_name="student", on_delete=models.CASCADE)
    tuties = models.ManyToManyField(User, related_name="tuties")

    def __str__(self):
        return f"{self.student.get_full_name()}, ?????????????????? {self.subject}"