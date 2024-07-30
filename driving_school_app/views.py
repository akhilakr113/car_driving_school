from django.shortcuts import render
# from flask import redirect
from . models import *
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
import datetime
from datetime import *
from django.contrib.auth.decorators import login_required
from django.contrib import auth

def logout(request):
    auth.logout(request)
    q=Complaint.objects.all()
    return render(request,'home.html',{'q':q})

def logout1(request):
    auth.logout(request)
    q=Complaint.objects.all()
    return render(request,'home.html',{'q':q})



def home(request):
    return render(request,"home.html")


def login_form(request):
    if request.method=='POST':
        uname=request.POST['uname']
        passw=request.POST['pass']
        try:
            lg=Login.objects.get(username=uname,password=passw)
            print(lg,"***********************************")
            request.session['loginid']=lg.pk
            if lg.usertype == 'admin':
                ob1 = auth.authenticate(username='admin', password='admin')
                if ob1 is not None:
                    auth.login(request, ob1)
                return HttpResponse("<script>alert('Login Successfully');window.location='/adminhome';</script>")
            

            if lg.usertype == 'driving':
                st=Drivingschool.objects.get(login_id=lg.pk)
                if st:
                    request.session['drivingschool_id']=st.pk
                    print(request.session['drivingschool_id'])
                    ob1 = auth.authenticate(username='admin', password='admin')
                    if ob1 is not None:
                        auth.login(request, ob1)
                return HttpResponse("<script>alert('Login Successfully');window.location='/drivingschoolhome';</script>")
            
            if lg.usertype == 'trainer':
              
                ur=Trainer.objects.get(login_id=lg.pk)
                if ur:
                    request.session['trainer_id']=ur.pk
                    ob1 = auth.authenticate(username='admin', password='admin')
                    if ob1 is not None:
                        auth.login(request, ob1)

                return HttpResponse("<script>alert('Login Successfully');window.location='/trainerhome';</script>")
            
            if lg.usertype == 'user':
                print("###############")
                ur=User.objects.get(login_id=lg.pk)
                if ur:
                    request.session['user_id']=ur.pk
                    ob1 = auth.authenticate(username='admin', password='admin')
                    if ob1 is not None:
                        auth.login(request, ob1)
                return HttpResponse("<script>alert('Login Successfully');window.location='/userhome';</script>")
        

        except:
            return HttpResponse("<script>alert('Invalid Username Or Password');window.location='/login';</script>")


    return render(request,"login.html")
def forgot_password(request):
    if 'forgot' in request.POST:
        uname = request.POST.get('uname')
        email = request.POST.get('email')

        # Check if a user with the given username exists in the Login model
        if Login.objects.filter(username=uname).exists():
            request.session['username'] = uname
            # Check if the email exists in the User model
            if User.objects.filter(email=email).exists():
                return HttpResponseRedirect("/new_password/%s" % uname)

            # Check if the email exists in the Drivingschool model
            elif Drivingschool.objects.filter(email=email).exists():
                return HttpResponseRedirect("/new_password/%s" % uname)

            # Check if the email exists in the Trainer model
            elif Trainer.objects.filter(email=email).exists():
                return HttpResponseRedirect("/new_password/%s" % uname)

    return render(request, 'forgot_password.html')
def new_password(request,uname):
    
    if 'new_p' in request.POST:
        np=request.POST['np']
        cp=request.POST['cp']
        if np == cp:
            
            lg=Login.objects.get(username=uname)
            print(lg)
            lg.password=cp
            lg.save()
            return HttpResponse("<script>alert('Password Successfully Changed.');window.location='/login'</script>")
        else:
            return HttpResponse("<script>alert('Confirm password mismatched.');window.location='/forgot_password'</script>")
   

    return render(request,'new_p.html') 



