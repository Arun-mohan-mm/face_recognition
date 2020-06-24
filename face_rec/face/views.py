from django.shortcuts import render
from .models import *
from django.contrib import messages
import requests
from bs4 import BeautifulSoup
from django.core.files.storage import FileSystemStorage
import pytz
from django.db.models import Q
from django.utils import timezone

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2,os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime, calendar
import time
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from datetime import date
from dateutil import relativedelta


def face_template(request):
    return render(request,'face_template.html')

def home(request):
    local_tz = pytz.timezone("Asia/Calcutta")
    fg = Exam.objects.all()
    kk = []
    for i in fg:
        bb = i.Time_start
        cpp = bb.replace(tzinfo=pytz.utc).astimezone(local_tz)
        bbn = cpp.strftime("%Y-%B-%d %H:%M:%S %p")
        if bbn not in kk:
            kk.append('Student name - ')
            kk.append(i.Student_name)
            kk.append('; ')
            kk.append('Subject name - ')
            kk.append(i.Subject_name)
            kk.append('; ')
            kk.append('Start time - ')
            ft = i.Time_start
            ftt = ft.replace(tzinfo=pytz.utc).astimezone(local_tz)
            fty = ftt.strftime("%Y-%B-%d %H:%M:%S %p")
            kk.append(fty)
            kk.append('; ')
            kk.append('Stop time - ')
            fte = i.Time_stop
            ftee = fte.replace(tzinfo=pytz.utc).astimezone(local_tz)
            fty1 = ftee.strftime("%Y-%B-%d %H:%M:%S %p")
            kk.append(fty1)
            kk.append('mh')

    return render(request, 'home.html',{'kk':kk})

def student_home(request):
    return render(request, "student_home.html")

def teacher_home(request):
    return render(request, "teacher_home.html")

def admin_home(request):
    return render(request, "admin_home.html")

def g_m(request):
    bb = Messages.objects.filter(Category = 'guest')
    return render(request,'guest_message.html',{'bb':bb})

def m_m(request):
    p = Registration.objects.get(id = request.session['logg'])
    bb = Messages.objects.filter(To_email = p.Email)
    return render(request,'message.html',{'bb':bb})

def delete_g_msg(request, id):
    Messages.objects.get(id=id).delete()
    bb = Messages.objects.filter(Category='guest')
    messages.success(request, 'Message deleted successfully')
    return render(request, 'guest_message.html', {'bb': bb})

def del_msg_admin(request,id):
    Messages.objects.get(id = id).delete()
    p = Registration.objects.get(id = request.session['logg'])
    bb = Messages.objects.filter(To_email=p.Email)
    messages.success(request, 'Message deleted successfully')
    return render(request,'message.html',{'bb':bb})

def reply_msg_admin(request,id):
    pa = Messages.objects.get(id = id)
    p = Registration.objects.get(id = request.session['logg'])
    bb = Messages.objects.filter(To_email = p.Email)
    if request.method == 'POST':
        f_email = request.POST.get('f_email')
        to_email = request.POST.get('to_email')
        msg_cont = request.POST.get('msg_cont')
        pa1 = Messages()
        pa1.Category = p.User_role
        pa1.From_email = to_email
        pa1.To_email = f_email
        pa1.Message_content = msg_cont
        pa1.save()
        messages.success(request, 'Message reply successful')
        return render(request, 'message.html', {'bb': bb})
    return render(request,'reply_msg_admin.html',{'pa':pa})

def sent_msg_admin(request):
    kk = Registration.objects.all()
    p = Registration.objects.get(id = request.session['logg'])
    bb = Messages.objects.filter(To_email = p.Email)
    if request.method == 'POST':
        to_em = request.POST.get('to_em')
        ddp = str(to_em)
        gg = ddp.split()
        pnm = gg[0]
        msg_cont = request.POST.get('msg_cont')
        nm = Messages()
        nm.Category = p.User_role
        kkp = Registration.objects.get(id = request.session['logg'])
        nm.From_email = kkp.Email
        nm.To_email = pnm
        nm.Message_content = msg_cont
        nm.save()
        messages.success(request, 'Message sent successfully')
        return render(request, 'message.html', {'bb': bb})
    return render(request,'sent_msg_admin.html',{'kk':kk})

def m_m2(request):
    p = Registration.objects.get(id = request.session['logg'])
    bb = Messages.objects.filter(To_email = p.Email)
    return render(request,'message2.html',{'bb':bb})

def feedback(request):
    x = datetime.datetime.now()
    y = x.strftime("%Y-%m-%d")
    dd = Registration.objects.get(id = request.session['logg'])
    ds = Course.objects.all()
    fd = []
    for i in ds:
        if i.Course not in fd:
            fd.append(i.Course)
    if request.method == 'POST':
        course = request.POST.get('select')
        text_feed = request.POST.get('text_feed')
        qw = Feedback()
        qw.Student_name = dd.First_name
        qw.Student_email = dd.Email
        qw.Teacher_email = 'Nil@Nil'
        qw.Course_name = course
        qw.Feedback_text = text_feed
        qw.Submission_date = y
        qw.Feed_reg = dd
        qw.save()
        messages.success(request, 'Thank you for your valuable feedback')
        return render(request, 'student_home.html')
    return render(request,'feedback.html',{'fd':fd,'dd':dd})

def del_msg_student(request,id):
    Messages.objects.get(id = id).delete()
    p = Registration.objects.get(id = request.session['logg'])
    bb = Messages.objects.filter(To_email = p.Email)
    messages.success(request, 'Message deleted successfully')
    return render(request,'message2.html',{'bb':bb})

def reply_msg_student(request,id):
    pa = Messages.objects.get(id = id)
    p = Registration.objects.get(id = request.session['logg'])
    bb = Messages.objects.filter(To_email = p.Email)
    if request.method == 'POST':
        f_email = request.POST.get('f_email')
        to_email = request.POST.get('to_email')
        msg_cont = request.POST.get('msg_cont')
        km = p.First_name
        kmd = p.Last_name
        pa1 = Messages()
        pa1.Name = str(km)+' '+str(kmd)
        pa1.Category = p.User_role
        pa1.From_email = to_email
        pa1.To_email = f_email
        pa1.Message_content = msg_cont
        pa1.save()
        messages.success(request, 'Message reply successful')
        return render(request, 'message2.html', {'bb': bb})
    return render(request,'reply_msg_student.html',{'pa':pa})

def sent_msg_student(request):
    kk = Registration.objects.all()
    p = Registration.objects.get(id = request.session['logg'])
    bb = Messages.objects.filter(To_email = p.Email)
    if request.method == 'POST':
        to_em = request.POST.get('to_em')
        ddp = str(to_em)
        gg = ddp.split()
        pnm = gg[0]
        msg_cont = request.POST.get('msg_cont')
        nm = Messages()
        nm.Category = p.User_role
        kkp = Registration.objects.get(id = request.session['logg'])
        nm.From_email = kkp.Email
        nm.To_email = pnm
        nm.Message_content = msg_cont
        nm.save()
        messages.success(request, 'Message sent successfully')
        return render(request, 'message2.html', {'bb': bb})
    return render(request,'sent_msg_student.html',{'kk':kk})

def add_course(request):
    if request.method == 'POST':
        dept = request.POST.get('dept')
        cou = request.POST.get('course')
        sub = request.POST.get('sub')
        cc = Course()
        cc.Department = dept
        cc.Course = cou
        cc.Subject = sub
        cc.save()
        cou = Course.objects.all()
        messages.success(request, 'Course has been added')
        return render(request, 'course.html', {'cou': cou})
    return render(request,'add_course.html')


def about(request):
    df = Registration.objects.get(User_role = 'admin')
    dm = Registration.objects.filter(User_role = 'teacher')
    return render(request,'about.html',{'df':df,'dm':dm})

def abb(request):
    amm = Registration.objects.get(User_role = 'admin')
    if request.method == 'POST':
        abbt = request.POST.get('abbt')
        idd = request.POST.get('idd')
        try:
            adc = Registration.objects.get(id = idd)
            adc.About_website = abbt
            adc.save()
            messages.success(request, 'Content added')
            return render(request, 'admin_home.html')
        except:
            adc = About()
            adc.About_website = abbt
            adc.save()
            messages.success(request, 'Content added')
            return render(request, 'admin_home.html')
    return render(request,'about_content.html',{'amm':amm})

def news(request):
    page = requests.get('https://www.indiatoday.in/education-today')
    soup = BeautifulSoup(page.content,'html.parser')
    week = soup.find(class_ = 'special-top-news')
    wm = week.find(class_ = 'itg-listing')
    w = wm.find_all('a')
    ww = []
    for x in w:
        ww.append(x.get_text())
    x = datetime.datetime.now()
    return render(request,'news.html',{'ww':ww,'x':x})

def admin_rg(request):
    if request.method == 'POST':
        lk = Registration.objects.all()
        for t in lk:
            if t.User_role == 'admin':
                messages.success(request, 'You are not allowed to be registered as admin')
                return render(request, 'home.html')
        x = datetime.datetime.now()
        z = x.strftime("%Y-%m-%d")
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if (not first_name.isalpha()) or (not last_name.isalpha()):
            messages.success(request, 'Non-alphabetic characters not allowed in name')
            return render(request, 'register_admin.html')

        email = request.POST.get('email')
        psw = request.POST.get('psw')
        admin = request.POST.get('adminn1')
        addr = request.POST.get('addr')
        dob = request.POST.get('dob')

        dob1 = dob.split('-')
        aa = int(dob1[0])
        ab = int(dob1[1])
        ac = int(dob1[2])
        t = date.today()
        u = date(aa, ab, ac)
        v = relativedelta.relativedelta(t, u)
        v = v.years
        if v < 18:
            messages.success(request, 'Registration allowed for admin above 18 years old')
            return render(request, 'register_admin.html')

        gender = request.POST.get('gender')
        phone = request.POST.get('phone')

        if len(phone) != 10:
            messages.success(request, 'Entered phone number is not valid')
            return render(request, 'register_admin.html')
        if not phone.isdigit():
            messages.success(request, 'Alphabetic characters not allowed in phone number')
            return render(request, 'register_admin.html')

        reg1 = Registration.objects.all()
        for i in reg1:
            if i.Email == email:
                messages.success(request, 'Admin already exists')
                return render(request, 'home.html')
        t = Registration()
        t.First_name = first_name
        t.Last_name = last_name
        t.Email = email
        t.Password = psw
        t.Registration_date = z
        t.About_website = 'Nil'
        t.User_role = admin
        t.Address = addr
        t.DOB = dob
        t.DOB = dob
        t.Gender = gender
        t.Phone = phone
        t.Qualification = 'Nil'
        t.Parent_phone = 'Nil'
        t.save()
        messages.success(request, 'You have successfully registered as admin')
        return render(request, 'home.html')
    else:
        return render(request, 'register_admin.html')

