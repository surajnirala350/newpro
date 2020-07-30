from django.contrib import messages
from django.shortcuts import render, redirect
from Ac_Admin.models import Department_Table
from Ac_Citizen.models import Citizen_Table, Complaint_Table, Feedback_Table, Reply_Table
from Ac_Ngo.models import Suggestion_Table


# Citizen Registration view
def citizen_registration(request):
    if request.method == 'POST':
       name = request.POST.get('name')
       mobile = request.POST.get('mobile')
       email = request.POST.get('email')
       address = request.POST.get('address')
       gender = request.POST.get('gender')
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
           Citizen_Table(
               name=name, mobile=mobile, email=email,
               address=address, gender=gender,
               username=username, password=password,otp=otp,status='pending').save()
           return render(request,'ac_citizen/citizen_otp_check.html',{'message':'Please enter your OTP'})
       else:
           return render(request,'ac_citizen/citizen_register.html',{'message':'Please Enter valid mobile Number'})
    else:
        return render(request, 'ac_citizen/citizen_register.html')


# SMS SEND FUNCTION for otp
def send_otp(mobile,otp):
    import requests
    url = "https://www.fast2sms.com/dev/bulk"
    payload = "sender_id=FSTSMS&message=Your One Time Password to Register : "+otp+"&language=english&route=p&numbers="+mobile
    headers = {
        'authorization': "SKkl50OiwzhVNtCWg9uBsUqRdGIfFbm3exaAocBz1rAaU9iQOYmnk6bq3TdRNZp58JF",
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
    message = "Dear Citizen, You have successfully registered for Active City Administration Application"
    payload = "sender_id=FSTSMS&message="+message+"&language=english&route=p&numbers="+mobile
    headers = {
        'authorization': "SKkl50OY2wzhVNtCWg9uBsUqRdGIfFbm3exaAocBz1rAaU9iQOYmnk6bq3TdRNZp58JF",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    # requests.post(url,data=payload,headers=headers)
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)
    return response


# otp confirmation
def citizen_otp_check(request):
    if request.method == "POST":
        otp = request.POST.get("otp")
        mobile = request.POST.get("cno")
        qs = Citizen_Table.objects.filter(mobile=mobile,otp=otp)
        print(qs)
        if qs:
            Citizen_Table.objects.filter(mobile=mobile).update(status='active')
            ACASMS(mobile)
            messages.error(request,"OTP is Valid")
            return redirect('citizen_login')
        else:
            messages.error(request, "Invalid OTP")
            return redirect('citizen_otp_check')
    else:
        return render(request, 'ac_citizen/citizen_otp_check.html', {'message': "Invalid OTP"})


# citizen login view
citzen_id = None
def citizen_login(request):
    ct_username = request.POST.get('username')
    ct_password = request.POST.get('password')
    qs = Citizen_Table.objects.filter(username=ct_username, password=ct_password)
    if qs:
        global citzen_id
        citzen_id = qs[0].citz_id
        request.session['username'] = ct_username
        request.session['citzen_id'] = citzen_id
        if qs[0].status == 'active':
            return render(request, 'ac_citizen/citizen_index.html',{'info':qs})
        else:
            messages.error(request, "Please Validate Your OTP")
            return redirect('citizen_login')
    else:
        messages.error(request, 'Invalid Citizen Login')
        return redirect('citizen_login')


qs1 = Department_Table.objects.all()
qs2 = Citizen_Table.objects.all()


# Complaints Views
def complaints_view(request):
    try:
        username = request.session['username']
        if request.method == 'POST':
            dept_name = request.POST.get('dept_name')
            citz_id = request.POST.get('citz_id')
            message = request.POST.get('message')
            image = request.FILES['image']
            status = 'pending'
            Complaint_Table(
                dept_name_id=dept_name, citz_id_id=citz_id,
                message=message, image=image, status=status,
            ).save()
            messages.success(request, 'Complaint Send Successfully')
            return render(request, 'ac_citizen/complaints.html/', {'data1': qs1, 'data2': citz_id})
        else:
            return render(request, 'ac_citizen/complaints.html/', {'data1': qs1, 'data2': citzen_id})
    except KeyError:
        return redirect('citizen_login')


# view_complaints_status
def view_complaints_status(request):
    try:
        username = request.session['username']
        id = request.GET.get('id')
        qs = Complaint_Table.objects.filter(citz_id_id=id)
        return render(request,'ac_citizen/citizen_complaints_index.html',{'cmplist':qs})
    except KeyError:
        return redirect('citizen_login')


# Display complaints
def complaints_list(request):
    try:
        username = request.session['username']
        qs = Complaint_Table.objects.all()
        cmp_name = request.GET.get('cmp_name')
        if cmp_name == 'admin':
            return render(request, 'ac_admin/admin_complaint_index.html', {'data':qs})
        else:
            return render(request, 'ac_officer/officer_complaints_index.html', {'data':qs})
    except KeyError:
        return redirect('citizen_login')


# Delete Complaints
def delete_complaints(request):
    try:
        username = request.session['username']
        del_id = request.POST.get('del_id')
        qs = Complaint_Table.objects.filter(comp_id=del_id)
        if qs:
            qs.delete()
            return redirect('complaints_list')
        else:
            return redirect('complaints_list')
    except KeyError:
        return redirect('admin_login')


# Feedback view
def feedback_view(request):
    try:
        username = request.session['username']
        if request.method == 'POST':
            dept_name = request.POST.get('dept_name')
            citz_id = request.POST.get('citz_id')
            fmessage = request.POST.get('fmessage')
            image = request.FILES['image']
            Feedback_Table(
                dept_name_id=dept_name, citz_id_id=citz_id,
                feed_message=fmessage, image=image,
            ).save()
            messages.success(request, 'Feedback Send Successfully')
            return redirect('feedback')
        else:
            return render(request, 'ac_citizen/feedback.html', {'data1': qs1, 'data2': citzen_id})
    except KeyError:
        return redirect('citizen_login')


# Display Feedbacks
def feedbacks_list(request):
    try:
        username = request.session['username']
        id = request.GET.get('id')
        qs = Feedback_Table.objects.filter(citz_id_id=id)
        return render(request, 'ac_citizen/feedback_list.html', {'data': qs})
    except KeyError:
        return redirect('citizen_login')


# Replay list
def citizen_replay_list(request):
    try:
        username = request.session['username']
        id = request.GET.get('id')
        list = Reply_Table.objects.filter(feed_id_id=id)
        return render(request,'ac_citizen/citizen_replay_list.html',{'list':list})
    except KeyError:
        return redirect('citizen_login')


# Suggestions View
def citizen_suggestion_view(request):
    qs1 = Department_Table.objects.all()
    if request.method == 'POST':
        dept_name = request.POST.get('dept_name')
        sug_message = request.POST.get('sug_message')
        Suggestion_Table(
            dept_name_id=dept_name,message=sug_message,).save()
        return render(request, 'ac_citizen/citizen_suggestions.html', {'data1':qs1})
    else:
        return render(request, 'ac_citizen/citizen_suggestions.html', {'data1':qs1})


# citizen_logout
def citizen_logout(request):
    try:
        del request.session['username']
        del request.session['citzen_id']
        request.session.modified = True
    except:
        return redirect('citizen_login')
    return redirect('citizen_login')