def  driving_school_register(request):
    if request.method=='POST':
        dname=request.POST['dname']
        place=request.POST['place']
        no=request.POST['no']
        mail=request.POST['mail']
        License=request.POST['line']
        uname=request.POST['uname']
        passw=request.POST['passw']
        lat=request.POST['latitudes']
        lon=request.POST['longitudes']
        lg=Login.objects.filter(username=uname,password=passw)
        nn=Drivingschool.objects.filter(phone=no)
        ni=Drivingschool.objects.filter(email=mail)
        nh=Drivingschool.objects.filter(license=License)

        print("lg===========",lg,"nn+++++++++",nn)

        if lg or nn or ni  :
            return HttpResponse("<script>alert('Username/Password/Phone/Email Already Exist..!!');window.location='/driving_school_register';</script>")
        if nh:
            return HttpResponse("<script>alert('Licence Number  Already Exist..!!');window.location='/driving_school_register';</script>")

        else:

            log=Login(username=uname,password=passw,usertype='pending')
            log.save()
            st=Drivingschool(name=dname,place=place,Latitude=lat,Cat="777",Longitude=lon,phone=no,email=mail,license=License,login=log)
            st.save()
            return HttpResponse("<script>alert('Successfully Registered');window.location='/driving_school_register';</script>")
    return render(request,"driving_school_registration.html")

def user_register(request):
    m = Drivingschool.objects.filter(login__usertype='driving')
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        place=request.POST['place']
        no=request.POST['no']
        mail=request.POST['mail']
        dob=request.POST['dob']
        gender=request.POST['gender']
        ds=request.POST['ds']
        uname=request.POST['uname']
        passw=request.POST['passw']
        lg=Login.objects.filter(username=uname,password=passw)
        nn=User.objects.filter(phone=no)
        ff=User.objects.filter(email=mail)
        print("lg===========",lg,"nn+++++++++",nn)

        if lg or nn or ff :
            return HttpResponse("<script>alert('Username/Password/Phone/Email Already Exist..!!');window.location='/user_register';</script>")
        else:
            log=Login(username=uname,password=passw,usertype='user')
            log.save()
            st=User(fname=fname,lname=lname,place=place,phone=no,email=mail,dob=dob,gender=gender,login=log,Drivingschool_id=ds)
            st.save()
            return HttpResponse("<script>alert('Successfully Registered');window.location='/user_register';</script>")
        
        
    return render(request,"user_register.html",{'m':m})


###############################ADMIN#########################################

@login_required(login_url='/')  
def adminhome(request):
    return render(request,'adminhome.html')
@login_required(login_url='/')  
def  managecategory(request):
    if request.method=='POST':
        categoryname=request.POST['catname']
        cat=Categories(category_name=categoryname)
        cat.save()
        return HttpResponse("<script>alert('Successfully ADD');window.location='/managecategory';</script>")
    
    view=Categories.objects.all()

    return render(request,'admin_manage_categories.html',{'view':view})
@login_required(login_url='/')  
def categoryupdate(request,catid):
    up=Categories.objects.get(categories_id=catid)
    if request.method=='POST':
        cat=request.POST['cat']
        up.category_name=cat
        up.save()
        return HttpResponse("<script>alert('Update Successfully');window.location='/managecategory';</script>")

    return render(request,"admin_manage_categories.html",{'up':up})

@login_required(login_url='/')  
def  categorydelete(request,catid):
    up=Categories.objects.get(categories_id=catid)
    up.delete()
    return HttpResponse("<script>alert('Delete Successfully');window.location='/managecategory';</script>")

@login_required(login_url='/')  
def viewdrivingschool(request):
    dr=Drivingschool.objects.all()
    return render(request,"admin_view_driving_school.html",{'dr':dr})
@login_required(login_url='/')  
def adminaccept_driving(request,did,lid):
    dr=Login.objects.get(login_id=lid)
    dr.usertype='driving'
    dr.save()
    return HttpResponse("<script>alert(' Accepted Successfully ');window.location='/viewdrivingschool';</script>")
