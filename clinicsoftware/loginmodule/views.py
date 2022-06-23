
from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User,auth
from django.core.mail import send_mail
from django.core.paginator import Paginator
import math, random
from django.db.models import Q
from .models import patient_detail
from .models import patient_health_detail
from .models import Patient_group
from .models import Account
from medicine.models import Medicine
from refdoc.models import RefDoc
from symptoms.models import Symptoms
from disease.models import Disease
from json import dumps
import datetime
import json as simplejson
import json
from django.http import JsonResponse
from django.db.models import Count
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.db.models.functions import ExtractMonth
from django.db.models import Q

# Create your views here.
def home(request):

    
    return render(request,'home/index.html')


def main_patient(request):
    patient=patient_detail.objects.all().order_by('-id')
    print(patient)
    paginator=Paginator(patient, 5)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    return render(request,'home/patients.html',{'patient':patient,'page_obj':page_obj})

def addpatient(request):
    return render(request,'home/addpatient.html')

def patient_details(request):

    if request.method=="POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        note = request.POST['note']
        age = request.POST['age']
        weight = request.POST['weight']
        contact = request.POST['contact']
        address = request.POST['address']
        rperson = request.POST['rperson']

        user = patient_detail( fname = fname,lname = lname,note = note,age = age, weight =  weight,contact = contact,address = address , rperson = rperson)
        user.save()

        return redirect('/patients')
    else:
        return redirect('/')


def viewdetail(request,i):
    #here i is patient id
    patient  = patient_detail.objects.get(id=i)
    return render(request,'home/particular_patient_detail.html',{'patient':patient})

def editpatientdetail(request,i):
        if request.method=="POST":
            fname = request.POST['fname']
            lname = request.POST['lname']
            note = request.POST['note']
            age = request.POST['age']
            weight = request.POST['weight']
            contact = request.POST['contact']
            address = request.POST['address']
            rperson = request.POST['rperson']

            a=patient_detail.objects.get(id = i)
            a.fname = fname
            a.lname = lname
            a.note = note
            a.age = age
            a.weight = weight
            a.contact = contact
            a.address = address
            a.rperson = rperson
            a.save()
            patient  = patient_detail.objects.get(id=i)
            return render(request,'home/particular_patient_detail.html',{'patient':patient})
        else:
            patient  = patient_detail.objects.get(id=i)
            return render(request,'home/particular_patient_edit_detail.html',{'patient':patient})


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None

def addpatient_health_details(request,i):
    patient_health = patient_detail.objects.get(id=i)
    medi=Medicine.objects.all()
    symp=Symptoms.objects.all()
    dies=Disease.objects.all()
    return render(request,'home/addpatient_health.html',{'patient':patient_health,'pid':patient_health.id,'medi':medi,'symp':symp,'dies':dies})

