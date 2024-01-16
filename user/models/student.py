from django.db import models

ATTENDANCE_STATUS = (
    ("present", "Present"),
    ("leave", "Leave"),
)
LEAVE_TYPE_CHOICES = (("half_day", "Half Day"), ("full_day", "Full Day"))


class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{self.name}- {self.roll_number}"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=ATTENDANCE_STATUS)
    leave_type = models.CharField(
        max_length=30, choices=LEAVE_TYPE_CHOICES, null=True, blank=True
    )

    def __str__(self):
        return f"{self.student.name}- {self.status}"