@login_required(login_url='/')  
def adminreject_driving(request,lid,did):
    dr=Login.objects.get(login_id=lid)
    f=Drivingschool.objects.get(login_id=lid)
    dr.delete()
    f.delete()
    return HttpResponse("<script>alert(' Rejected Successfully ');window.location='/viewdrivingschool';</script>")
@login_required(login_url='/')  
def viewtrainer(request,tid):
    tr=Trainer.objects.filter(drivingschool=tid)
    return render(request,"admin_view_trainer.html",{'tr':tr})
@login_required(login_url='/')  
def admin_view_users(request):
    ur=User.objects.all()
    return render(request,"admin_view_users.html",{'ur':ur})
@login_required(login_url='/')  
def admin_view_licence_req(request):
    c=LicenseRequest.objects.all()

    if request.method == 'POST':
        from_date = request.POST.get('fd')

        if from_date:  
            c = c.filter(date=from_date)
     
    return render(request,"admin_view_licence_req.html",{'ur':c})

@login_required(login_url='/')  
def admin_view_driving_req(request):
    c=DrivingRequest.objects.all()

    if request.method == 'POST':
        from_date = request.POST.get('fd')

        if from_date:  
            c = c.filter(date=from_date)
     
    return render(request,"admin_view_driving_req.html",{'ur':c})
@login_required(login_url='/')  
def admin_view_complaints(request):
    comp=Complaint.objects.all()
    return render(request,"admin_view_complaints.html",{'comp':comp})

@login_required(login_url='/')  
def admin_send_reply(request,id):
    if request.method=='POST':
        rep=Complaint.objects.get(complaint_id=id)

        replys=request.POST['rep']
        rep.reply_text=replys
        rep.save()
        return HttpResponse("<script>alert(' Send Successfully ');window.location='/admin_view_complaints';</script>")
    
    return render(request,"admin_send_reply.html")



#############################################Drivingschool################################

@login_required(login_url='/')  
def drivingschoolhome(request):
    return render(request,"driving_school_home.html")

@login_required(login_url='/')  
def managetrainer(request):
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        place=request.POST['place']
        no=request.POST['no']
        mail=request.POST['mail']
        dob=request.POST['dob']
        gender=request.POST['gender']
        uname=request.POST['uname']
        passw=request.POST['passw']
        lg=Login.objects.filter(username=uname,password=passw)
        nn=Trainer.objects.filter(phone=no)
        nl=Trainer.objects.filter(email=mail)

        print("lg===========",lg,"nn+++++++++",nn)

        if lg or nn or nl :
            return HttpResponse("<script>alert('Username/Password/Phone/Email Already Exist..!!');window.location='/managetrainer';</script>")
        else:
            log=Login(username=uname,password=passw,usertype='trainer')
            log.save()
            st=Trainer(drivingschool_id=request.session['drivingschool_id'],fname=fname,lname=lname,place=place,phone=no,email=mail,dob=dob,gender=gender,login=log)
            st.save()
            return HttpResponse("<script>alert('Successfully Registered');window.location='/managetrainer';</script>")
        
    tt=Trainer.objects.filter(drivingschool_id=request.session['drivingschool_id'])
        
    return render(request,"driving_manage_trainer.html",{'tt':tt})

@login_required(login_url='/')  
def trainerdelete(request,id):
    up=Trainer.objects.get(trainer_id=id)
    up.delete()
    return HttpResponse("<script>alert('Delete Successfully');window.location='/managetrainer';</script>")
@login_required(login_url='/')  
def trainerupdate(request,id):
    up=Trainer.objects.get(trainer_id=id)
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        place=request.POST['place']
        no=request.POST['no']
        mail=request.POST['mail']
        dob=request.POST['dob']
        gender=request.POST['gender']

        up.fname=fname
        up.lname=lname
        up.place=place
        up.phone=no
        up.email=mail
        up.dob=dob
        up.gender=gender
        up.save()
        return HttpResponse("<script>alert('Update Successfully');window.location='/managetrainer';</script>")

    return render(request,"driving_manage_trainer.html",{'up':up})