def patient_health_details(request,i):
    # i is pid
    if request.method=="POST":
        t1=patient_detail.objects.get(id=i)
        fname=t1.fname
        lname=t1.lname
        symptoms = request.POST.getlist('symptoms')
        diagnostic = request.POST.getlist('diagnostic')
        note = request.POST.getlist('note')
        prescription = request.POST.getlist('prescription')
        timee = request.POST.getlist('time')
        countt = request.POST.getlist('countt')
        printpres = request.POST.getlist('printpres')
        report = request.POST['report']
        fees = request.POST['fees']
        paid = request.POST['paid']
        date = datetime.date.today()
        time=datetime.datetime.now().time()
        paid_og=paid


        print(request.POST)
        print(note)
        print(prescription)
        print(timee)
        print(countt)
        print('-----------------')
        print(printpres)
        #--------------------calculation of settleing account when extra or lee money is added-------------------

        patient_all_visit_acc=patient_health_detail.objects.filter(patient_id=i)

        fees1=int(fees)
        paid1=int(paid)
        
        for j in patient_all_visit_acc:

            if fees1 > paid1:

                if j.paid > j.fees:
                
                    print('this is >')
                    a = fees1-paid1
                    b=j.paid-j.fees
                    c=a-b
                   #if c>=0:
                    print('-this is b-')
                    print(b)
                    j.paid=j.paid-b
                    print(paid1)
                    paid1 = paid1+b
                    print(paid1)
                    paid = paid1
                    
                    
                    b=patient_health_detail.objects.get(id=j.id)
                    b.paid=j.paid
                    b.left_from_doc=b.paid-b.fees
                    b.save()

            elif fees1 < paid1:
                
                if j.paid < j.fees :
                    print('this is <')
                    a= paid1 - fees1
                    b=j.fees-j.paid
                    print('-----------')
                    print(a)
                    print(b)
                    if a>=b:
                        
                        if a>b:
                            j.paid=j.paid+b
                            #a=a-b
                            print('this is a>b')
                            print(a)
                    
                            paid1=paid1-b
                            paid=paid1
                        elif a==b:
                            print('this is a==b')
                            print(a)
                            j.paid=j.paid+b
                            paid1=paid1-a
                            paid=paid1


                    elif a<b:
                        
                        print('this is a<b')
                        j.paid=j.paid+a
                        print(j.paid)
                        paid1=paid1-a
                        print(paid1)
                        paid=paid1
                   

                    b=patient_health_detail.objects.get(id=j.id)
                    b.paid=j.paid
                    b.left_from_patient=b.fees-b.paid
                    b.save()

               
        p1=patient_detail.objects.get(id=i)
        user = patient_health_detail(patient_id=p1,fname = fname,lname = lname,report=report,date=date,time=time,fees=fees,paid=paid,paid_original=paid_og)
        listIWantToStore1 = prescription
        user.prescription = json.dumps(listIWantToStore1)
        listIWantToStore2 = note
        user.note = json.dumps(listIWantToStore2)
        listIWantToStore3 = timee
        user.m_time = json.dumps(listIWantToStore3)
        listIWantToStore4 = countt
        user.countt = json.dumps(listIWantToStore4)
        symptoms1 = symptoms
        user.countt = json.dumps(listIWantToStore4)
        diagnostic1 = diagnostic
        user.countt = json.dumps(listIWantToStore4)
        user.save()
        patient = patient_detail.objects.all()


        
        return redirect('/')
        #return render(request,'home/index.html')#'home.html',{'patient':patient})
def calclulation(i,j,pid):
    if i == j:
        Account.objects.filter(patient_id = pid).update(tleft_from_patient=0,tleft_from_doc=0)
        return 0
    elif i > j:
        c=i-j
        Account.objects.filter(patient_id = pid).update(tleft_from_patient=c,tleft_from_doc=0)
        return c
    elif j > i:
        c=j-i
        Account.objects.filter(patient_id = pid).update(tleft_from_doc=c,tleft_from_patient=0)
        return c

def summary1(i,j):
    s=patient_health_detail.objects.get(id=i)
    #j is patient id and  i is visit no
    g=patient_health_detail.objects.get(id=i)
    

    pid=j
    p1=patient_detail.objects.get(id=pid)
    paid=s.paid
    fees=s.fees
    d=patient_health_detail.objects.filter(patient_id=pid)
    Total_FEES=0
    Total_PAID=0
    for g in d:
     Total_FEES=Total_FEES+g.fees
     Total_PAID=Total_PAID+g.paid
    
    try:
     t=Account.objects.get(patient_id=pid)
     if t != None:
      Account.objects.filter(patient_id = pid).update(tfees=Total_FEES,tpaid=Total_PAID)
      t=Account.objects.get(patient_id=pid)
    except:
     
     Account(patient_id=p1,tfees=Total_FEES,tpaid=Total_PAID).save()
     t=Account.objects.get(patient_id=pid)

    if fees == paid:
        calclulation(Total_FEES,Total_PAID,pid)
        s=patient_health_detail.objects.get(id=i)
        t=Account.objects.get(patient_id=pid)
        pleft=0
        dleft=0
        patient_health_detail.objects.filter(id=i).update(left_from_patient=pleft,left_from_doc=dleft)
        return 0

    elif paid < fees:
        calclulation(Total_FEES,Total_PAID,pid)
        pleft=fees-paid
        patient_health_detail.objects.filter(id=i).update(left_from_patient=pleft)
        s=patient_health_detail.objects.get(id=i)
        t=Account.objects.get(patient_id=pid)
        
        return 0
    elif paid > fees:
        calclulation(Total_FEES,Total_PAID,pid)
        dleft=paid-fees
        patient_health_detail.objects.filter(id=i).update(left_from_doc=dleft)
        s=patient_health_detail.objects.get(id=i)
        t=Account.objects.get(patient_id=pid)
        
        return 0