def register_st(request):
    mk = Course.objects.all()
    mn = []
    for i in mk:
        if i.Course not in mn:
            mn.append(i.Course)
    if request.method == 'POST':
        x = datetime.datetime.now()
        y = x.strftime("%Y-%m-%d")
        typ = request.POST.get('student')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if (not first_name.isalpha()) or (not last_name.isalpha()):
            messages.success(request, 'Non-alphabetic characters not allowed in name')
            return render(request, 'register.html')
        email = request.POST.get('email')
        addr = request.POST.get('addr')
        dob = request.POST.get('dob')
        dob1 = dob.split('-')
        aa = int(dob1[0])
        ab = int(dob1[1])
        ac = int(dob1[2])
        t = date.today()
        u = date(aa,ab,ac)
        v = relativedelta.relativedelta(t,u)
        v = v.years
        if v < 18:
            messages.success(request, 'Registration allowed for students above 18 years old')
            return render(request, 'register.html')
        d_c = request.POST.get('d_c')
        phone = request.POST.get('phone')
        p_phone = request.POST.get('p_phone')
        if len(phone) != 10 or len(p_phone) != 10:
            messages.success(request, 'Entered phone number is not valid')
            return render(request, 'register.html')
        if (not phone.isdigit()) or (not p_phone.isdigit()):
            messages.success(request, 'Alphabetic characters not allowed in phone number')
            return render(request, 'register.html')
        gender = request.POST.get('gender')
        course = request.POST.get('course')
        class1 = request.POST.get('class')
        sem = request.POST.get('sem')
        try:
            mgn = Registration.objects.all()
        except:
            messages.success(request, 'Please register')
            return render(request, 'home.html')
        for w in mgn:
            if w.Email == email and w.User_role == 'student':
                messages.success(request, 'You have already registered..Please login')
                return render(request, 'register.html')
        psw = request.POST.get('psw')
        reg = Registration()
        reg.First_name = first_name
        reg.Last_name = last_name
        reg.Email = email
        reg.Password = psw
        reg.Registration_date = y
        reg.About_website = 'Nil'
        reg.User_role = typ
        reg.Address = addr
        reg.DOB = dob
        reg.DOJ_course = d_c
        reg.Gender = gender
        reg.Phone = phone
        reg.Qualification = 'Nil'
        reg.Parent_phone = p_phone
        reg.Course = course
        reg.Class = class1
        reg.Semester = sem
        reg.save()
        messages.success(request, 'You have successfully registered')
        return render(request, 'home.html')
    else:
        return render(request, 'register.html',{'mn':mn})

def login(request):
    if request.method == 'POST':
        username = request.POST.get("email")
        password = request.POST.get("pword")
        if (Registration.objects.filter(Email=username, Password=password).exists()):
            logs = Registration.objects.filter(Email=username, Password=password)
            for value in logs:
                user_id = value.id
                usertype  = value.User_role
                if usertype == 'admin':
                    ss = Registration.objects.all()
                    request.session['logg'] = user_id
                    return render(request, "admin_home.html",{'ss':ss})

                elif usertype == 'student':
                    request.session['logg'] = user_id
                    return render(request, 'student_home.html')
                elif usertype == 'teacher':
                    request.session['logg'] = user_id
                    return render(request, 'teacher_home.html')
                else:
                    messages.success(request, 'Your access to the website may be blocked or under review. If you are already a member, please contact admin. If you are a new user, please wait till approval from admin.')
                    return render(request, 'login.html')
        else:
            messages.success(request, 'Email or password entered is incorrect')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def logout(request):
    local_tz = pytz.timezone("Asia/Calcutta")
    fg = Exam.objects.all()
    kk = []
    for i in fg:
        bb = i.Time_start
        cpp = bb.replace(tzinfo=pytz.utc).astimezone(local_tz)
        bbn = cpp.strftime("%Y-%B-%d %H:%M:%S %p")
        if bbn not in kk:
            kk.append('Student name - ')
            kk.append(i.Student_name)
            kk.append('; ')
            kk.append('Subject name - ')
            kk.append(i.Subject_name)
            kk.append('; ')
            kk.append('Start time - ')
            ft = i.Time_start
            ftt = ft.replace(tzinfo=pytz.utc).astimezone(local_tz)
            fty = ftt.strftime("%Y-%B-%d %H:%M:%S %p")
            kk.append(fty)
            kk.append('; ')
            kk.append('Stop time - ')
            fte = i.Time_stop
            ftee = fte.replace(tzinfo=pytz.utc).astimezone(local_tz)
            fty1 = ftee.strftime("%Y-%B-%d %H:%M:%S %p")
            kk.append(fty1)
            kk.append('mh')

    if 'logg' in request.session:
        del request.session['logg']
        return render(request, 'home.html',{'kk':kk})
    return render(request, 'home.html',{'kk':kk})

def update_pr_tr(request):
    bb = Registration.objects.get(id = request.session['logg'])
    if request.method == 'POST':
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')

        if (not f_name.isalpha()) or (not l_name.isalpha()):
            messages.success(request, 'Non-alphabetic characters not allowed in name')
            return render(request, 'update_pr_tr.html', {'bb': bb})

        email = request.POST.get('email')
        pasw = request.POST.get('psw')
        addr = request.POST.get('addr')
        dob = request.POST.get('dob')

        dob1 = dob.split('-')
        aa = int(dob1[0])
        ab = int(dob1[1])
        ac = int(dob1[2])
        t = date.today()
        u = date(aa, ab, ac)
        v = relativedelta.relativedelta(t, u)
        v = v.years
        if v < 18:
            messages.success(request, 'Age should be above 18 years. Please check DOB.')
            return render(request, 'update_pr_tr.html', {'bb': bb})

        gender = request.POST.get('gender')
        phone = request.POST.get('phone')

        if len(phone) != 10:
            messages.success(request, 'Entered phone number is not valid')
            return render(request, 'update_pr_tr.html', {'bb': bb})
        if not phone.isdigit():
            messages.success(request, 'Alphabetic characters not allowed in phone number')
            return render(request, 'update_pr_tr.html', {'bb': bb})

        qual = request.POST.get('qual')
        bb.First_name = f_name
        bb.Last_name = l_name
        bb.Email = email
        bb.Password = pasw
        bb.Address = addr
        bb.DOB = dob
        bb.Gender = gender
        bb.Phone = phone
        bb.Qualification = qual
        bb.save()
        messages.success(request, 'Updated successfully')
        return render(request, 'teacher_home.html')
    return render(request, 'update_pr_tr.html', {'bb': bb})

def sched_test(request):
    sew = Registration.objects.filter(User_role = 'student')
    return render(request,'sched_test.html',{'sew':sew})

def sched_test1(request):
    numbb = request.POST.get('numbb')
    request.session['subj_j'] = subj = request.POST.get('subj')
    nmbb = int(numbb)
    request.session['exam_start'] = dtt = request.POST.get('dtt')
    request.session['exam_stop'] = stt = request.POST.get('stt')

    dtt1 = dtt.split('T')
    dat = dtt1[0].split('-')
    tim = dtt1[1].split(':')
    y = int(dat[0])
    m = int(dat[1])
    d = int(dat[2])
    h = int(tim[0])
    mm = int(tim[1])

    stt1 = stt.split('T')
    dat1 = stt1[0].split('-')
    tim1 = stt1[1].split(':')
    y1 = int(dat1[0])
    m1 = int(dat1[1])
    d11 = int(dat1[2])
    h1 = int(tim1[0])
    mm1 = int(tim1[1])

    d1 = datetime.datetime(y, m, d, h, mm)
    d2 = datetime.datetime(y1, m1, d11, h1, mm1)
    d3 = datetime.datetime.now()
    if d3 >= d1 or d2 < d1 or d3 >= d1:
        messages.success(request, 'Please check entered date and time')
        sew = Registration.objects.filter(User_role='student')
        return render(request, 'sched_test.html', {'sew': sew})
    request.session['cc'] = nmbb
    k = request.POST.getlist('scd')
    if not k:
        messages.success(request, 'Please select student')
        sew = Registration.objects.filter(User_role='student')
        return render(request, 'sched_test.html', {'sew': sew})
    request.session['stu_for_test'] = k
    return render(request,'sched_test2.html')

def sched_test3(request):
    m = request.session['stu_for_test']
    ques = request.POST.get('ques')
    op1 = request.POST.get('op1')
    op2 = request.POST.get('op2')
    op3 = request.POST.get('op3')
    ans = request.POST.get('ans')
    c = request.session['cc']
    stz = Registration.objects.get(id = request.session['logg'])
    if c>0:
        for i in m:
            i = int(i)
            mnm = Registration.objects.get(id = i)
            fd = Exam()
            ty2 = mnm.First_name
            ty2 = str(ty2)
            mn2 = mnm.Last_name
            mn2 = str(mn2)
            fd.Student_name = ty2+' '+mn2
            fd.Student_email = mnm.Email
            ty = stz.First_name
            ty = str(ty)
            mn = stz.Last_name
            mn = str(mn)
            fd.Teacher_name = ty+' '+mn
            subje = request.session['subj_j']
            subje = str(subje)
            fd.Subject_name = subje
            fd.Option1 = op1
            fd.Option2 = op2
            fd.Option3 = op3
            fd.Correct_answer = ans
            fd.Question = ques

            drts = request.session['exam_start']
            drtd = drts.replace('T',' ')
            time_zone = pytz.timezone('Asia/Calcutta')
            drtd = datetime.datetime.strptime(drtd,"%Y-%m-%d %H:%M")
            fd.Time_start = time_zone.localize(drtd)

            drts1 = request.session['exam_stop']
            drtd1 = drts1.replace('T', ' ')
            time_zone = pytz.timezone('Asia/Calcutta')
            drtd1 = datetime.datetime.strptime(drtd1, "%Y-%m-%d %H:%M")
            fd.Time_stop = time_zone.localize(drtd1)

            dt = Registration.objects.get(id = request.session["logg"])
            fd.Exam_reg = dt
            fd.save()
        c -= 1
        request.session['cc'] = c
        if c == 0:
            messages.success(request, 'Exam scheduled successfully')
            return render(request, 'teacher_home.html')
        return render(request,'sched_test2.html')
    else:
        messages.success(request, 'Exam scheduled successfully')
        return render(request, 'teacher_home.html')

def delete_test(request):
    hh = Registration.objects.get(id = request.session['logg'])
    fg = Exam.objects.filter(Exam_reg = hh)
    return render(request, 'delete_test.html', {'fg': fg})

def delete_test1(request, id):
    Exam.objects.get(id = id).delete()
    hh = Registration.objects.get(id = request.session['logg'])
    fg = Exam.objects.filter(Exam_reg = hh)
    return render(request, 'delete_test.html', {'fg': fg})

def exam_result(request):
    hh = Registration.objects.get(id = request.session['logg'])
    g = str(hh.First_name)
    g1 = str(hh.Last_name)
    km = g+' '+g1
    gt = Exam_results.objects.filter(Teacher_name = km)
    return render(request,'exam_result.html',{'hh':hh,'gt':gt})

def delete_ex_re(request, id):
    Exam_results.objects.get(id=id).delete()
    hh = Registration.objects.get(id=request.session['logg'])
    g = str(hh.First_name)
    g1 = str(hh.Last_name)
    km = g+' '+g1
    gt = Exam_results.objects.filter(Teacher_name = km)
    return render(request, 'exam_result.html', {'hh': hh, 'gt': gt})

def sent_msg_teacher(request):
    p = Registration.objects.get(id = request.session['logg'])
    bb = Messages.objects.filter(To_email = p.Email)
    kk = Registration.objects.all()
    if request.method == 'POST':
        to_em = request.POST.get('to_em')
        ddp = str(to_em)
        gg = ddp.split()
        pnm = gg[0]
        first = gg[2]
        last = gg[3]
        msg_cont = request.POST.get('msg_cont')
        nm = Messages()
        nm.Category = p.User_role
        kkp = Registration.objects.get(id = request.session['logg'])
        nm.Name = first+' '+last
        nm.From_email = kkp.Email
        nm.To_email = pnm
        nm.Message_content = msg_cont
        nm.save()
        messages.success(request, 'Message sent successfully')
        return render(request, 'message1.html', {'bb': bb})
    return render(request,'sent_msg_teacher.html',{'kk':kk})

def ex_not(request):
    local_tz = pytz.timezone("Asia/Calcutta")
    hh = Registration.objects.get(id = request.session['logg'])
    fg = Exam.objects.filter(Student_email = hh.Email)
    kk = []
    for i in fg:
        bb = i.Time_start
        cpp = bb.replace(tzinfo=pytz.utc).astimezone(local_tz)
        bbn = cpp.strftime("%Y-%B-%d %H:%M:%S %p")
        if bbn not in kk:
            kk.append('Subject name')
            kk.append(i.Subject_name)
            kk.append('Start time')
            ft = i.Time_start
            ftt = ft.replace(tzinfo=pytz.utc).astimezone(local_tz)
            fty = ftt.strftime("%Y-%B-%d %H:%M:%S %p")
            kk.append(fty)
            kk.append('Stop time')
            fte = i.Time_stop
            ftee = fte.replace(tzinfo=pytz.utc).astimezone(local_tz)
            fty1 = ftee.strftime("%Y-%B-%d %H:%M:%S %p")
            kk.append(fty1)
    return render(request,'ex_not.html',{'kk':kk})