@login_required(login_url='/')  
def viewqueries(request):
    qu=Queries.objects.filter(drivingschool=request.session['drivingschool_id'])
    return render(request,"drving_view_queries.html",{'qu':qu})

@login_required(login_url='/')  
def sendqueries(request,id):
    rr=Queries.objects.get(queries_id=id)
    if request.method=='POST':
        replys=request.POST['rep']
        rr.reply=replys
        rr.save()
        return HttpResponse("<script>alert(' Send Successfully ');window.location='/viewqueries';</script>")


    return render(request,"drving_sendqueries_reply.html")
@login_required(login_url='/')  
def drivingview_request(request):
    qu=DrivingRequest.objects.filter(user__Drivingschool_id=request.session['drivingschool_id'])
    return render(request,"drivingview_request.html",{'qu':qu})
@login_required(login_url='/')  
def drivingaccept_req(request,id):
    qu=DrivingRequest.objects.get(driving_request_id=id)
    if request.method=='POST':
        amt=request.POST['amt']
        qu.amount=amt
        qu.status='accept'
        qu.save()
        return HttpResponse("<script>alert(' Accepted Successfully ');window.location='/drivingview_request';</script>")

    return render(request,"drivingaccept_req.html",{'qu':qu})
@login_required(login_url='/')  
def drivingreject_req(request,id):
    qu=DrivingRequest.objects.get(driving_request_id=id)
    qu.status='reject'
    qu.save()
    return HttpResponse("<script>alert(' Rejected Successfully ');window.location='/drivingview_request';</script>")
@login_required(login_url='/')  
def drivingassign_trainer(request,oid):
    v=Trainer.objects.filter(drivingschool_id=request.session['drivingschool_id'])
    return render(request,'drivingassign_trainer.html',{'v':v,'oid':oid})
@login_required(login_url='/')  
def drivingassign(request,id,oid):
    c=AssignedTrainer(date=date.today(),status='assigned',trainer_id=id,user_id=request.session['user_id'])
    c.save()
    v=DrivingRequest.objects.get(driving_request_id=oid)
    v.status='assigned'
    v.save()
    return HttpResponse("<script>alert('Assigned ....!!!');window.location='/drivingview_request';</script>")

@login_required(login_url='/')  
def drivingview_lrequest(request):
    qu=LicenseRequest.objects.filter(user__Drivingschool_id=request.session['drivingschool_id'])
    return render(request,"drivingview_lrequest.html",{'qu':qu})
@login_required(login_url='/')  
def drivingaccept_lreq(request,id):
    qu=LicenseRequest.objects.get(license_request_id=id)
    if request.method=='POST':
        amt=request.POST['amt']
        qu.amount=amt
        qu.status='accept'
        qu.save()
        return HttpResponse("<script>alert(' Accepted Successfully ');window.location='/drivingview_lrequest';</script>")

    return render(request,"drivingaccept_req.html",{'qu':qu})
@login_required(login_url='/')  
def drivingreject_lreq(request,id):
    qu=LicenseRequest.objects.get(license_request_id=id)
    qu.status='reject'
    qu.save()
    return HttpResponse("<script>alert(' Rejected Successfully ');window.location='/drivingview_lrequest';</script>")






########################################Trainer###############################
@login_required(login_url='/')  
def trainerhome(request):
    return render(request,"trainer_home.html")