def visit_summary(request):
    patient = patient_detail.objects.all().order_by('-id')
    paginator=Paginator(patient, 5)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)

    for i in patient:
        particular_patient = patient_health_detail.objects.filter(patient_id=i)
        for j in particular_patient:
            summary1(j.id, i.id)

    return render(request,'home/visit_summary.html',{'patient':patient,'page_obj':page_obj})
    

def particular_person_summary(request,i):
    visit=patient_health_detail.objects.filter(patient_id=i).all()
    patient_info = patient_detail.objects.get(id=i)

    #print("-------------------------------------------------")
    #print(visit.patient_visit)
    #print("-------------------------------------------------")
    s={'patient':visit,'id':i,'patient_info':patient_info}
    return render(request,'home/particular_patient.html',s)
    

    
def summary(request,i,j):
    s=patient_health_detail.objects.get(id=i)
    #j is patient id and  i is visit no
    g=patient_health_detail.objects.get(id=i)
    jsonDec = json.decoder.JSONDecoder()
    prescription = jsonDec.decode(g.prescription)
    note = jsonDec.decode(g.note)
    m_time = jsonDec.decode(g.m_time)
    countt = jsonDec.decode(g.countt)

    prescription.pop(0)
    note.pop(0)
    m_time.pop(0)
    countt.pop(0)
    
    prescription_details = []

    for p,n,t,c in zip(prescription,note,m_time,countt):
        prescription_details.append({"p":p,"n":n,"t":t,"c":c})

    pid=j
    p1=patient_detail.objects.get(id=pid)
    paid=s.paid
    fees=s.fees
    d=patient_health_detail.objects.filter(patient_id=pid)
    Total_FEES=0
    Total_PAID=0
    for g in d:
     Total_FEES=Total_FEES+g.fees
     Total_PAID=Total_PAID+g.paid
    
    try:
     t=Account.objects.get(patient_id=pid)
     if t != None:
      Account.objects.filter(patient_id = pid).update(tfees=Total_FEES,tpaid=Total_PAID)
      t=Account.objects.get(patient_id=pid)
    except:
     
     Account(patient_id=p1,tfees=Total_FEES,tpaid=Total_PAID).save()
     t=Account.objects.get(patient_id=pid)

    if fees == paid:
        calclulation(Total_FEES,Total_PAID,pid)
        s=patient_health_detail.objects.get(id=i)
        t=Account.objects.get(patient_id=pid)
        summary={'s':s,'t':t,'prescription_details':prescription_details}
        return render(request,'home/summary.html',summary)
    elif paid < fees:
        calclulation(Total_FEES,Total_PAID,pid)
        pleft=fees-paid
        patient_health_detail.objects.filter(id=i).update(left_from_patient=pleft)
        s=patient_health_detail.objects.get(id=i)
        t=Account.objects.get(patient_id=pid)
        summary={'s':s,'t':t,'prescription_details':prescription_details}
        return render(request,'home/summary.html',summary)
    elif paid > fees:
        calclulation(Total_FEES,Total_PAID,pid)
        dleft=paid-fees
        patient_health_detail.objects.filter(id=i).update(left_from_doc=dleft)
        s=patient_health_detail.objects.get(id=i)
        t=Account.objects.get(patient_id=pid)
        summary={'s':s,'t':t,'prescription_details':prescription_details}
        return render(request,'home/summary.html',summary)



def patient_group(request): 
    
    p = patient_detail.objects.all()
    return render(request,'home/patient_group.html',{'patient':p})

def create_group(request): 
    if request.method=="POST":
        mem = request.POST.getlist('mselect')
        mem_sep = []
        for i in mem:
         mem_sep.append(i.split(":"))


        print("-------------------------------------------------")
        print(mem)
        print(mem_sep)
        print(mem_sep[0][0])
        print("-------------------------------------------------")

        gname = request.POST['gname']
        user=Patient_group(gname=gname)
        listIWantToStore = mem_sep
        user.member = json.dumps(listIWantToStore)
        user.save()
        g = Patient_group.objects.all()
        s={'group':g}
        return redirect('/all_group')
        
    else:
         p = patient_detail.objects.all()
         s={'patient':p}
         return render(request,'home/patient_group.html',s)
        
