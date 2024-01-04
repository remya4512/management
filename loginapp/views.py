from django.shortcuts import render,redirect
from loginapp.models import Course,Student,Usermember
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
import os
# Create your views here.

def index(request):
    return render(request,'index.html')

def admin_login(request):
    if request.method=='POST':
        username=request.POST['name']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            if user.is_staff:
                login(request,user)
                return redirect('admin_home')
            else:
                login(request,user)
                auth.login(request,user)
                messages.info(request,f'Welcome {username}')
                return redirect('user_home')
        else:
            messages.info(request,'Invalid username or password...Try again')
            return redirect('/')
    return render(request,'index.html')

def user_home(request):
    if request.user.is_authenticated:
        return render(request,'user_home.html')
    return redirect('/')

def admin_home(request):
    if request.user.is_authenticated and request.user.is_staff:
        return render(request,'admin_home.html')
    return redirect('index.html')

def teacher_signup(request):
    courses=Course.objects.all()
    return render(request,'teacher_signup.html',{'course':courses}) 
    

def add_course(request):
    if request.user.is_authenticated:
        return render(request,'add_course.html')
    return redirect('/')

def add_coursedb(request):
    if request.method=='POST':
        course_name =request.POST['course']
        course_fee=request.POST['fee']
        course=Course(course_name=course_name,fee=course_fee)
        course.save()
        return redirect('/')
    
def add_teacherdb(request):
        if request.method=='POST':
            fname=request.POST['fname']  
            lname=request.POST['lname']  
            uname=request.POST['uname']  
            password=request.POST['password']  
            cpassword=request.POST['cpassword']  
            email=request.POST['email']
            address=request.POST['address']  
            age=request.POST['age']  
            number=request.POST['number']  
            sel=request.POST['sel']  
            course1=Course.objects.get(id=sel)  
            image=request.FILES.get('file')
            if password==cpassword:
                if User.objects.filter(username=uname).exists():
                    messages.info(request,'This username already exists.....')
                    return redirect('teacher_signup')
                else:
                    user=User.objects.create_user(first_name=fname,last_name=lname,username=uname,password=password,email=email)
                    user.save()

                    member=Usermember(address=address,age=age,number=number,course=course1,user=user,image=image)
                    member.save()
                    return redirect('/')
            else:
                messages.info(request,'password does not match..')
                return redirect('teacher_signup')
            
        else:
            return redirect('index.html')
        

def add_student(request):
    courses=Course.objects.all()
    return render(request,'add_student.html',{'course':courses}) 

def add_studentdb(request):
    if request.method=='POST':
        student_name =request.POST['name']  
        student_address =request.POST['address'] 
        age=request.POST['age'] 
        jdate=request.POST['jdate']
        sel=request.POST['sel'] 

        course1=Course.objects.get(id=sel)
        student=Student(student_name=student_name,student_address=student_address,student_age=age,joining_date=jdate,course=course1)
        student.save()
        return redirect('/')  

def show_details(request):
    student=Student.objects.all()
    return render(request,'show_details.html',{'students':student}) 

def admin_logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('/')

def editpage(request,pk):
    student=Student.objects.get(id=pk)
    course=Course.objects.all()
    return render(request,'editpage.html',{'student':student,'course':course}) 

def deletepage(request,pk):
   s=Student.objects.get(id=pk)
   s.delete()
   return redirect('show_details')

def editdb(request,pk):
    if request.method=='POST':
      student=Student.objects.get(id=pk)
      

      student.student_name=request.POST.get('name')
      student.student_address=request.POST.get('address')
      student.student_age=request.POST.get('age')
      student.joining_date=request.POST.get('jdate')

      
      
      courseid=request.POST['sel']
      student.course=Course.objects.get(id=courseid)  
      student.save()
      return redirect('show_details')
   
    return render(request,"editpage.html")


def profile(request):
    if request.user.is_authenticated:
        current_user=request.user.id

        user1=Usermember.objects.get(user_id=current_user)
        return render(request,'profile.html',{'users':user1})
    
def show_teacher(request):
    if request.user.is_authenticated:
        user1=Usermember.objects.all()
        return render(request,'show_teacher.html',{'user':user1})
    return redirect('/')

def delete(request,pk):
    user=Usermember.objects.get(id=pk)
    if user.image:
        user.image.delete() 
    user.delete() 
    user.user.delete() 
    return redirect('show_teacher')




def user_edit(request):
    if request.user.is_authenticated:
        current_user=request.user.id
        courses=Course.objects.all()
        user1=Usermember.objects.get(user_id=current_user)
        return render(request,'user_edit.html',{'users':user1,'course':courses})
    
        
         
    
    
    
def edit(request):
    if request.user.is_authenticated:
        current_user=request.user.id
        
        user1=Usermember.objects.get(user_id=current_user)
        user2=User.objects.get(id=current_user)
        if request.method=='POST': 
            if len(request.FILES)!=0:
                if len(user1.image)>0:
                    os.remove(user1.image.path)
                user1.image=request.FILES.get('file')
            user2.first_name=request.POST.get('fname')
            user2.last_name=request.POST.get('lname')
            user2.username=request.POST.get('uname')
            
            user2.email=request.POST.get('email')
            user1.age=request.POST.get('age')
            user1.address=request.POST.get('address')
            user1.number=request.POST.get('number')
            
            courseid=request.POST['sel']
            user1.course=Course.objects.get(id=courseid)  
              
            user1.save()
            user2.save()
            return redirect('profile')
        return render(request,'user_edit.html',{'users':user1})
    return redirect('/')   


        