@login_required(login_url='/')  
def managetutorial(request):
    if request.method=='POST':

        Tutorials=request.FILES['tut']
        Type=request.POST['type']
    
        fs= FileSystemStorage()
        image=fs.save(Tutorials.name,Tutorials)

        
        pro=Tutorial(tutorial=image,type=Type,date=date.today(),trainer_id=request.session['trainer_id'])
        pro.save()
        return HttpResponse("<script>alert('ADD Successfully');window.location='/managetutorial';</script>")


     
    tt=Tutorial.objects.filter(trainer_id=request.session['trainer_id'])

    return render(request,"trainer_manage_tutorial.html",{'tt':tt})

@login_required(login_url='/')  
def deletetutorial(request,id):
    tt=Tutorial.objects.get(tutorial_id=id)
    tt.delete()
    return HttpResponse("<script>alert('Delete Successfully');window.location='/managetutorial';</script>")


@login_required(login_url='/')  
def viewassignedusers(request):
    ast=AssignedTrainer.objects.filter(trainer_id=request.session['trainer_id'])
    return render(request,"trainer_view_assigned_users.html",{'ast':ast})
@login_required(login_url='/')  
def trainerupdatestatus(request,id):
    obj=AssignedTrainer.objects.get(assigned_id=id)

    if request.method=='POST':
        staus=request.POST['stt']
        obj.status=staus
        obj.save()
        return HttpResponse("<script>alert('Update Successfully');window.location='/viewassignedusers';</script>")


    return render(request,"trainer_update_status.html")

from django.shortcuts import render, redirect
from .models import Trainer, chats
@login_required(login_url='/')  
def trainerchatwith_user(request, pid):
    photographer = User.objects.get(login_id=pid)
    pname = photographer.fname

    view = chats.objects.filter(sender=request.session['loginid'], receiver=pid) | chats.objects.filter(sender=pid, receiver=request.session['loginid']).order_by('date_time')

    if request.method == 'POST':
        msg = request.POST.get('msg')
        chat_instance = chats(sender=request.session['loginid'], sender_type='trainer', receiver=pid, reciver_type='user', message=msg,date_time=date.today())
        chat_instance.save()
      
        return HttpResponseRedirect("/trainerchatwith_user/%s"%pid)


    return render(request, 'trainerchatwith_user.html', {'cht': view, 'dname': pname})


###########################################User#############################
@login_required(login_url='/')  
def userhome(request):
    return render(request,"user_home.html")


@login_required(login_url='/')  
def user_send_complaint(request):
    if request.method=='POST':
        compl=request.POST['comp']


        pro=Complaint(complaint=compl,reply_text='pending',date=date.today(),user_id=request.session['user_id'])
        pro.save()
        return HttpResponse("<script>alert('ADD Successfully');window.location='/user_send_complaint';</script>")


    
    comp=Complaint.objects.filter(user_id=request.session['user_id'])

    return render(request,"user_send_complaint.html",{'obj':comp})


@login_required(login_url='/')  
def user_view_tutorial(request):
    # Get the currently logged-in user
    current_user = request.session['user_id']

    # Filter AssignedTrainer to get the trainer assigned to the current user
    assigned_trainer = AssignedTrainer.objects.filter(user=current_user)

    # Extract trainer IDs assigned to the current user
    trainer_ids = assigned_trainer.values_list('trainer_id', flat=True)

    # Filter Tutorial objects based on trainer IDs
    tutorials = Tutorial.objects.filter(trainer_id__in=trainer_ids)

    return render(request, 'user_view_tutorial.html', {'obj': tutorials})



@login_required(login_url='/')  
def user_view_drivingschool(request):
    obj=User.objects.get(user_id=request.session['user_id'])
    return render(request,'user_view_drivingschool.html',{'obj':obj})
@login_required(login_url='/')  
def user_send_driving_req(request):
    obj=Categories.objects.all()
    v=DrivingRequest.objects.filter(user_id=request.session['user_id'])
    if request.method=='POST':
        cat=request.POST['cat']
        cm=DrivingRequest(category_id=cat,amount='pending',date=date.today(),status='pending',user_id=request.session['user_id'])
        cm.save()

    return render(request,'user_send_driving_req.html',{'obj':obj,'v':v})