def all_group(request): 
    g = Patient_group.objects.all().order_by('id')
    paginator=Paginator(g, 5)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)    
    
    return render(request,'home/all_group.html',{'group':g,'page_obj':page_obj})


def particular_group(request,i):
    #here i is gid
    g=Patient_group.objects.get(id=i)
    jsonDec = json.decoder.JSONDecoder()
    gList = jsonDec.decode(g.member)
    mem_sep = []
    mem_sep1 = []
    
    for i in gList:
        #print("this is i")
        #print(i[0])#pid is patient id
        pid = i[0]
        advance_summ=patient_health_detail.objects.filter(patient_id=pid)
        for j in advance_summ:
            #print("this is j")
            #print(j.id)
            summary1(j.id, pid )#j.id is visit no
    
    for j in gList:
        mem_sep.append({"id":j[0],"name":j[1]})
        
    print("-------------------------------------------------")
    #print(mem_sep)
    print(mem_sep[0]["id"])
    print("-------------------------------------------------")
    Total_Group_paid=0
    Total_Group_fees=0
    Total_Group_from_patient=0
    Total_Group_from_doc=0
    
    dleft_account = []
    pleft_account = []
    #print("-------------------------------------------------")
    for i in gList:
        #print(i[0])#pid is patient id
        pid = i[0]
        #print(pid)
        #print("-------------------------------------------------")
        
        #print(i[0])#pid is patient id
        pid = i[0]
        #print(pid)
    #print("-------------------------------------------------")
        o = Account.objects.get(patient_id=pid)
        o1 = patient_detail.objects.get(id=pid)
        print(o.tfees)
        print(o1)
   
        Total_Group_paid=Total_Group_paid+o.tpaid
        Total_Group_fees=Total_Group_fees+o.tfees
        Total_Group_from_patient=Total_Group_from_patient+o.tleft_from_patient
        Total_Group_from_doc=Total_Group_from_doc+o.tleft_from_doc

        if o.tleft_from_patient != 0:
            pleft_account.append({'fname':o1.fname,'lname':o1.lname,'left':o.tleft_from_patient})
            mem_sep1.append({"id":i[0],"name":i[1],"pleft":o.tleft_from_patient,"dleft":0})
        else:
            #pleft_account.append({'fname':o1.fname,'lname':o1.lname,'left':0})

            if o.tleft_from_doc != 0:
                dleft_account.append({'fname':o1.fname,'lname':o1.lname,'left':o.tleft_from_doc}) 
                mem_sep1.append({"id":i[0],"name":i[1],"pleft":0,"dleft":o.tleft_from_doc})
            else:
                dleft_account.append({'fname':o1.fname,'lname':o1.lname,'left':0}) 
                mem_sep1.append({"id":i[0],"name":i[1],"pleft":0,"dleft":o.tleft_from_doc})
    
    print("-------------------------------------------------")
        
    p = patient_detail.objects.all()
    s={'list':mem_sep,'list1':mem_sep1,'patient':p,'tpaid':Total_Group_fees,'tfees':Total_Group_paid,'tfrom_patient':Total_Group_from_patient,'tfrom_doc':Total_Group_from_doc,'list_pleft':pleft_account,'list_dleft':dleft_account}
    return render(request,'home/particular_group.html',s)
        
        #    return render(request,'home/pageadddata.html')



