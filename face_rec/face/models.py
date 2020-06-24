from django.db import models
from django.contrib import admin

class Registration(models.Model):
    First_name = models.CharField(max_length=200)
    Last_name = models.CharField(max_length=200)
    DOB = models.CharField(max_length=200)
    DOJ_course = models.CharField(max_length=200)
    Phone = models.CharField(max_length=200)
    Address = models.TextField()
    Gender = models.CharField(max_length=200)
    Qualification = models.CharField(max_length=200)
    Semester = models.IntegerField(null = True)
    Course = models.CharField(max_length=200, blank = True)
    Class = models.IntegerField(null = True)
    Parent_phone = models.CharField(max_length=200)
    Email = models.EmailField(max_length=200)
    Password = models.CharField(max_length=200)
    Registration_date = models.DateField()
    About_website = models.TextField()
    User_role = models.CharField(max_length=200)

class Attendance(models.Model):
    Name = models.CharField(max_length=200)
    Email = models.EmailField()
    Date = models.CharField(max_length=200)
    Time = models.CharField(max_length=200)

class Messages(models.Model):
    Category = models.CharField(max_length=200)
    Name = models.CharField(max_length=200)
    From_email = models.EmailField()
    To_email = models.EmailField()
    Message_content = models.TextField(default='Nil')

class Feedback(models.Model):
    Student_name = models.CharField(max_length=200)
    Student_email = models.EmailField()
    Teacher_email = models.EmailField()
    Course_name = models.CharField(max_length=200)
    Feedback_text = models.TextField(default='Nil')
    Submission_date = models.DateField()
    Feed_reg = models.ForeignKey(Registration, on_delete=models.CASCADE)

class Requests(models.Model):
    Name = models.CharField(max_length=200)
    Email = models.EmailField()
    User_category = models.CharField(max_length=200)
    Old_password = models.CharField(max_length=200)
    New_password = models.CharField(max_length=200)
    Req_reg = models.ForeignKey(Registration, on_delete=models.CASCADE)

class Course(models.Model):
    Department = models.CharField(max_length=200)
    Course = models.CharField(max_length=200)
    Subject = models.CharField(max_length=200)

class Blogs(models.Model):
    Name = models.CharField(max_length=200)
    Blog_content = models.TextField()
    Image = models.ImageField()
    Date_blog = models.DateField()
    Approval_status = models.CharField(max_length=200)

class Exam(models.Model):
    Student_name = models.CharField(max_length=200)
    Student_email = models.EmailField()
    Teacher_name = models.CharField(max_length=200)
    Subject_name = models.CharField(max_length=200)
    Question = models.TextField()
    Option1 = models.TextField()
    Option2 = models.TextField()
    Option3 = models.TextField()
    Correct_answer = models.TextField()
    Lock = models.CharField(max_length=200)
    Time_start = models.DateTimeField()
    Time_stop = models.DateTimeField()
    Exam_reg = models.ForeignKey(Registration, on_delete=models.CASCADE)

class Exam_results(models.Model):
    Student_name = models.CharField(max_length=200)
    Student_email = models.EmailField(max_length=200)
    Teacher_name = models.CharField(max_length=200)
    Subject_name = models.CharField(max_length=200)
    Total_marks = models.IntegerField()
    Acquired_marks = models.IntegerField()
    Grade = models.CharField(max_length=200)
    Time_stop = models.DateTimeField(auto_now=True)
    Exam_res_reg = models.ForeignKey(Registration, on_delete=models.CASCADE)