@login_required(login_url='/')  
def usermake_payment(request,oid,total):
    v=DrivingRequest.objects.get(driving_request_id=oid)
    if request.method == "POST":
        q =Payment(type='driving',amount=total, date=date.today(), request_id=oid)
        q.save()

        v.status = 'paid'
        v.save()    
        return HttpResponse("<script>alert('Payment Completed....!!!');window.location='/userhome';</script>")
    
    return render(request, 'customer_payment.html', {'total': total})
@login_required(login_url='/')  
def userview_invoice(request,id,amt):
    cdate=date.today
    b=DrivingRequest.objects.get(driving_request_id=id)
    return render(request,'userview_invoice.html',{'b':b,'cdate':cdate,'amt':amt})

@login_required(login_url='/')  
def user_send_license_req(request):
    obj=Categories.objects.all()
    v=LicenseRequest.objects.filter(user_id=request.session['user_id'])
    if request.method=='POST':
        cat=request.POST['cat']
        cm=LicenseRequest(category_id=cat,amount='pending',date=date.today(),status='pending',user_id=request.session['user_id'])
        cm.save()

    return render(request,'user_send_license_req.html',{'obj':obj,'v':v})
@login_required(login_url='/')  
def user_makepayment(request,oid,total):
    v=LicenseRequest.objects.get(license_request_id=oid)
    if request.method == "POST":
        q =Payment(type='licence',amount=total, date=date.today(),request_id='1000')
        q.save()

        v.status = 'paid'
        v.save()    
        return HttpResponse("<script>alert('Payment Completed....!!!');window.location='/userhome';</script>")
    
    return render(request, 'customer_payment.html', {'total': total})
@login_required(login_url='/')  
def userviewl_invoice(request,id,amt):
    cdate=date.today
    b=LicenseRequest.objects.get(license_request_id=id)
    return render(request,'userviewl_invoice.html',{'b':b,'cdate':cdate,'amt':amt})
@login_required(login_url='/')  
def userview_trainer(request):
    th=AssignedTrainer.objects.filter(user_id=request.session['user_id'])
    
    return render(request, 'userview_trainer.html', {'th': th})



from django.shortcuts import render, redirect
from .models import Trainer, chats
@login_required(login_url='/')  
def userchatwith_trainer(request, pid):
    photographer = Trainer.objects.get(login_id=pid)
    pname = photographer.fname

    view = chats.objects.filter(sender=request.session['loginid'], receiver=pid) | chats.objects.filter(sender=pid, receiver=request.session['loginid']).order_by('date_time')

    if request.method == 'POST':
        msg = request.POST.get('msg')
        chat_instance = chats(sender=request.session['loginid'], sender_type='user', receiver=pid, reciver_type='trainer', message=msg,date_time=date.today())
        chat_instance.save()
      
        return HttpResponseRedirect("/userchatwith_trainer/%s"%pid)


    return render(request, 'userchatwith_trainer.html', {'cht': view, 'dname': pname})


@login_required(login_url='/')  
def trainer_send_queries(request):
    t=Trainer.objects.get(trainer_id=request.session['trainer_id'])
    did=t.drivingschool_id
    obj=Queries.objects.filter(trainer_id=request.session['trainer_id'])
    if request.method=='POST':
        compl=request.POST['comp']


        pro=Queries(message=compl,reply='pending',date=date.today(),trainer_id=request.session['trainer_id'],drivingschool_id=did)
        pro.save()
        return HttpResponse("<script>alert('ADD Successfully');window.location='/trainer_send_queries';</script>")


    

    return render(request,"trainer_send_queries.html",{'obj':obj})
@login_required(login_url='/')  
def driving_viewuser(request):
    v=User.objects.filter(Drivingschool_id=request.session['drivingschool_id'])
    return render(request,"driving_viewuser.html",{"v":v})