def statistic(request):
    try:
        patient = patient_detail.objects.all()
        total_patient=0
        current_month_patient=0
        current_month_revenue=0
        today_patient=0
        today_revenue=0
        daily_patient_list =[]
        daily_revenue_list =[]
        date_list=[]
        temp=[]
        #-------------calulate total patient----------------
        for i in patient:
            total_patient=total_patient+1

        total_patient_month=0
        date = datetime.date.today()
        last_date=date.day
        end_date = datetime.date.today()    
        start_date = end_date - datetime.timedelta(last_date)       
        monthly_id=patient_health_detail.objects.filter(date__range=[start_date,end_date])

        #---------------------calculate current month patient revenue---------
        for i in monthly_id:
        #print(i.id)
        #print(i.fees)
            current_month_patient=current_month_patient+1
            current_month_revenue=current_month_revenue+i.fees
            temp.append(str(i.date.day))
        #--------------------calculate today patient and revenue----------------
        for i in temp:
            if i not in date_list:
                date_list.append(i)

        today_patient_object=patient_health_detail.objects.filter(date=date)
        for i in today_patient_object:
            today_patient=today_patient+1
            today_revenue=today_revenue+i.fees
        date_temp=0
    #-------------------------------------------calculate daily revenue and patient-----------------------------
        for i in monthly_id:
            daily_patient=0
            daily_revenue=0
            
            if date_temp == i.date: # to ignore same date as there are many enrty on one day
                continue
            else:
                date_temp=i.date
                particular_date_object=patient_health_detail.objects.filter(date=i.date)

                for j in particular_date_object:
                    daily_patient=daily_patient+1
                    daily_revenue=daily_revenue+j.fees

                daily_patient_list.append({"date":i.date.day,"patient":daily_patient})
                daily_revenue_list.append({"date":i.date.day,"revenue":daily_revenue})
                
                daily_patient_list1=[]
                daily_revenue_list1=[]
                k=0
                j=0
                for i in range(1, 32, 1):
                    
                    if daily_patient_list[k]["date"] == i:
                        a=daily_patient_list[k]["patient"]
                        daily_patient_list1.append(a)
                        k=k+1
                        if k>=len(daily_patient_list):
                            break
                    else:
                        daily_patient_list1.append(0)
                
                k=0
                j=0
                for i in range(1, 32, 1):
                    if j>=len(daily_revenue_list):
                        break
                    if daily_revenue_list[j]["date"] == i:
                        b=daily_revenue_list[j]["revenue"]
                        daily_revenue_list1.append(b)
                        j=j+1
                        
                    else:
                        daily_revenue_list1.append(0)
                        


                    # print('--this is daily patient---')
                    # print(daily_patient_list1)
                    # print(daily_revenue_list1)
                    # print('--this is daily patient abc---')
                    # print(daily_patient_list)
                    # print(daily_revenue_list)

                daily_patient_list_data = {'daily_patient_list':daily_patient_list1}      
                daily_revenue_list_data =  {'daily_revenue_list':daily_revenue_list1}    
                daily_patient_listJSON = dumps(daily_patient_list_data)
                daily_revenue_listJSON = dumps(daily_revenue_list_data)

    #-----------------------------------------------calculate monthly revenue and patient-------------------------------
        monthly_revenue_list=patient_health_detail.objects.annotate(month=TruncMonth('date')).values('month').annotate(total_revenue=Sum('fees')).order_by('month').annotate(extract_month=ExtractMonth('month'))
        monthly_patient_list=patient_health_detail.objects.annotate(month=TruncMonth('date')).values('month').annotate(total_patient=Count('id')).order_by('month').annotate(extract_month=ExtractMonth('month'))
        # print("---------------this is j------------------")
        # for j in monthly_revenue_list:
        #     print(j)
        # print("---------------this is j------------------")
        # for j in monthly_patient_list:
        #     print(j["extract_month"])

        monthly_patient_list2=[]
        monthly_revenue_list2=[]

        for j in monthly_patient_list:
            monthly_patient_list2.append({'month':j["extract_month"],'patient':j["total_patient"]})
        j=0
        for j in monthly_revenue_list:
            monthly_revenue_list2.append({'month':j["extract_month"],'revenue':j["total_revenue"]})

        # print("---------------this is lentgh------------------")
        # print(len(monthly_revenue_list2))
        print("---------------this is ------------------")
        print(monthly_patient_list2)
        print(monthly_revenue_list2)

        monthly_patient_list1=[]
        monthly_revenue_list1=[]

        k=0
        for i in range(1, 13, 1):
            if k>=len(monthly_patient_list2):
                
                break 
            if monthly_patient_list2[k]["month"] == i:
                
                a=monthly_patient_list2[k]["patient"]
                monthly_patient_list1.append(a)
                k=k+1
            else:
                monthly_patient_list1.append(0)

        # print("---------------this is list1 ------------------")
        # print(monthly_patient_list1)
        k=0
        for i in range(1, 13, 1):
            if k>=len(monthly_revenue_list2):
                    break        
            if monthly_revenue_list2[k]["month"] == i:
                a=monthly_revenue_list2[k]["revenue"]
                monthly_revenue_list1.append(a)
                k=k+1
            else:
                monthly_revenue_list1.append(0)

        monthly_patient_list_data = {'monthly_patient_list':monthly_patient_list1}      
        monthly_revenue_list_data =  {'monthly_revenue_list':monthly_revenue_list1}    
        monthly_patient_listJSON = dumps(monthly_patient_list_data)
        monthly_revenue_listJSON = dumps(monthly_revenue_list_data)

        

        


        
        print("---------------------------------")
        print(current_month_patient)
        print(current_month_revenue)
        print(total_patient)  
        print(today_patient)  
        print(today_revenue)
        
        print("-------------daily patient og--------------------")
        print(daily_patient_list)#done
        print(daily_revenue_list)#done
        print("-------------daily patient--------------------")
        print(daily_patient_list1)#done
        print(daily_revenue_list1)#done
        print("---------------------------------")
        print('--this is monthly patient---')
        print(monthly_patient_list1)
        print(monthly_revenue_list1)
        print(end_date) 
        print(start_date) 
        print(date_list)


        
        data_for_statistics={'daily_patient_list': daily_patient_listJSON,'daily_revenue_list':daily_revenue_listJSON,'monthly_patient_list':monthly_patient_listJSON,'monthly_revenue_list':monthly_revenue_listJSON,'today_patient':today_patient,'today_revenue':today_revenue,'total_patient':total_patient}
        return render(request,'home/index.html', data_for_statistics)

    except:
        today_patient=0
        today_revenue=0
        total_patient=0
        daily_patient_list1=[]
        daily_revenue_list1=[]
        monthly_patient_list1=[]
        monthly_revenue_list1=[]
        daily_patient_list_data = {'daily_patient_list':daily_patient_list1}      
        daily_revenue_list_data =  {'daily_revenue_list':daily_revenue_list1}    
        daily_patient_listJSON = dumps(daily_patient_list_data)
        daily_revenue_listJSON = dumps(daily_revenue_list_data)

        monthly_patient_list_data = {'monthly_patient_list':monthly_patient_list1}      
        monthly_revenue_list_data =  {'monthly_revenue_list':monthly_revenue_list1}    
        monthly_patient_listJSON = dumps(monthly_patient_list_data)
        monthly_revenue_listJSON = dumps(monthly_revenue_list_data)


        data_for_statistics={'daily_patient_list': daily_patient_listJSON,'daily_revenue_list':daily_revenue_listJSON,'monthly_patient_list':monthly_patient_listJSON,'monthly_revenue_list':monthly_revenue_listJSON,'today_patient':today_patient,'today_revenue':today_revenue,'total_patient':total_patient}
        return render(request,'home/index.html', data_for_statistics)
