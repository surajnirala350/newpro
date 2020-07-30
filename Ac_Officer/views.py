from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from Ac_Admin.models import Department_Table
from Ac_Citizen.models import Complaint_Table
from Ac_Ngo.models import Suggestion_Table
from Ac_Officer.models import Officer_Table


# officer home
def officer_home(request):
    try:
        username = request.session['username']
        return render(request,'ac_officer/officer_index.html')
    except KeyError:
        return redirect('officer_login')


# Officer register view
def officer_register(request):
    try:
        username = request.session['username']
        qs = Department_Table.objects.all()
        qs2 = Officer_Table.objects.all()
        if request.method == "POST":
            name = request.POST.get('name')
            mobile = request.POST.get('mobile')
            email = request.POST.get('email')
            dept_name = request.POST.get('dept_name')
            username = request.POST.get('username')
            password = request.POST.get('password')

            one = name[0]
            two = int(mobile[0]) + int(mobile[-1])
            three = username[-3]
            four = password[3]

            otp = four + one + str(two) + three

            mess = send_otp(mobile, otp)

            import json
            d = json.loads(mess.text)
            if d['return']:
                Officer_Table(
                    name=name, mobile=mobile, email=email,dept_name_id=dept_name,otp=otp,
                    username=username, password=password,status='pendding').save()
                return render(request, 'ac_officer/officer_otp_check.html', {'message': 'Please enter your OTP'})
            else:
                return render(request, 'ac_officer/officer_otp_check.html',{'message': 'Please Enter valid mobile Number'})
            # return render(request, 'ac_officer/officer_register.html', {'data2': qs2, 'rmessage': 'Officer is registered'})
        else:
            return render(request, 'ac_officer/officer_register.html', {'data': qs, 'data2': qs2})
    except KeyError:
        return redirect('admin_login')


# SMS SEND FUNCTION for otp
def send_otp(mobile,otp):
    import requests
    url = "https://www.fast2sms.com/dev/bulk"
    payload = "sender_id=FSTSMS&message=Your One Time Password to Register : "+otp+"&language=english&route=p&numbers="+mobile
    headers = {
        'authorization': "gexNny2P3UqrvHLBsmt5Y1Rlk69EifKcwXuTSVGzDajMFWpQ4AbZGpcmNDPoRjLguUdHJkhV71n2OK4q",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)
    return response


# SMS SEND FUNCTION For success register
def ACASMS(mobile):
    import requests
    url = "https://www.fast2sms.com/dev/bulk"
    message = "Dear Officer, You have successfully registered in Active City Administration Application for Officer Post"
    payload = "sender_id=FSTSMS&message="+message+"&language=english&route=p&numbers="+mobile
    headers = {
        'authorization': "gexNny2P3UqrvHLBsmt5Y1Rlk69EifKcwXuTSVGzDajMFWpQ4AbZGpcmNDPoRjLguUdHJkhV71n2OK4q",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    # requests.post(url,data=payload,headers=headers)
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)
    return response


# otp confirmation
def officer_otp_check(request):
    if request.method == "POST":
        otp = request.POST.get("otp")
        mobile = request.POST.get("cno")
        qs = Officer_Table.objects.filter(mobile=mobile,otp=otp)
        print(qs)
        if qs:
            Officer_Table.objects.filter(mobile=mobile).update(status='active')
            ACASMS(mobile)
            messages.error(request,"OTP is Valid")
            return redirect('officer_register')
        else:
            messages.error(request, "Invalid OTP")
            return redirect('officer_otp_check')
    else:
        return render(request, 'ac_officer/officer_otp_check.html', {'message': "Invalid OTP"})


# Officer Delete View
def delete_officer(request):
    try:
        username = request.session['username']
        qs1 = Officer_Table.objects.all()
        name = request.GET.get('name')
        qs2 = Officer_Table.objects.filter(name=name)
        if qs2:
            qs2.delete()
            return render(request, 'ac_officer/officer_register.html', {'data2': qs1, 'message': 'Officer is deleted'})
        return redirect('officer_register')
    except KeyError:
        return redirect('admin_login')


# Update Officer
def update_officer(request):
    try:
        username = request.session['username']
        qs = Department_Table.objects.all()
        qs1 = Officer_Table.objects.all()
        up_name = request.GET.get('name')
        qs2 = Officer_Table.objects.filter(name=up_name)
        if request.method == 'POST':
            name = request.POST.get('name')
            new_name = request.POST.get('new_name')
            mobile = request.POST.get('mobile')
            email = request.POST.get('email')
            dept_name = request.POST.get('dept_name')
            username = request.POST.get('username')
            password = request.POST.get('password')
            Officer_Table.objects.filter(name=name).update(
                name=new_name, mobile=mobile, email=email,
                dept_name_id=dept_name, username=username, password=password, )
            return render(request, 'ac_officer/officer_register.html', {'data2': qs1, 'umessage': 'Officer is updated'})
        return render(request, 'ac_officer/officer_register.html', {'up_name': qs2, 'data': qs, 'data2': qs1})
    except KeyError:
        return redirect('admin_login')


# Officer Login check
def officer_login_check(request):
    username = request.POST.get('off_username')
    password = request.POST.get('off_password')
    qs = Officer_Table.objects.filter(username=username,password=password)
    if qs:
        dept = qs[0].dept_name_id
        request.session['username'] = username
        request.session['department'] = dept
        # username = request.session['username']
        return render(request, 'ac_officer/officer_index.html')
    else:
        messages.error(request, 'Invalid Officer Login')
        return redirect('officer_login')


# officer logout
def officer_logout(request):
    try:
       del request.session['username']
       request.session.modified = True
    except:
        return redirect('officer_login')
    return redirect('officer_login')


# officer Pending complaints
def officer_pending_complaints(request):
    try:
        username = request.session['username']
        dept = request.GET.get('name')
        # dept = request.session.get('department')
        qs = Complaint_Table.objects.filter(dept_name_id=dept,status='pending')
        return render(request,'ac_officer/officer_pending_complaints.html',{'list':qs})
    except KeyError:
        return redirect('officer_login')


# ofiicer assigned complaints
def officer_assigned_complaints(request):
    try:
        username = request.session['username']
        dept = request.session.get('department')
        qs = Complaint_Table.objects.filter(dept_name_id=dept,status='assigned')
        return render(request,'ac_officer/officer_assigned_complaints.html',{'list':qs})
    except KeyError:
        return redirect('officer_login')


# officer closed complaints list
def closed_complaints_list(request):
    try:
        username = request.session['username']
        dept = request.session.get('department')
        qs = Complaint_Table.objects.filter(dept_name_id=dept, status='closed')
        return render(request,'ac_officer/officer_closed_complaints.html',{'closedlist':qs})
    except KeyError:
        return redirect('officer_login')


# close complaints
def closed_complaint(request):
    try:
        username = request.session['username']
        cmpid = request.GET.get('cmp_id')
        import datetime
        date = datetime.datetime.today()
        date = date.date()
        print(date, 'taday')
        qs = Complaint_Table.objects.filter(comp_id=cmpid, status='assigned')
        if qs:
            qs.update(status='closed', close_date=date)
            return render(request, 'ac_officer/officer_closed_complaints.html')
        return redirect('officer_assigned_complaints')
    except KeyError:
        return redirect('officer_login')


# officer suggestions list
def officer_suggestions(request):
    try:
        username = request.session['username']
        dept = request.GET.get('name')
        qs = Suggestion_Table.objects.filter(dept_name_id=dept)
        return render(request,'ac_officer/officer_suggestion_list.html',{'list':qs})
    except KeyError:
        redirect('officer_login')