def start_test(request):
    local_tz = pytz.timezone("Asia/Calcutta")
    hh = Registration.objects.get(id = request.session['logg'])
    fg = Exam.objects.filter(Student_email = hh.Email)
    x = datetime.datetime.now()
    x = pytz.utc.localize(x)
    fgc = timezone.now()
    hj = []
    for i in fg:
        zz = i.Time_start
        nb = i.Time_stop
        nbn = nb.replace(tzinfo=pytz.utc).astimezone(local_tz)
        nbnn = nbn.strftime("%Y-%B-%d %I:%M:%S %p")
        if fgc>zz and fgc<nb:
            nb = Exam.objects.filter(Student_email = hh.Email, Time_start__lte = fgc, Time_stop__gte = fgc)
            for i in nb:
                if i.Lock == 'locked':
                    messages.success(request, 'You have already attended the exam')
                    return render(request, 'student_home.html')
            for i in nb:
                hj.append(i.Correct_answer)
                request.session['teec'] = i.Teacher_name
                request.session['ssub'] = i.Subject_name
                request.session['student'] = i.Student_name
                request.session['student_ema'] = i.Student_email
                gg = str(nbnn)
            request.session['exam_id'] = hj
            return render(request,'start_test.html',{'nb':nb,'gg':gg})
    messages.success(request, 'No exam is scheduled now')
    return render(request, 'student_home.html')

def save_exam(request):
    end_time = request.POST.get('end_time')
    endd = end_time[0:20]
    edr = datetime.datetime.strptime(endd, '%Y-%B-%d %H:%M:%S')
    b = datetime.datetime.now()
    bb = b.strftime('%Y-%B-%d %H:%M:%S')
    edr1 = datetime.datetime.strptime(bb, '%Y-%B-%d %H:%M:%S')
    if edr < edr1:
        messages.success(request, 'You have timed out')
        return render(request, 'student_home.html')
    correct_answers = request.POST.getlist('exx3')
    answers = request.POST.getlist('exx')
    if len(correct_answers) != len(answers):
        messages.success(request, 'Your exam attempt failed due to selecting multiple answers')
        return render(request,'student_home.html')
    count = 0
    count1 = 0
    for i in correct_answers:
        count1 += 1
    for i,j in zip(correct_answers,answers):
        if i == j:
            count += 1
    hh = Registration.objects.get(id = request.session['logg'])
    fg = Exam.objects.filter(Student_email = hh.Email)
    x = datetime.datetime.now()
    x = pytz.utc.localize(x)
    fgc = timezone.now()
    for i in fg:
        zz = i.Time_start
        nb = i.Time_stop
        if fgc > zz and fgc < nb:
            nb = Exam.objects.filter(Student_email = hh.Email, Time_start__lte = fgc, Time_stop__gte = fgc)
            for i in nb:
                i.Lock = 'locked'
                i.save()
    ddd = Exam_results()
    ddd.Student_name = request.session['student']
    ddd.Student_email = request.session['student_ema']
    ddd.Teacher_name = request.session['teec']
    ddd.Subject_name = request.session['ssub']
    ddd.Total_marks = count1
    ddd.Acquired_marks = count
    avg = 100 * float(count)/float(count1)
    if avg >= 80:
        ddd.Grade = 'A'
    elif avg < 80 and avg >= 50 :
        ddd.Grade = 'B'
    elif avg < 50 and avg >= 30:
        ddd.Grade = 'C'
    elif avg < 50 and avg >= 30:
        ddd.Grade = 'C'
    else:
        ddd.Grade = 'Failed'
    ddd.Time_stop = b
    ddd.Exam_res_reg = hh
    ddd.save()
    messages.success(request, 'You have successfully finished your exam')
    return render(request, 'student_home.html')

def exam_result1(request):
    gt = Exam_results.objects.all()
    hh = Registration.objects.get(id = request.session['logg'])
    return render(request,'exam_result1.html',{'hh':hh,'gt':gt})

def ch_p11(request):
    th = Registration.objects.get(id = request.session['logg'])
    if request.method == 'POST':
        new_pass = request.POST.get('pssw')
        old_pass = request.POST.get('pssw_old')
        email = request.POST.get('em')
        cate = request.POST.get('usr')
        nam = request.POST.get('nam')
        g = Requests()
        g.Name = nam
        g.Email = email
        g.User_category = cate
        g.Old_password = old_pass
        g.New_password = new_pass
        g.Req_reg = th
        g.save()
        messages.success(request, 'Please wait for your password approval.. Continue to use old password')
        return render(request, 'Teacher_home.html')
    return render(request, 'change_password1.html', {'th': th})