def settle_account(request,pid):
    #pid is pid
    o=patient_detail.objects.get(id=pid)
    advance_summ=patient_health_detail.objects.filter(patient_id=pid)

    for j in advance_summ:
          
            summary1(j.id,pid)

    if request.method=="POST":
        new_pamount = request.POST['new_pamount']
        new_damount = request.POST['new_damount']

        new_pamount1=int(new_pamount)
        new_damount1=int(new_damount)

        if new_damount1 and new_pamount1 > 0:
            return render(request,'home/page-500.html')

        if new_damount1 != 0:
            patient_all_visit_acc=patient_health_detail.objects.filter(patient_id=pid)

            for i in patient_all_visit_acc:
                if i.fees == i.paid:
                    pass

                elif i.left_from_doc != 0:

                    a =i.paid-i.fees
                    print('this is a')
                    print(a)

                    if new_damount1 >= a:
                        print('>=')
                        new_damount1=new_damount1-a
                        i.paid=i.paid-a
                        b=patient_health_detail.objects.get(id=i.id)
                        b.paid=i.paid
                        b.save()

                    elif new_damount1==0:
                        print('=')
                        pass

                    elif new_damount1 < a:
                       print('<=')
                       c = a-new_damount1
                       print('this is c')
                       print(c)
                       

                       #new_damount1=new_damount1-c
                       i.paid=i.paid-new_damount1
                       b=patient_health_detail.objects.get(id=i.id)
                       b.paid=i.paid
                       b.save()
                       new_damount1=0

        else:
           
            patient_all_visit_acc=patient_health_detail.objects.filter(patient_id=pid)

            for i in patient_all_visit_acc:
                if i.fees == i.paid:
                    pass

                elif i.left_from_patient != 0:

                    a =i.fees-i.paid
                    print('this is a')
                    print(a)

                    if new_pamount1 >= a:
                        print('>=')
                        new_pamount1=new_pamount1-a
                        i.paid=i.paid+a
                        b=patient_health_detail.objects.get(id=i.id)
                        b.paid=i.paid
                        b.save()
                    elif new_pamount1==0:
                        print('=')
                        pass
                    elif new_pamount1 < a:
                       print('<=')
                       c = a-new_pamount1
                       print('this is c')
                       print(c)
                       #new_pamount1=new_pamount1-c
                       i.paid=i.paid+new_pamount1
                       b=patient_health_detail.objects.get(id=i.id)
                       b.paid=i.paid
                       b.save()
                       new_pamount1=0


        advance_summ=patient_health_detail.objects.filter(patient_id=pid)
        for j in advance_summ:
          
            summary1(j.id,pid)
                 
             
        patient_account = Account.objects.get(patient_id=pid)

        return render(request,'home/particular_patient_settle_account.html',{'patient_account':patient_account,'patient':o})
    else:
        patient_account = Account.objects.get(patient_id=pid)
        
        return render(request,'home/particular_patient_settle_account.html',{'patient_account':patient_account,'patient':o})
        
