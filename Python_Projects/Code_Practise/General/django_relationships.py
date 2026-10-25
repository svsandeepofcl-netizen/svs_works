from django.db import models

class Classroom(models.Model):
    name = models.CharField(max_length=50)

class Club(models.Model):
    club_name=models.CharField(max_length=50)

class Locker(models.Model):
    locker_id=models.CharField(max_length=10)

class Student(models.Model):
    student_name=models.CharField(max_length=50)
    club=models.ManyToManyField(Club, blank=True)
    class_room = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    student_locker_id=models.OneToOneField(Locker, on_delete=models.CASCADE)