def TakeImages(request):
    if request.method == 'POST':
        nam = request.POST.get('name')
        em = request.POST.get('em')
        serial = 0
        try:
            exists = Registration.objects.get(First_name = nam, Email = em)
            if exists:
                reader1 = Registration.objects.all()
                for k in reader1:
                    serial = serial + 1
                serial = (serial // 2)
        except:
            messages.success(request, 'Email or name entered is incorrect')
            return render(request, 'face_template.html')
        name = str(nam)
        if ((name.isalpha()) or (' ' in name)):
            cam = cv2.VideoCapture(0)
            harcascadePath = "C:\\Users\\user\\Desktop\\students\\pyt_stud_rinchu\\face_rec\\face\\haarcascade_frontalface_default.xml"
            detector = cv2.CascadeClassifier(harcascadePath)
            sampleNum = 0
            while (True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    # incrementing sample number
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder TrainingImage
                    km = Registration.objects.get(First_name = name, Email = em)
                    serial = km.id
                    cv2.imwrite("C:\\Users\\user\\Desktop\\students\\pyt_stud_rinchu\\face_rec\\face\\TrainingImage\ " + name + "." + str(serial) + "." + str(km.Email) + '.' + str(sampleNum) + ".jpg",
                                gray[y:y + h, x:x + w])
                    # display the frame
                    cv2.imshow('Taking Images', img)
                # wait for 100 miliseconds
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                # break if the sample number is morethan 100
                elif sampleNum > 100:
                    break
            cam.release()
            cv2.destroyAllWindows()

            recognizer = cv2.face_LBPHFaceRecognizer.create()
            faces, ID = getImagesAndLabels("C:\\Users\\user\\Desktop\\students\\pyt_stud_rinchu\\face_rec\\face\\TrainingImage")
            recognizer.train(faces, np.array(ID))
            recognizer.save("C:\\Users\\user\\Desktop\\students\\pyt_stud_rinchu\\face_rec\\face\\TrainingImageLabel\\Trainner.yml")


            messages.success(request, 'Images taken')
            return render(request, 'face_template.html')
        else:
            if (name.isalpha() == False):
                messages.success(request, 'Enter correct name')
                return render(request,'face_template.html')


def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids


def save_pass():
    try:
        key = Password.objects.get()
    except:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = Password()
            tf.password = new_pass
            tf.save()
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    op = (old.get())
    newp = (new.get())
    nnewp = (nnew.get())
    if (op == key):
        if(newp == nnewp):
            txf = Password()
            txf.password = newp
            txf.save()
        else:
            mess._show(title='Error', message='Confirm new password again!!!')
            return
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')
        return
    mess._show(title='Password Changed', message='Password changed successfully!!')
    master.destroy()

def TrackImages(request):
    #check_haarcascadefile()
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    try:
        recognizer.read("C:\\Users\\user\\Desktop\\students\\pyt_stud_rinchu\\face_rec\\face\\TrainingImageLabel\\Trainner.yml")
    except:
        messages.success(request, 'Person cannot be identified. Please take images.')
        return render(request, 'face_template.html')
    harcascadePath = "C:\\Users\\user\\Desktop\\students\\pyt_stud_rinchu\\face_rec\\face\\haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            serial = int(serial)
            if (conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M')
                try:
                    df = Registration.objects.get(id = serial)
                except:
                    messages.success(request, 'Your ID has been updated. Please take images')
                    return render(request, 'face_template.html')
                kmk = Attendance()
                ghy = df.First_name
                ghy = str(ghy)
                khy = df.Last_name
                khy = str(khy)
                kmk.Name = ghy+' '+khy
                kmk.Email = df.Email
                kmk.Date = str(date)
                kmk.Time = str(timeStamp)
                bb = ghy+' '+khy
                cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
                if (cv2.waitKey(1) == ord('q')):
                    kmk.save()
                    cam.release()
                    cv2.destroyAllWindows()
                    messages.success(request, 'Attendance taken')
                    return render(request, 'face_template.html')
            else:
                Id = 'Unknown'
                bb = str(Id)
                cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
        cv2.imshow('Taking Attendance', im)
        if (cv2.waitKey(1) == ord('q')):
            break
    """ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = Attendance.objects.filter(Date = date)
    if exists:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(attendance)
        csvFile1.close()
    else:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            writer.writerow(attendance)
        csvFile1.close()"""
    cam.release()
    cv2.destroyAllWindows()
    messages.success(request, 'Failed to take attendance. Please be available in front of camera.')
    return render(request, 'face_template.html')

def contact(request):
    local_tz = pytz.timezone("Asia/Calcutta")
    fg = Exam.objects.all()
    kk = []
    for i in fg:
        bb = i.Time_start
        cpp = bb.replace(tzinfo=pytz.utc).astimezone(local_tz)
        bbn = cpp.strftime("%Y-%B-%d %H:%M:%S %p")
        if bbn not in kk:
            kk.append('Student name - ')
            kk.append(i.Student_name)
            kk.append('; ')
            kk.append('Subject name - ')
            kk.append(i.Subject_name)
            kk.append('; ')
            kk.append('Start time - ')
            ft = i.Time_start
            ftt = ft.replace(tzinfo=pytz.utc).astimezone(local_tz)
            fty = ftt.strftime("%Y-%B-%d %H:%M:%S %p")
            kk.append(fty)
            kk.append('; ')
            kk.append('Stop time - ')
            fte = i.Time_stop
            ftee = fte.replace(tzinfo=pytz.utc).astimezone(local_tz)
            fty1 = ftee.strftime("%Y-%B-%d %H:%M:%S %p")
            kk.append(fty1)
            kk.append('mh')

    m = Registration.objects.get(User_role = 'admin')
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        t_a = request.POST.get('t_a')
        g = Messages()
        g.Category = 'guest'
        g.Name = name
        g.From_email = email
        g.To_email = m.Email
        g.Message_content = t_a
        g.save()
        messages.success(request, 'Message sent successfully')
        return render(request,'home.html',{'kk':kk})
    return render(request,'contact.html')

def atten(request):
    mb = Registration.objects.all()
    cou = []
    cla = []
    sem = []
    for w in mb:
        if w.Course not in cou and w.Course != '':
            cou.append(w.Course)
        if w.Class not in cla and w.Class != '' and w.Class is not None:
            cla.append(w.Class)
        if w.Semester not in sem and w.Semester != '' and w.Semester is not None:
            sem.append(w.Semester)
    if request.method == 'POST':
        course = request.POST.get('course')
        class1 = request.POST.get('class')
        class1 = int(class1)
        sem = request.POST.get('sem')
        sem = int(sem)
        dat = request.POST.get('dat')
        month = request.POST.get('month')
        week = request.POST.get('week')
        if dat == '' and month == '' and week == '':
            mb = Registration.objects.all()
            cou = []
            cla = []
            sem = []
            for w in mb:
                if w.Course not in cou and w.Course != '':
                    cou.append(w.Course)
                if w.Class not in cla and w.Class != '' and w.Class is not None:
                    cla.append(w.Class)
                if w.Semester not in sem and w.Semester != '' and w.Semester is not None:
                    sem.append(w.Semester)
            messages.success(request, 'Please select daily/weekly/monthly attendance')
            return render(request, 'atten_adm.html', {'cou': cou, 'cla': cla, 'sem': sem})

        elif dat != '' and month == '' and week == '':
            dat = request.POST.get('dat')
            request.session['datte'] = dat
            try:
                k = Registration.objects.filter(Class = class1, Course = course, Semester = sem)
                m = Attendance.objects.filter(Date=dat)
                gb = []
                for b in m:
                    for c in k:
                        if (b.Email == c.Email) and (b.Email not in gb):
                            gb.append(b.Email)
                request.session['atten_email'] = gb
                return render(request, 'atten5.html', {'m': m,'gb':gb})
            except:
                mb = Registration.objects.all()
                cou = []
                cla = []
                sem = []
                for w in mb:
                    if w.Course not in cou and w.Course != '':
                        cou.append(w.Course)
                    if w.Class not in cla and w.Class != '' and w.Class is not None:
                        cla.append(w.Class)
                    if w.Semester not in sem and w.Semester != '' and w.Semester is not None:
                        sem.append(w.Semester)
                messages.success(request, 'Attendance not available')
                return render(request, 'atten_adm.html', {'cou': cou, 'cla': cla, 'sem': sem})

        elif dat == '' and month != '' and week == '':
            month = request.POST.get('month')
            try:
                k = Registration.objects.filter(Class=class1, Course=course, Semester=sem)
                mm = Attendance.objects.all()
                ms = []
                m1 = []
                m2 = []
                m3 = []
                m5 = []
                for i in mm:
                    t = str(i.Date)
                    t = t[0:7]
                    if t == month:
                        ms.append(i.Name)
                        m1.append(i.Email)
                        m2.append(i.Date)
                        m3.append(i.Time)
                        m5.append(i.id)
                m4 = zip(ms, m1, m2, m3, m5)
                request.session['datte'] = ms
                request.session['datte1'] = m1
                request.session['datte2'] = m2
                request.session['datte3'] = m3
                request.session['datte4'] = m5
                gb = []
                for c in k:
                    if c.Email not in gb:
                        gb.append(c.Email)
                request.session['atten_email'] = gb
                return render(request, 'atten5.html', {'m4': m4, 'gb': gb})
            except:
                mb = Registration.objects.all()
                cou = []
                cla = []
                sem = []
                for w in mb:
                    if w.Course not in cou and w.Course != '':
                        cou.append(w.Course)
                    if w.Class not in cla and w.Class != '' and w.Class is not None:
                        cla.append(w.Class)
                    if w.Semester not in sem and w.Semester != '' and w.Semester is not None:
                        sem.append(w.Semester)
                messages.success(request, 'Attendance not available')
                return render(request, 'atten_adm.html', {'cou': cou, 'cla': cla, 'sem': sem})

        elif dat == '' and month == '' and week != '':
            week = request.POST.get('week')

            r = datetime.datetime.strptime(week + '-1', "%Y-W%W-%w")
            r = str(r)
            r = r[0:10]
            r = r.split('-')
            a = r[0]
            a = int(a)
            b = r[1]
            b = int(b)
            c = r[2]
            c = int(c)
            base = datetime.datetime(a, b, c)
            days = datetime.timedelta(7)
            base = base - days
            mk = []
            for x in range(0, 6):
                y = base + datetime.timedelta(days=x)
                y = str(y)
                y = y[0:10]
                mk.append(y)
            request.session['datte'] = mk
            try:
                k = Registration.objects.filter(Class=class1, Course=course, Semester=sem)
                m = Attendance.objects.filter(Q(Date = mk[0]) | Q(Date = mk[1]) | Q(Date = mk[2]) | Q(Date = mk[3]) | Q(Date = mk[4]) | Q(Date = mk[5]))
                gb = []
                for b in m:
                    for c in k:
                        if (b.Email == c.Email) and (b.Email not in gb):
                            gb.append(b.Email)
                request.session['atten_email'] = gb
                return render(request, 'atten5.html', {'m': m, 'gb': gb})
            except:
                mb = Registration.objects.all()
                cou = []
                cla = []
                sem = []
                for w in mb:
                    if w.Course not in cou and w.Course != '':
                        cou.append(w.Course)
                    if w.Class not in cla and w.Class != '' and w.Class is not None:
                        cla.append(w.Class)
                    if w.Semester not in sem and w.Semester != '' and w.Semester is not None:
                        sem.append(w.Semester)
                messages.success(request, 'Attendance not available')
                return render(request, 'atten_adm.html', {'cou': cou, 'cla': cla, 'sem': sem})
        else:
            mb = Registration.objects.all()
            cou = []
            cla = []
            sem = []
            for w in mb:
                if w.Course not in cou and w.Course != '':
                    cou.append(w.Course)
                if w.Class not in cla and w.Class != '' and w.Class is not None:
                    cla.append(w.Class)
                if w.Semester not in sem and w.Semester != '' and w.Semester is not None:
                    sem.append(w.Semester)
            messages.success(request, 'Please select only one option (daily/weekly/monthly)')
            return render(request, 'atten_adm.html', {'cou': cou, 'cla': cla, 'sem': sem})
    return render(request,'atten_adm.html',{'cou':cou,'cla':cla,'sem':sem})

def atten1(request):
    mb = Registration.objects.all()
    mkb = Registration.objects.filter(User_role = 'student')
    cou = []
    cla = []
    sem = []
    for w in mb:
        if w.Course not in cou and w.Course != '':
            cou.append(w.Course)
        if w.Class not in cla and w.Class != '' and w.Class is not None:
            cla.append(w.Class)
        if w.Semester not in sem and w.Semester != '' and w.Semester is not None:
            sem.append(w.Semester)
    stu = []
    cse = []
    clm = []
    smm = []
    idp = []
    for wt in mkb:
        ddy = wt.First_name
        ddy = str(ddy)
        dtk = wt.Last_name
        dtt = str(dtk)
        mte = ddy + ' ' + dtt
        if mte not in stu and mte != '' and mte is not None:
            stu.append(mte)
            cse.append(wt.Course)
            clm.append(wt.Class)
            smm.append(wt.Semester)
            idp.append(wt.id)
    stb = zip(stu,cse,clm,smm,idp)
    if request.method == 'POST':
        student = request.POST.get('student')
        course = request.POST.get('course')
        class1 = request.POST.get('class')
        class1 = int(class1)
        semk = request.POST.get('sem')
        semk = int(semk)
        if student != 'Nil' and (course != 'Nil' or class1 != 0 or semk != 0):
            messages.success(request, "Please select 'student attendance' OR 'Course wise attendance'")
            return render(request, 'atten_tea.html', {'cou': cou, 'cla': cla, 'sem': sem,'stb':stb})
        if student != 'Nil':
            student = int(student)
            mss = Registration.objects.get(id = student)
            course = mss.Course
            class1 = mss.Class
            class1 = int(class1)
            sem = mss.Semester
            sem = int(sem)
        else:
            course = request.POST.get('course')
            class1 = request.POST.get('class')
            class1 = int(class1)
            sem = request.POST.get('sem')
            sem = int(sem)
        dat = request.POST.get('dat')
        month = request.POST.get('month')
        week = request.POST.get('week')
        time1 = request.POST.get('time1')
        time2 = request.POST.get('time2')
        hhour = request.POST.get('hhour')

        if ( ((time1 == '' and time2 == '') or (time1 == '' or time2 == '')) and (hhour == '0') ) or ( ((time1 != '' and time2 != '') or (time1 != '' or time2 != '')) and (hhour != '0') ):
            cou = []
            cla = []
            sem = []
            for w in mb:
                if w.Course not in cou and w.Course != '':
                    cou.append(w.Course)
                if w.Class not in cla and w.Class != '' and w.Class is not None:
                    cla.append(w.Class)
                if w.Semester not in sem and w.Semester != '' and w.Semester is not None:
                    sem.append(w.Semester)
            messages.success(request, 'Please select start and stop time OR hour. Do not select both.')
            return render(request, 'atten_tea.html', {'cou': cou, 'cla': cla, 'sem': sem,'stb':stb})

        if hhour != '0':
            if hhour == '1':
                time1 = '08:30'
                time2 = '09:30'
            if hhour == '2':
                time1 = '09:30'
                time2 = '10:30'
            if hhour == '3':
                time1 = '10:30'
                time2 = '11:30'
            if hhour == '4':
                time1 = '11:30'
                time2 = '12:30'
            if hhour == '5':
                time1 = '13:30'
                time2 = '14:30'
            if hhour == '6':
                time1 = '14:30'
                time2 = '15:30'

        if dat == '' and month == '' and week == '':
            mb = Registration.objects.all()
            cou = []
            cla = []
            sem = []
            for w in mb:
                if w.Course not in cou and w.Course != '':
                    cou.append(w.Course)
                if w.Class not in cla and w.Class != '' and w.Class is not None:
                    cla.append(w.Class)
                if w.Semester not in sem and w.Semester != '' and w.Semester is not None:
                    sem.append(w.Semester)
            messages.success(request, 'Please select daily/weekly/monthly attendance')
            return render(request, 'atten_tea.html', {'cou': cou, 'cla': cla, 'sem': sem, 'stb':stb})

        elif dat != '' and month == '' and week == '':
            dat = request.POST.get('dat')
            request.session['datte'] = dat

            try:
                if student == 'Nil':
                    k = Registration.objects.filter(Class = class1, Course = course, Semester = sem)
                    m = Attendance.objects.filter(Date=dat)
                else:
                    sdm = int(student)
                    k = Registration.objects.filter(id = sdm)
                    for e in k:
                        m = Attendance.objects.filter(Date=dat, Email=e.Email)
                gb1 = []
                timm = []
                dass = []
                gm8 = []
                for q in m:
                    drp = '%H:%M'
                    time4 = datetime.datetime.strptime(time1, drp)
                    time5 = datetime.datetime.strptime(time2, drp)
                    tim3 = str(q.Time)
                    timm3 = str(q.Time)
                    dass1 = str(q.Date)
                    tim3 = datetime.datetime.strptime(tim3, drp)
                    if tim3 >= time4 and tim3 <= time5:
                        gm8.append(q.Email)
                    if (tim3 >= time4 and tim3 <= time5):
                        gb1.append(q.Email)
                        timm.append(timm3)
                        dass.append(dass1)
                gb22 = zip(gb1,timm, dass)
                emp = []
                timp = []
                datp = []
                namp = []
                for o in k:
                    gb33 = zip(gb1, timm, dass)
                    for d,b,g in gb33:
                        if d == o.Email:
                            emp.append(d)
                            timp.append(b)
                            datp.append(g)
                            fn = o.First_name
                            fn = str(fn)
                            sn = o.Last_name
                            sn = str(sn)
                            snn = fn+' '+sn
                            namp.append(snn)
                m = zip(namp,emp,datp,timp)
                gb2 = []
                for s in k:
                    if s.Email not in gb2:
                        gb2.append(s.Email)
                gb1 = set(gb1)
                gb2 = set(gb2)
                couns = 0
                couns1 = 0
                for i in gb1:
                    if i in gb2:
                        couns += 1
                for k in gb2:
                    couns1 += 1

                perc = couns / couns1 * 100
                perc = round(perc, 2)

                counp = 0
                for p in gm8:
                    counp += 1
                perce = counp/1 * 100
                perce = round(perce,2)

                return render(request, 'atten6.html', {'m': m,'dat':dat,'perc':perc,'perce':perce,'stm':student,'class1':class1,'course':course,'sem':sem})
            except:
                mb = Registration.objects.all()
                cou = []
                cla = []
                sem = []
                for w in mb:
                    if w.Course not in cou and w.Course != '':
                        cou.append(w.Course)
                    if w.Class not in cla and w.Class != '' and w.Class is not None:
                        cla.append(w.Class)
                    if w.Semester not in sem and w.Semester != '' and w.Semester is not None:
                        sem.append(w.Semester)
                messages.success(request, 'Attendance not available')
                return render(request, 'atten_tea.html', {'cou': cou, 'cla': cla, 'sem': sem, 'stb':stb})

        elif dat == '' and month != '' and week == '':

            month = request.POST.get('month')
            try:
                mon = month.split('-')
                year = mon[0]
                year = int(year)
                montt = mon[1]
                montt = int(montt)
                num_days = calendar.monthrange(year, montt)
                numm = num_days[1]
                numm = int(numm)
                dayy = []
                yeer = []
                montp = []
                for day in range(1, numm + 1):
                    day = str(day)
                    year = str(year)
                    montt = str(montt)
                    if len(day) == 1:
                        dayy.append('0'+day)
                    else:
                        dayy.append(day)
                    yeer.append(year)
                    if len(montt) == 1:
                        montp.append('0'+montt)
                    else:
                        montp.append(montt)
                ghr = zip(yeer, montp, dayy)
                ghr1 = []
                for a, b, c in ghr:
                    d = str(a) + '-' + str(b) + '-' + str(c)
                    ghr1.append(d)
                dailyy = []
                for w in ghr1:

                    if student == 'Nil':
                        km = Registration.objects.filter(Class=class1, Course=course, Semester=sem)
                        kj = Attendance.objects.filter(Date=w)
                    else:
                        sdm = int(student)
                        km = Registration.objects.filter(id=sdm)
                        for e in km:
                            kj = Attendance.objects.filter(Date=w, Email=e.Email)

                    khg = []
                    for u in kj:
                        for s in km:
                            if u.Email == s.Email and u.Email not in khg:
                                drp = '%H:%M'
                                time4 = datetime.datetime.strptime(time1, drp)
                                time5 = datetime.datetime.strptime(time2, drp)
                                tim3 = str(u.Time)
                                tim3 = datetime.datetime.strptime(tim3, drp)
                                if tim3 >= time4 and tim3 <= time5:
                                    khg.append(u.Email)
                    khg1 = []
                    for uu in km:
                        if uu.Email not in khg1:
                            khg1.append(uu.Email)
                    dailyy1 = len(khg)/len(khg1) * 100
                    dailyy.append(dailyy1)
                tot = 0
                for we in range(0,len(dailyy)):
                    tot += dailyy[we]
                percc = tot/len(dailyy)
                perc = round(percc,2)
                perce = round(percc, 2)

                k = Registration.objects.filter(Class=class1, Course=course, Semester=sem)
                mm = Attendance.objects.all()

                gb = []
                for c in k:
                    if c.Email not in gb:
                        gb.append(c.Email)
                ms = []
                m1 = []
                m2 = []
                m3 = []
                m5 = []
                for i in mm:
                    t = str(i.Date)
                    t = t[0:7]
                    if t == month:
                        drp = '%H:%M'
                        time4 = datetime.datetime.strptime(time1, drp)
                        time5 = datetime.datetime.strptime(time2, drp)
                        tim3 = str(i.Time)
                        tim3 = datetime.datetime.strptime(tim3, drp)
                        if tim3 >= time4 and tim3 <= time5:
                            for pk in km:
                                if pk.Email == i.Email:
                                    ms.append(i.Name)
                                    m1.append(i.Email)
                                    m2.append(i.Date)
                                    m3.append(i.Time)
                                    m5.append(i.id)

                m4 = zip(ms, m1, m2, m3, m5)

                request.session['datte'] = ms
                request.session['datte1'] = m1
                request.session['datte2'] = m2
                request.session['datte3'] = m3
                request.session['datte4'] = m5
                request.session['atten_email'] = gb
                return render(request, 'atten6.html', {'m4': m4, 'perc':perc, 'perce':perce, 'stm':student})
            except:
                mb = Registration.objects.all()
                cou = []
                cla = []
                sem = []
                for w in mb:
                    if w.Course not in cou and w.Course != '':
                        cou.append(w.Course)
                    if w.Class not in cla and w.Class != '' and w.Class is not None:
                        cla.append(w.Class)
                    if w.Semester not in sem and w.Semester != '' and w.Semester is not None:
                        sem.append(w.Semester)
                messages.success(request, 'Attendance not available')
                return render(request, 'atten_tea.html', {'cou': cou, 'cla': cla, 'sem': sem, 'stb':stb})

        elif dat == '' and month == '' and week != '':
            week = request.POST.get('week')
            r = datetime.datetime.strptime(week + '-1', "%Y-W%W-%w")
            r = str(r)
            r = r[0:10]
            r = r.split('-')
            a = r[0]
            a = int(a)
            b = r[1]
            b = int(b)
            c = r[2]
            c = int(c)
            base = datetime.datetime(a, b, c)
            days = datetime.timedelta(7)
            base = base - days
            mk = []
            for x in range(0, 6):
                y = base + datetime.timedelta(days=x)
                y = str(y)
                y = y[0:10]
                mk.append(y)
            request.session['datte'] = mk

            dailyy = []
            for w in mk:

                if student == 'Nil':
                    km = Registration.objects.filter(Class=class1, Course=course, Semester=sem)
                    kj = Attendance.objects.filter(Date=w)
                else:
                    sdm = int(student)
                    km = Registration.objects.filter(id=sdm)
                    for e in km:
                        kj = Attendance.objects.filter(Date=w, Email=e.Email)

                khg = []
                for u in kj:
                    for s in km:
                        if u.Email == s.Email and u.Email not in khg:
                            drp = '%H:%M'
                            time4 = datetime.datetime.strptime(time1, drp)
                            time5 = datetime.datetime.strptime(time2, drp)
                            tim3 = str(u.Time)
                            tim3 = datetime.datetime.strptime(tim3, drp)
                            if tim3 >= time4 and tim3 <= time5:
                                khg.append(u.Email)
                khg1 = []
                for uu in km:
                    if uu.Email not in khg1:
                        khg1.append(uu.Email)
                dailyy1 = len(khg) / len(khg1) * 100
                dailyy.append(dailyy1)
            tot = 0
            for we in range(0, len(dailyy)):
                tot += dailyy[we]
            percc = tot / len(dailyy)
            perc = round(percc, 2)
            perce = round(percc, 2)


            try:
                k = Registration.objects.filter(Class = class1, Course = course, Semester = sem)
                m = Attendance.objects.filter(Q(Date = mk[0]) | Q(Date = mk[1]) | Q(Date = mk[2]) | Q(Date = mk[3]) | Q(Date = mk[4]) | Q(Date = mk[5]))
                nam = []
                em = []
                dat = []
                tim = []
                for b in m:
                    for c in k:
                        if b.Email == c.Email:
                            drp = '%H:%M'
                            time4 = datetime.datetime.strptime(time1, drp)
                            time5 = datetime.datetime.strptime(time2, drp)
                            tim3 = str(b.Time)
                            tim3 = datetime.datetime.strptime(tim3, drp)
                            if tim3 >= time4 and tim3 <= time5:
                                for ms in km:
                                    if ms.Email == b.Email:
                                        dd = c.First_name
                                        dd = str(dd)
                                        dtp = c.Last_name
                                        dtp = str(dtp)
                                        mtp = dd + ' ' + dtp
                                        nam.append(mtp)
                                        em.append(b.Email)
                                        dat.append(b.Date)
                                        tim.append(b.Time)
                m5 = zip(nam,em,dat,tim)
                return render(request, 'atten6.html', {'m5': m5,'perc':perc,'perce':perce})
            except:
                mb = Registration.objects.all()
                cou = []
                cla = []
                sem = []
                for w in mb:
                    if w.Course not in cou and w.Course != '':
                        cou.append(w.Course)
                    if w.Class not in cla and w.Class != '' and w.Class is not None:
                        cla.append(w.Class)
                    if w.Semester not in sem and w.Semester != '' and w.Semester is not None:
                        sem.append(w.Semester)
                messages.success(request, 'Attendance not available')
                return render(request, 'atten_tea.html', {'cou': cou, 'cla': cla, 'sem': sem, 'stb':stb})
        else:
            mb = Registration.objects.all()
            cou = []
            cla = []
            sem = []
            for w in mb:
                if w.Course not in cou and w.Course != '':
                    cou.append(w.Course)
                if w.Class not in cla and w.Class != '' and w.Class is not None:
                    cla.append(w.Class)
                if w.Semester not in sem and w.Semester != '' and w.Semester is not None:
                    sem.append(w.Semester)
            messages.success(request, 'Please select only one option (daily/weekly/monthly)')
            return render(request, 'atten_tea.html', {'cou': cou, 'cla': cla, 'sem': sem, 'stb':stb})
    return render(request,'atten_tea.html',{'cou':cou,'cla':cla,'sem':sem,'stb':stb})

def absent1(request):
    mb = Registration.objects.all()
    mkbt = Registration.objects.filter(User_role='student')
    cou = []
    cla = []
    sem = []
    for w in mb:
        if w.Course not in cou and w.Course != '':
            cou.append(w.Course)
        if w.Class not in cla and w.Class != '' and w.Class is not None:
            cla.append(w.Class)
        if w.Semester not in sem and w.Semester != '' and w.Semester is not None:
            sem.append(w.Semester)

    stu = []
    cse = []
    clm = []
    smm = []
    idp = []
    for wt in mkbt:
        ddy = wt.First_name
        ddy = str(ddy)
        dtk = wt.Last_name
        dtt = str(dtk)
        mte = ddy + ' ' + dtt
        if mte not in stu and mte != '' and mte is not None:
            stu.append(mte)
            cse.append(wt.Course)
            clm.append(wt.Class)
            smm.append(wt.Semester)
            idp.append(wt.id)
    stb = zip(stu, cse, clm, smm, idp)

    if request.method == 'POST':

        student = request.POST.get('student')
        course = request.POST.get('course')
        class1 = request.POST.get('class')
        class1 = int(class1)
        semk = request.POST.get('sem')
        semk = int(semk)
        if student != 'Nil' and (course != 'Nil' or class1 != 0 or semk != 0):
            messages.success(request, "Please select 'student wise absentees' OR 'Course wise absentees'")
            return render(request, 'atten_tea1.html', {'cou': cou, 'cla': cla, 'sem': sem, 'stb': stb})
        if student != 'Nil':
            student = int(student)
            mss = Registration.objects.get(id=student)
            course = mss.Course
            class1 = mss.Class
            class1 = int(class1)
            sem = mss.Semester
            sem = int(sem)
        else:
            course = request.POST.get('course')
            class1 = request.POST.get('class')
            class1 = int(class1)
            sem = request.POST.get('sem')
            sem = int(sem)

        dat = request.POST.get('dat')
        month = request.POST.get('month')
        week = request.POST.get('week')
        time1 = request.POST.get('time1')
        time2 = request.POST.get('time2')
        hhour = request.POST.get('hhour')

        if (((time1 == '' and time2 == '') or (time1 == '' or time2 == '')) and (hhour == '0')) or (
                ((time1 != '' and time2 != '') or (time1 != '' or time2 != '')) and (hhour != '0')):
            cou = []
            cla = []
            sem = []
            for w in mb:
                if w.Course not in cou and w.Course != '':
                    cou.append(w.Course)
                if w.Class not in cla and w.Class != '' and w.Class is not None:
                    cla.append(w.Class)
                if w.Semester not in sem and w.Semester != '' and w.Semester is not None:
                    sem.append(w.Semester)
            messages.success(request, 'Please select start and stop time OR hour. Do not select both.')
            return render(request, 'atten_tea1.html', {'cou': cou, 'cla': cla, 'sem': sem, 'stb':stb})

        if hhour != '0':
            if hhour == '1':
                time1 = '08:30'
                time2 = '09:30'
            if hhour == '2':
                time1 = '09:30'
                time2 = '10:30'
            if hhour == '3':
                time1 = '10:30'
                time2 = '11:30'
            if hhour == '4':
                time1 = '11:30'
                time2 = '12:30'
            if hhour == '5':
                time1 = '13:30'
                time2 = '14:30'
            if hhour == '6':
                time1 = '14:30'
                time2 = '15:30'




        if dat == '' and month == '' and week == '':
            mb = Registration.objects.all()
            cou = []
            cla = []
            sem = []
            for w in mb:
                if w.Course not in cou and w.Course != '':
                    cou.append(w.Course)
                if w.Class not in cla and w.Class != '' and w.Class is not None:
                    cla.append(w.Class)
                if w.Semester not in sem and w.Semester != '' and w.Semester is not None:
                    sem.append(w.Semester)
            messages.success(request, 'Please select daily/weekly/monthly absentees')
            return render(request, 'atten_tea1.html', {'cou': cou, 'cla': cla, 'sem': sem, 'stb':stb})

        elif dat != '' and month == '' and week == '':
            dat = request.POST.get('dat')
            request.session['datte'] = dat
            try:
                if student == 'Nil':
                    k = Registration.objects.filter(Class=class1, Course=course, Semester=sem)
                    m = Attendance.objects.filter(Date=dat)
                else:
                    sdm = int(student)
                    k = Registration.objects.filter(id=sdm)
                    for e in k:
                        m = Attendance.objects.filter(Date=dat, Email=e.Email)

                gb1 = []
                gm8 = []
                for q in m:
                    drp = '%H:%M'
                    time4 = datetime.datetime.strptime(time1, drp)
                    time5 = datetime.datetime.strptime(time2, drp)
                    tim3 = str(q.Time)
                    tim3 = datetime.datetime.strptime(tim3, drp)
                    if (tim3 >= time4) and (tim3 <= time5):
                        gm8.append(q.Email)
                    if (tim3 >= time4 and tim3 <= time5):
                        gb1.append(q.Email)

                gb2 = []
                for s in k:
                    if s.Email not in gb2:
                        gb2.append(s.Email)
                gb1 = set(gb1)
                gb2 = set(gb2)
                couns = 0
                couns1 = 0
                for i in gb2:
                    if i not in gb1:
                        couns += 1
                for kk in gb2:
                    couns1 += 1

                perc = couns / couns1 * 100
                perc = round(perc, 2)

                perce = perc

                gb3 = gb2 - gb1
                print(gb3)
                for i in k:
                    print(i.Email)
                return render(request, 'atten7.html', {'k': k, 'gb3':gb3, 'dat': dat, 'perc': perc, 'perce': perce, 'stm': student,'class1':class1,'course':course,'sem':sem})
            except:
                mb = Registration.objects.all()
                cou = []
                cla = []
                sem = []
                for w in mb:
                    if w.Course not in cou and w.Course != '':
                        cou.append(w.Course)
                    if w.Class not in cla and w.Class != '' and w.Class is not None:
                        cla.append(w.Class)
                    if w.Semester not in sem and w.Semester != '' and w.Semester is not None:
                        sem.append(w.Semester)
                messages.success(request, 'Absent list not available')
                return render(request, 'atten_tea1.html', {'cou': cou, 'cla': cla, 'sem': sem, 'stb':stb})

        elif dat == '' and month != '' and week == '':
            month = request.POST.get('month')
            mon = month.split('-')
            year = mon[0]
            year = int(year)
            montt = mon[1]
            montt = int(montt)
            num_days = calendar.monthrange(year,montt)
            numm = num_days[1]
            numm = int(numm)
            dayy = []
            yeer = []
            montp = []
            for day in range(1,numm+1):
                day = str(day)
                year = str(year)
                montt = str(montt)
                if len(day) == 1:
                    dayy.append('0' + day)
                else:
                    dayy.append(day)
                yeer.append(year)
                if len(montt) == 1:
                    montp.append('0' + montt)
                else:
                    montp.append(montt)
            ghr = zip(yeer,montp,dayy)
            ghr1 =[]
            for a,b,c in ghr:
                d = str(a)+'-'+str(b)+'-'+str(c)
                ghr1.append(d)

            dailyy = []
            for w in ghr1:

                if student == 'Nil':
                    km = Registration.objects.filter(Class=class1, Course=course, Semester=sem)
                    kj = Attendance.objects.filter(Date=w)
                else:
                    sdm = int(student)
                    km = Registration.objects.filter(id=sdm)
                    for e in km:
                        kj = Attendance.objects.filter(Date=w, Email=e.Email)


                khg = []
                for u in kj:
                    for s in km:
                        if u.Email == s.Email and u.Email not in khg:
                            drp = '%H:%M'
                            time4 = datetime.datetime.strptime(time1, drp)
                            time5 = datetime.datetime.strptime(time2, drp)
                            tim3 = str(u.Time)
                            tim3 = datetime.datetime.strptime(tim3, drp)
                            if tim3 >= time4 and tim3 <= time5:
                                khg.append(u.Email)
                khg1 = []
                for uu in km:
                    if uu.Email not in khg1:
                        khg1.append(uu.Email)
                khf = set(khg)
                khf1 = set(khg1)
                khg2 = khf1 - khf
                dailyy1 = len(khg2) / len(khg1) * 100
                dailyy.append(dailyy1)
            cntr = 0
            for kp in dailyy:
                kp = int(kp)
                if kp == 100:
                    cntr += 1
            perce = (cntr/numm)*100
            tot = 0
            for we in range(0, len(dailyy)):
                tot += dailyy[we]
            perc = tot / len(dailyy)
            perc = round(perc, 2)


            try:
                nam = []
                em = []
                dat = []
                for w in ghr1:
                    datetime_object = datetime.datetime.strptime(w, "%Y-%m-%d")
                    bnc = datetime_object.strftime("%Y-%m-%d")

                    if student == 'Nil':
                        k = Registration.objects.filter(Class=class1, Course=course, Semester=sem)
                        dy = Attendance.objects.filter(Date=bnc)
                    else:
                        sdm = int(student)
                        k = Registration.objects.filter(id=sdm)
                        for e in k:
                            dy = Attendance.objects.filter(Date=bnc, Email=e.Email)
                    gs = []
                    for q in dy:
                        drp = '%H:%M'
                        time4 = datetime.datetime.strptime(time1, drp)
                        time5 = datetime.datetime.strptime(time2, drp)
                        tim3 = str(q.Time)
                        tim3 = datetime.datetime.strptime(tim3, drp)
                        if tim3 >= time4 and tim3 <= time5:
                            gs.append(q.Email)
                    gs1 = []
                    for h in k:
                        gs1.append(h.Email)
                    gs1 = set(gs1)
                    gs = set(gs)
                    gs2 = gs1 - gs
                    for iy in gs2:
                        for ww in k:
                            if iy == ww.Email:
                                dd = ww.First_name
                                dd = str(dd)
                                dtp = ww.Last_name
                                dtp = str(dtp)
                                mtp = dd + ' ' + dtp
                                nam.append(mtp)
                                em.append(iy)
                                dat.append(w)
                m4 = zip(nam, em, dat)
                return render(request, 'atten7.html', {'m4': m4,'perc':perc,'perce':perce})
            except:
                mb = Registration.objects.all()
                cou = []
                cla = []
                sem = []
                for w in mb:
                    if w.Course not in cou and w.Course != '':
                        cou.append(w.Course)
                    if w.Class not in cla and w.Class != '' and w.Class is not None:
                        cla.append(w.Class)
                    if w.Semester not in sem and w.Semester != '' and w.Semester is not None:
                        sem.append(w.Semester)
                messages.success(request, 'Absent list not available')
                return render(request, 'atten_tea1.html', {'cou': cou, 'cla': cla, 'sem': sem, 'stb':stb})

        elif dat == '' and month == '' and week != '':
            week = request.POST.get('week')
            r = datetime.datetime.strptime(week + '-1', "%Y-W%W-%w")
            r = str(r)
            r = r[0:10]
            r = r.split('-')
            a = r[0]
            a = int(a)
            b = r[1]
            b = int(b)
            c = r[2]
            c = int(c)
            base = datetime.datetime(a, b, c)
            days = datetime.timedelta(7)
            base = base - days
            mk = []
            for x in range(0, 6):
                y = base + datetime.timedelta(days = x)
                y = str(y)
                y = y[0:10]
                mk.append(y)
            dailyy = []
            for w in mk:
                if student == 'Nil':
                    km = Registration.objects.filter(Class=class1, Course=course, Semester=sem)
                    kj = Attendance.objects.filter(Date=w)
                else:
                    sdm = int(student)
                    km = Registration.objects.filter(id=sdm)
                    for e in km:
                        kj = Attendance.objects.filter(Date=w, Email=e.Email)
                khg = []
                for u in kj:
                    for s in km:
                        if u.Email == s.Email and u.Email not in khg:
                            drp = '%H:%M'
                            time4 = datetime.datetime.strptime(time1, drp)
                            time5 = datetime.datetime.strptime(time2, drp)
                            tim3 = str(u.Time)
                            tim3 = datetime.datetime.strptime(tim3, drp)
                            if tim3 >= time4 and tim3 <= time5:
                                khg.append(u.Email)
                khg1 = []
                for uu in km:
                    if uu.Email not in khg1:
                        khg1.append(uu.Email)
                khf = set(khg)
                khf1 = set(khg1)
                khg2 = khf1 - khf
                dailyy1 = len(khg2) / len(khg1) * 100
                dailyy.append(dailyy1)
            cntr = 0
            for kp in dailyy:
                kp = int(kp)
                if kp == 100:
                    cntr += 1
            perce = (cntr / 6) * 100
            perce = round(perce, 2)
            tot = 0
            for we in range(0, len(dailyy)):
                tot += dailyy[we]
            perc = tot / len(dailyy)
            perc = round(perc, 2)



            try:
                nam = []
                em = []
                dat = []
                for w in mk:
                    w = str(w)

                    if student == 'Nil':
                        k = Registration.objects.filter(Class=class1, Course=course, Semester=sem)
                        dy = Attendance.objects.filter(Date=w)
                    else:
                        sdm = int(student)
                        k = Registration.objects.filter(id=sdm)
                        for e in k:
                            dy = Attendance.objects.filter(Date=w, Email=e.Email)

                    gs = []
                    for q in dy:
                        drp = '%H:%M'
                        time4 = datetime.datetime.strptime(time1, drp)
                        time5 = datetime.datetime.strptime(time2, drp)
                        tim3 = str(q.Time)
                        tim3 = datetime.datetime.strptime(tim3, drp)
                        if tim3>=time4 and tim3<=time5:
                            gs.append(q.Email)
                    gs1 = []
                    for p in k:
                        gs1.append(p.Email)
                    gs = set(gs)
                    gs1 = set(gs1)
                    gs2 = gs1 - gs
                    gs2 = list(gs2)
                    for iy in gs2:
                        for ww in k:
                            if iy == ww.Email:
                                dd = ww.First_name
                                dd = str(dd)
                                dtp = ww.Last_name
                                dtp = str(dtp)
                                mtp = dd+' '+dtp
                                nam.append(mtp)
                                em.append(iy)
                                dat.append(w)
                m4 = zip(nam,em,dat)
                return render(request, 'atten7.html', {'m4': m4, 'perc':perc, 'perce':perce})
            except:
                mb = Registration.objects.all()
                cou = []
                cla = []
                sem = []
                for w in mb:
                    if w.Course not in cou and w.Course != '':
                        cou.append(w.Course)
                    if w.Class not in cla and w.Class != '' and w.Class is not None:
                        cla.append(w.Class)
                    if w.Semester not in sem and w.Semester != '' and w.Semester is not None:
                        sem.append(w.Semester)
                messages.success(request, 'Absent list not available')
                return render(request, 'atten_tea1.html', {'cou': cou, 'cla': cla, 'sem': sem, 'stb':stb})
        else:
            mb = Registration.objects.all()
            cou = []
            cla = []
            sem = []
            for w in mb:
                if w.Course not in cou and w.Course != '':
                    cou.append(w.Course)
                if w.Class not in cla and w.Class != '' and w.Class is not None:
                    cla.append(w.Class)
                if w.Semester not in sem and w.Semester != '' and w.Semester is not None:
                    sem.append(w.Semester)
            messages.success(request, 'Please select only one option (daily/weekly/monthly)')
            return render(request, 'atten_tea1.html', {'cou': cou, 'cla': cla, 'sem': sem, 'stb':stb})
    return render(request,'atten_tea1.html',{'cou':cou,'cla':cla,'sem':sem,'stb':stb})

def attention(request):
    dat = request.session['datte']
    m = Attendance.objects.filter(Date=dat)
    gb = request.session['atten_email']
    return render(request, 'atten5.html', {'m': m, 'gb': gb})

def attin(request):
    m = Attendance.objects.all()
    return render(request, 'atten.html', {'m': m})

def atten3(request):
    dat = request.POST.get('dat')
    m = Attendance.objects.filter(Date = dat)
    return render(request,'atten1.html',{'m':m})

def atten4(request):
    month = request.POST.get('month')
    mm = Attendance.objects.all()
    m = []
    m1 = []
    m2 = []
    m3 = []
    for i in mm:
        t = str(i.Date)
        t = t[0:7]
        if t == month:
            m.append(i.Name)
            m1.append(i.Email)
            m2.append(i.Date)
            m3.append(i.Time)
    m4 = zip(m,m1,m2,m3)

    return render(request,'atten3.html',{'m4':m4})

def atten5(request):
    week = request.POST.get('week')
    r = datetime.datetime.strptime(week + '-1', "%Y-W%W-%w")
    r = str(r)
    r = r[0:10]
    r = r.split('-')
    a = r[0]
    a = int(a)
    b = r[1]
    b = int(b)
    c = r[2]
    c = int(c)
    base = datetime.datetime(a,b,c)
    mk = []
    for x in range(0, 6):
        y = base + datetime.timedelta(days=x)
        y = str(y)
        y = y[0:10]
        mk.append(y)
    bv = Attendance.objects.all()
    return render(request,'atten4.html',{'bv':bv,'mk':mk})

def edit_atten(request, id):
    m = Attendance.objects.get(id = id)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        date = request.POST.get('date')
        time = request.POST.get('time')
        m.Name = name
        m.Email = email
        m.Date = date
        m.Time = time
        m.save()
        m = Attendance.objects.all()
        messages.success(request, 'Attendance edited successfully')
        return render(request, 'atten.html', {'m':m})
    return render(request,'edit_atten.html',{'m':m})

def edit_atten1(request, id):
    id = int(id)
    m = Attendance.objects.get(id = id)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        date = request.POST.get('date')
        time = request.POST.get('time')
        m.Name = name
        m.Email = email
        m.Date = date
        m.Time = time
        m.save()

        try:
            dat = request.session['datte']
            m = Attendance.objects.filter(Date = dat)
            gb = request.session['atten_email']
            messages.success(request, 'Attendance edited successfully')
            return render(request, 'atten5.html', {'m': m, 'gb': gb})
        except:
            ms = request.session['datte']
            m1 = request.session['datte1']
            m2 = request.session['datte2']
            m3 = request.session['datte3']
            m5 = request.session['datte4']
            m4 = zip(ms,m1,m2,m3,m5)
            gb = request.session['atten_email']
            messages.success(request, 'Attendance edited successfully')
            return render(request, 'atten5.html', {'m4': m4, 'gb': gb})
    return render(request,'edit_atten1.html',{'m':m})

def delete_atten(request, id):
    Attendance.objects.get(id = id).delete()
    m = Attendance.objects.all()
    messages.success(request, 'Attendance deleted')
    return render(request, 'atten.html', {'m': m})

def delete_atten1(request, id):
    id = int(id)
    Attendance.objects.get(id = id).delete()

    try:
        dat = request.session['datte']
        m = Attendance.objects.filter(Date=dat)
        gb = request.session['atten_email']
        messages.success(request, 'Attendance deleted successfully')
        return render(request, 'atten5.html', {'m': m, 'gb': gb})
    except:
        ms = request.session['datte']
        m1 = request.session['datte1']
        m2 = request.session['datte2']
        m3 = request.session['datte3']
        m5 = request.session['datte4']
        m4 = zip(ms, m1, m2, m3, m5)
        gb = request.session['atten_email']
        messages.success(request, 'Attendance deleted successfully')
        return render(request, 'atten5.html', {'m4': m4, 'gb': gb})


def add_atten(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        date = request.POST.get('date')
        time = request.POST.get('time')
        sw = Attendance()
        sw.Name = name
        sw.Email = email
        sw.Date = date
        sw.Time = time
        sw.save()
        m = Attendance.objects.all()
        messages.success(request, 'Attendance added')
        return render(request, 'atten.html', {'m': m})
    else:
        return render(request,'add_atten.html')

def add_atten1(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        date = request.POST.get('date')
        time = request.POST.get('time')
        sw = Attendance()
        sw.Name = name
        sw.Email = email
        sw.Date = date
        sw.Time = time
        sw.save()

        try:
            dat = request.session['datte']
            m = Attendance.objects.filter(Date=dat)
            gb = request.session['atten_email']
            messages.success(request, 'Attendance added successfully')
            return render(request, 'atten5.html', {'m': m, 'gb': gb})
        except:
            ms = request.session['datte']
            m1 = request.session['datte1']
            m2 = request.session['datte2']
            m3 = request.session['datte3']
            m5 = request.session['datte4']
            m4 = zip(ms, m1, m2, m3, m5)
            gb = request.session['atten_email']
            messages.success(request, 'Attendance added successfully')
            return render(request, 'atten5.html', {'m4': m4, 'gb': gb})
    else:
        return render(request,'add_atten1.html')


def adm_prof(request):
    gtt = Registration.objects.filter(User_role = 'admin')
    return render(request, 'adm_prof.html',{'gtt':gtt})

def del_admin(request, id):
    local_tz = pytz.timezone("Asia/Calcutta")
    fg = Exam.objects.all()
    kk = []
    for i in fg:
        bb = i.Time_start
        cpp = bb.replace(tzinfo=pytz.utc).astimezone(local_tz)
        bbn = cpp.strftime("%Y-%B-%d %H:%M:%S %p")
        if bbn not in kk:
            kk.append('Student name - ')
            kk.append(i.Student_name)
            kk.append('; ')
            kk.append('Subject name - ')
            kk.append(i.Subject_name)
            kk.append('; ')
            kk.append('Start time - ')
            ft = i.Time_start
            ftt = ft.replace(tzinfo=pytz.utc).astimezone(local_tz)
            fty = ftt.strftime("%Y-%B-%d %H:%M:%S %p")
            kk.append(fty)
            kk.append('; ')
            kk.append('Stop time - ')
            fte = i.Time_stop
            ftee = fte.replace(tzinfo=pytz.utc).astimezone(local_tz)
            fty1 = ftee.strftime("%Y-%B-%d %H:%M:%S %p")
            kk.append(fty1)
            kk.append('mh')

    Registration.objects.get(id = id).delete()
    messages.success(request, 'You have successfully resigned from administration')
    return render(request, 'home.html', {'kk':kk})

def edit_admin(request):
    bb1 = Registration.objects.get(User_role = 'admin')
    return render(request, 'update_admin.html',{'bb1':bb1})

def feedbak(request):
    se = Feedback.objects.filter(Teacher_email = 'Nil@Nil')
    return render(request,'feedbak.html',{'se':se})

def forward_t_t(request, id):
    se = Feedback.objects.get(id = id)
    request.session['fdd'] = se.id
    sm = Registration.objects.filter(User_role = 'teacher')
    return render(request, 'feedbak1.html', {'se': se,'sm':sm})

def feedbak2(request):
    kk = request.session['fdd']
    kk = int(kk)
    pk = Feedback.objects.get(id = kk)
    teac = request.POST.get('teac')
    teac = int(teac)
    tm = Registration.objects.get(id = teac)
    mn = Feedback()
    mn.Student_name = pk.Student_name
    mn.Student_email = pk.Student_email
    mn.Course_name = pk.Course_name
    mn.Feedback_text = pk.Feedback_text
    mn.Submission_date = pk.Submission_date
    mn.Feed_reg = pk.Feed_reg
    mn.Teacher_email = tm.Email
    mn.save()
    messages.success(request, 'Message has been forwarded to teacher')
    return render(request, 'admin_home.html')

def feedback_teacher(request):
    mn = Registration.objects.get(id = request.session['logg'])
    tt = Feedback.objects.filter(Teacher_email = mn.Email)
    return render(request,'feedback_teacher.html',{'tt':tt})

def delete_feedback(request, id):
    Feedback.objects.get(id=id).delete()
    se = Feedback.objects.all()
    return render(request, 'feedbak.html', {'se': se})

def pass_req(request):
    dd = Requests.objects.all()
    return render(request,'pass_req.html',{'dd':dd})

def pass_req1(request, id):
    ff = Requests.objects.get(id = id)
    tt = Registration.objects.get(Email = ff.Email)
    tt.Password = ff.New_password
    tt.save()
    Requests.objects.get(id=id).delete()
    dd = Requests.objects.all()
    return render(request, 'pass_req.html', {'dd': dd})

def course(request):
    cou = Course.objects.all()
    return render(request,'course.html',{'cou':cou})

def course1(request):
    cou = Course.objects.all()
    return render(request,'course1.html',{'cou':cou})

def course2(request):
    cou = Course.objects.all()
    return render(request, 'course2.html', {'cou': cou})

def ch_p11(request):
    th = Registration.objects.get(id = request.session['logg'])
    if request.method == 'POST':
        new_pass = request.POST.get('pssw')
        old_pass = request.POST.get('pssw_old')
        email = request.POST.get('em')
        cate = request.POST.get('usr')
        nam = request.POST.get('nam')
        g = Requests()
        g.Name = nam
        g.Email = email
        g.User_category = cate
        g.Old_password = old_pass
        g.New_password = new_pass
        g.Req_reg = th
        g.save()
        messages.success(request, 'Please wait for your password approval.. Continue to use old password')
        return render(request, 'teacher_home.html')
    return render(request, 'change_password1.html', {'th': th})

def m_m1(request):
    p = Registration.objects.get(id = request.session['logg'])
    bb = Messages.objects.filter(To_email = p.Email)
    return render(request,'message1.html',{'bb':bb})

def del_msg_teacher(request,id):
    Messages.objects.get(id = id).delete()
    p = Registration.objects.get(id = request.session['logg'])
    bb = Messages.objects.filter(To_email = p.Email)
    messages.success(request, 'Message deleted successfully')
    return render(request,'message1.html',{'bb':bb})

def reply_msg_teacher(request,id):
    pa = Messages.objects.get(id = id)
    p = Registration.objects.get(id = request.session['logg'])
    bb = Messages.objects.filter(To_email = p.Email)
    if request.method == 'POST':
        f_email = request.POST.get('f_email')
        to_email = request.POST.get('to_email')
        msg_cont = request.POST.get('msg_cont')
        pa1 = Messages()
        pa1.Category = p.User_role
        pa1.From_email = to_email
        pa1.To_email = f_email
        pa1.Message_content = msg_cont
        pa1.save()
        messages.success(request, 'Message reply successful')
        return render(request, 'message1.html', {'bb': bb})
    return render(request,'reply_msg_teacher1.html',{'pa':pa})

def block(request):
    t_reg = Registration.objects.filter(Q(User_role="teacher") | Q(User_role="teacher_blocked"))
    s_reg = Registration.objects.filter(Q(User_role="student") | Q(User_role="student_blocked"))
    return render(request,'block.html',{'t_reg':t_reg,'s_reg':s_reg})

def blocks(request, id):
    klk = Registration.objects.get(id=id)
    klk.User_role = 'teacher_blocked'
    klk.save()
    t_reg = Registration.objects.filter(Q(User_role = "teacher") | Q(User_role = "teacher_blocked"))
    s_reg = Registration.objects.filter(Q(User_role = "student") | Q(User_role = "student_blocked"))
    return render(request, 'block.html', {'t_reg': t_reg, 's_reg': s_reg})

def allows(request, id):
    klk = Registration.objects.get(id=id)
    klk.User_role = 'teacher'
    klk.save()
    t_reg = Registration.objects.filter(Q(User_role="teacher") | Q(User_role="teacher_blocked"))
    s_reg = Registration.objects.filter(Q(User_role="student") | Q(User_role="student_blocked"))
    return render(request, 'block.html', {'t_reg': t_reg, 's_reg': s_reg})

def blocks1(request, id):
    klk = Registration.objects.get(id=id)
    klk.User_role = 'student_blocked'
    klk.save()
    t_reg = Registration.objects.filter(Q(User_role = "teacher") | Q(User_role = "teacher_blocked"))
    s_reg = Registration.objects.filter(Q(User_role = "student") | Q(User_role = "student_blocked"))
    return render(request, 'block.html', {'t_reg': t_reg, 's_reg': s_reg})

def allows1(request, id):
    klk = Registration.objects.get(id=id)
    klk.User_role = 'student'
    klk.save()
    t_reg = Registration.objects.filter(Q(User_role="teacher") | Q(User_role="teacher_blocked"))
    s_reg = Registration.objects.filter(Q(User_role="student") | Q(User_role="student_blocked"))
    return render(request, 'block.html', {'t_reg': t_reg, 's_reg': s_reg})

def add_blog(request):
    local_tz = pytz.timezone("Asia/Calcutta")
    fg = Exam.objects.all()
    kk = []
    for i in fg:
        bb = i.Time_start
        cpp = bb.replace(tzinfo=pytz.utc).astimezone(local_tz)
        bbn = cpp.strftime("%Y-%B-%d %H:%M:%S %p")
        if bbn not in kk:
            kk.append('Student name - ')
            kk.append(i.Student_name)
            kk.append('; ')
            kk.append('Subject name - ')
            kk.append(i.Subject_name)
            kk.append('; ')
            kk.append('Start time - ')
            ft = i.Time_start
            ftt = ft.replace(tzinfo=pytz.utc).astimezone(local_tz)
            fty = ftt.strftime("%Y-%B-%d %H:%M:%S %p")
            kk.append(fty)
            kk.append('; ')
            kk.append('Stop time - ')
            fte = i.Time_stop
            ftee = fte.replace(tzinfo=pytz.utc).astimezone(local_tz)
            fty1 = ftee.strftime("%Y-%B-%d %H:%M:%S %p")
            kk.append(fty1)
            kk.append('mh')


    if request.method == 'POST':
        nam = request.POST.get('nam')
        c_b = request.POST.get('c_b')
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        fs.save(photo.name, photo)
        date1 = request.POST.get('date1')
        b = Blogs()
        b.Name = nam
        b.Blog_content = c_b
        b.Image = photo
        b.Date_blog = date1
        b.Approval_status = 'Rejected'
        b.save()
        messages.success(request, 'Blog added successfully. Please wait for approval')
        return render(request, 'home.html',{'kk':kk})
    return render(request,'add_blog.html')

def view_blog(request):
    dc = Blogs.objects.filter(Approval_status = 'Approved')
    return render(request,'display_blog.html',{'dc':dc})

def blogs_admin(request):
    dm = Blogs.objects.all()
    return render(request,'blogs_admin.html',{'dm':dm})

def blog_approves(request,id):
    sas = Blogs.objects.get(id=id)
    sas.Approval_status = 'Approved'
    sas.save()
    dm = Blogs.objects.all()
    return render(request, 'blogs_admin.html', {'dm': dm})

def blog_rejects(request, id):
    sas = Blogs.objects.get(id=id)
    sas.Approval_status = 'Rejected'
    sas.save()
    dm = Blogs.objects.all()
    return render(request, 'blogs_admin.html', {'dm': dm})

def blog_delete(request, id):
    Blogs.objects.get(id=id).delete()
    dm = Blogs.objects.all()
    return render(request, 'blogs_admin.html', {'dm': dm})

def ch_p(request):
    th = Registration.objects.get(id = request.session['logg'])
    if request.method == 'POST':
        new_pass = request.POST.get('pssw')
        old_pass = request.POST.get('pssw_old')
        email = request.POST.get('em')
        cate = request.POST.get('usr')
        nam = request.POST.get('nam')
        g = Requests()
        g.Name = nam
        g.Email = email
        g.User_category = cate
        g.Old_password = old_pass
        g.New_password = new_pass
        g.Req_reg = th
        g.save()
        messages.success(request, 'Please wait for your password approval.. Continue to use old password')
        return render(request, 'student_home.html')
    return render(request,'change_password.html',{'th':th})

def update_pr_st(request):
    b = Registration.objects.get(id = request.session['logg'])
    if request.method == 'POST':
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')

        if (not f_name.isalpha()) or (not l_name.isalpha()):
            messages.success(request, 'Non-alphabetic characters not allowed in name')
            return render(request, 'update_pr_st.html', {'b': b})

        email = request.POST.get('email')
        addr = request.POST.get('addr')
        dob = request.POST.get('dob')

        dob1 = dob.split('-')
        aa = int(dob1[0])
        ab = int(dob1[1])
        ac = int(dob1[2])
        t = date.today()
        u = date(aa, ab, ac)
        v = relativedelta.relativedelta(t, u)
        v = v.years
        if v < 18:
            messages.success(request, 'Age should be above 18 years. Please check DOB.')
            return render(request, 'update_pr_st.html', {'b': b})

        d_c = request.POST.get('d_c')
        phone = request.POST.get('phone')
        p_phone = request.POST.get('p_phone')

        if len(phone) != 10 or len(p_phone) != 10:
            messages.success(request, 'Entered phone number is not valid')
            return render(request, 'update_pr_st.html', {'b': b})
        if (not phone.isdigit()) or (not p_phone.isdigit()):
            messages.success(request, 'Alphabetic characters not allowed in phone number')
            return render(request, 'update_pr_st.html', {'b': b})

        gender = request.POST.get('gender')
        b.First_name = f_name
        b.Last_name = l_name
        b.Email = email
        b.Address = addr
        b.DOB = dob
        b.DOJ_course = d_c
        b.Phone = phone
        b.Parent_phone = p_phone
        b.Gender = gender
        b.save()
        messages.success(request, 'Profile updated')
        return render(request,'student_home.html')
    return render(request, 'update_pr_st.html', {'b': b})


def register_tr(request):
    local_tz = pytz.timezone("Asia/Calcutta")
    fg = Exam.objects.all()
    kk = []
    for i in fg:
        bb = i.Time_start
        cpp = bb.replace(tzinfo=pytz.utc).astimezone(local_tz)
        bbn = cpp.strftime("%Y-%B-%d %H:%M:%S %p")
        if bbn not in kk:
            kk.append('Student name - ')
            kk.append(i.Student_name)
            kk.append('; ')
            kk.append('Subject name - ')
            kk.append(i.Subject_name)
            kk.append('; ')
            kk.append('Start time - ')
            ft = i.Time_start
            ftt = ft.replace(tzinfo=pytz.utc).astimezone(local_tz)
            fty = ftt.strftime("%Y-%B-%d %H:%M:%S %p")
            kk.append(fty)
            kk.append('; ')
            kk.append('Stop time - ')
            fte = i.Time_stop
            ftee = fte.replace(tzinfo=pytz.utc).astimezone(local_tz)
            fty1 = ftee.strftime("%Y-%B-%d %H:%M:%S %p")
            kk.append(fty1)
            kk.append('mh')


    if request.method == 'POST':
        x = datetime.datetime.now()
        y = x.strftime("%Y-%m-%d")
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if (not first_name.isalpha()) or (not last_name.isalpha()):
            messages.success(request, 'Non-alphabetic characters not allowed in name')
            return render(request, 'register_teacher.html')

        email = request.POST.get('email')
        psw = request.POST.get('psw')
        teach = request.POST.get('teacher')
        addr = request.POST.get('addr')
        dob = request.POST.get('dob')

        dob1 = dob.split('-')
        aa = int(dob1[0])
        ab = int(dob1[1])
        ac = int(dob1[2])
        t = date.today()
        u = date(aa, ab, ac)
        v = relativedelta.relativedelta(t, u)
        v = v.years
        if v <= 25:
            messages.success(request, 'Registration allowed for teachers above 25 years old')
            return render(request, 'register_teacher.html')

        gender = request.POST.get('gender')
        phone = request.POST.get('phone')

        if not phone.isdigit():
            messages.success(request, 'Alphabetic characters not allowed in phone number')
            return render(request, 'register_teacher.html')

        if len(phone) != 10:
            messages.success(request, 'Entered phone number is not valid')
            return render(request, 'register_teacher.html')

        qual = request.POST.get('qual')
        reg1 = Registration.objects.all()
        for i in reg1:
            if i.Email == email:
                messages.success(request, 'Teacher already exists')
                return render(request, 'home.html',{'kk':kk})
        t = Registration()
        t.First_name = first_name
        t.Last_name = last_name
        t.Email = email
        t.Password = psw
        t.Registration_date = y
        t.About_website = 'Nil'
        t.User_role = teach
        t.Address = addr
        t.DOB = dob
        t.Gender = gender
        t.Phone = phone
        t.Qualification = qual
        t.save()
        messages.success(request, 'You have successfully registered')
        return render(request, 'home.html',{'kk':kk})
    else:
        return render(request, 'register_teacher.html')

def edit_course(request, id):
    id = int(id)
    ccf = Course.objects.get(id = id)
    if request.method == 'POST':
        dep = request.POST.get('dep')
        cou1 = request.POST.get('cou')
        sub = request.POST.get('sub')
        ccf.Department = dep
        ccf.Course = cou1
        ccf.Subject = sub
        ccf.save()
        cou = Course.objects.all()
        messages.success(request, 'Course edited')
        return render(request, 'course.html',{'cou':cou})
    return render(request,'edit_course.html',{'ccf':ccf})

def delete_course(request, id):
    Course.objects.get(id = id).delete()
    cou = Course.objects.all()
    messages.success(request, 'Course deleted')
    return render(request,'course.html',{'cou':cou})

def bnb(request):
    if request.method == 'POST':
        first = request.POST.get('first')
        last = request.POST.get('last')

        if (not first.isalpha()) or (not last.isalpha()):
            bb1 = Registration.objects.get(User_role='admin')
            messages.success(request, 'Non-alphabetic characters not allowed in name')
            return render(request, 'update_admin.html', {'bb1': bb1})

        em = request.POST.get('em')
        psw = request.POST.get('psw')
        addr = request.POST.get('addr')
        dob = request.POST.get('dob')

        dob1 = dob.split('-')
        aa = int(dob1[0])
        ab = int(dob1[1])
        ac = int(dob1[2])
        t = date.today()
        u = date(aa, ab, ac)
        v = relativedelta.relativedelta(t, u)
        v = v.years
        if v < 18:
            bb1 = Registration.objects.get(User_role='admin')
            messages.success(request, 'Age should be above 18 years. Please check DOB.')
            return render(request, 'update_admin.html', {'bb1': bb1})

        gender = request.POST.get('gender')
        phone = request.POST.get('phone')

        if len(phone) != 10:
            bb1 = Registration.objects.get(User_role='admin')
            messages.success(request, 'Entered phone number is not valid')
            return render(request, 'update_admin.html', {'bb1': bb1})
        if not phone.isdigit():
            bb1 = Registration.objects.get(User_role='admin')
            messages.success(request, 'Alphabetic characters not allowed in phone number')
            return render(request, 'update_admin.html', {'bb1': bb1})

        dcd = Registration.objects.get(User_role = 'admin')
        dcd.Email = em
        dcd.Password = psw
        dcd.First_name = first
        dcd.Last_name = last
        dcd.Email = em
        dcd.Password = psw
        dcd.Address = addr
        dcd.DOB = dob
        dcd.Gender = gender
        dcd.Phone = phone
        dcd.save()
        gtt = Registration.objects.filter(User_role='admin')
        messages.success(request, 'You have successfully updated your profile')
        return render(request, 'adm_prof.html', {'gtt': gtt})
    else:
        return render(request, "admin_home.html")