def ref_doctor(request):

    if request.method == 'POST':
        doc_list = []
        query = request.POST['search1']
        name = RefDoc.objects.all().filter((Q(name__icontains = query)))
        print(name)
        for i in name:
            doc_list.append({'name':i.name,'details':i.details})
            print(i.id)
            print(i.details)
        return render(request,'home/ref_doc.html',{'doc_list':doc_list})
    else:
         return render(request,'home/ref_doc.html')

def search_patient(request):
    if request.method=='GET':
        query=request.GET.get('q')
        print(query)
        submitbutton=request.GET.get('submit')
        if query:
            lookups=Q(fname__iexact=query)|Q(lname__iexact=query)|Q(contact__iexact=query)
            results=patient_detail.objects.filter(lookups).distinct()
            print(results)
            context={'results':results,'submitbutton':submitbutton}
            template_name='home/patients.html'
            return render(request,template_name,context)
        else:
            return redirect('main_patient')
    
    else:
        return render(request, 'home/patients.html')

def search_patient_summary(request):
    if request.method=='GET':
        query=request.GET.get('q')
        print(query)
        submitbutton=request.GET.get('submit')
        if query:
            lookups=Q(fname__iexact=query)|Q(lname__iexact=query)|Q(contact__iexact=query)
            results=patient_detail.objects.filter(lookups).distinct()
            print(results)
            context={'results':results,'submitbutton':submitbutton}
            template_name='home/visit_summary.html'
            return render(request,template_name,context)
        else:
            return redirect('visit_summary')
    
    else:
        return render(request, 'home/visit_summary.html')

def search_patient_Group(request):
    if request.method=='GET':
        query=request.GET.get('q')
        print(query)
        print("search patient_group is called")
        submitbutton=request.GET.get('submit')
        if query:
            lookups=Q(gname__iexact=query)
            results=Patient_group.objects.filter(lookups).distinct()
            print(results)
            context={'results':results,'submitbutton':submitbutton}
            template_name='home/all_group.html'
            return render(request,template_name,context)
        else:
            return redirect('all_group')
    
    else:
        return render(request, template_name)
def delete_patient(request,i):
    patient=patient_detail.objects.get(id=i)
    print('================================')
    print('deleting')
    print(patient)
    patient.delete()
    print('===================================')
    return redirect('main_patient')

def delete_group(request,i):
    grp=Patient_group.objects.get(id=i)
    print(grp)
    grp.delete()
    return redirect('all_group')
