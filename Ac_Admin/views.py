from django.contrib import messages
from django.shortcuts import render, redirect
from Ac_Admin.models import Admin_Table, Department_Table, Contact_Us
from Ac_Citizen.models import Complaint_Table, Feedback_Table, Reply_Table
from Ac_Ngo.models import Suggestion_Table, Article_Table


# Admin Login View
def admin_login_check(request):
    try:
        username = request.POST.get('admin_username')
        password = request.POST.get('admin_password')
        qs = Admin_Table.objects.filter(username=username, password=password)
        if qs:
            request.session['username'] = username
            return render(request, 'ac_admin/admin_index.html', {'info': qs})
        else:
            messages.error(request, 'Invalid Admin Login')
            return redirect('admin_login')
    except ValueError:
        return redirect('admin_login')


# admin home
def admin_home(request):
    try:
        username = request.session['username']
        return render(request,'ac_admin/admin_index.html')
    except KeyError:
        return redirect('admin_login')


# Add Department View
def add_department(request):
    try:
        username = request.session['username']
        qs = Department_Table.objects.all()
        if request.method == 'POST':
            dept_name = request.POST.get('dept_name')
            Department_Table(dept_name=dept_name).save()
            messages.success(request, 'Department Add Successfully')
            return redirect('admin_add_department')
        else:
            return render(request, 'ac_admin/department_index.html', {'data': qs})
    except KeyError:
        return redirect('admin_login')


# Update Department
def update_department(request):
    try:
        username = request.session['username']
        qs1 = Department_Table.objects.all()
        up_id = request.GET.get('name')
        qs = Department_Table.objects.filter(dept_name=up_id)
        if request.method == 'POST':
            old_name = request.POST.get('dept_name')
            new_name = request.POST.get('dept_name1')
            Department_Table.objects.filter(dept_name=old_name).update(dept_name=new_name)
            return render(request, 'ac_admin/department_index.html', {'data': qs1, 'upmessage': 'Department is Updated'})
        else:
            return render(request, 'ac_admin/department_index.html', {'up_id': qs, 'data': qs1})
    except KeyError:
        return redirect('admin_login')


# Delete Department
def delete_department(request):
    try:
        username = request.session['username']
        del_id = request.GET.get('name')
        qs = Department_Table.objects.filter(dept_name=del_id)
        if qs:
            qs.delete()
            qs1 = Department_Table.objects.all()
            return render(request, 'ac_admin/department_index.html', {'data': qs1, 'message': "Department is deleted"})
        return redirect('admin_add_department')
    except KeyError:
        return redirect('admin_login')


# admin logout view
def logout_view(request):
    try:
       del request.session['username']
       request.session.modified = True
    except:
        return redirect('admin_login')
    return redirect('admin_login')


# complaints list
def admin_complaints_list(request):
    try:
        username = request.session['username']
        return render(request,'ac_admin/admin_complaint_index.html')
    except KeyError:
        return redirect('admin_login')


# Admin pending complaints
def admin_pending_complaints(request):
    try:
        username = request.session['username']
        qs = Complaint_Table.objects.filter(status='pending')
        return render(request,'ac_admin/admin_pending_complaints.html',{'object_list':qs})
    except KeyError:
        return redirect('admin_login')


# Admin Assigned complaints
def admin_assigned_complaints(request):
    try:
        username = request.session['username']
        qs = Complaint_Table.objects.filter(status='assigned')
        return render(request,'ac_admin/assigned_complaints.html',{'object_list':qs})
    except KeyError:
        return redirect('admin_login')


# Admin Closed complaints
def admin_closed_complaints(request):
    try:
        username = request.session['username']
        qs = Complaint_Table.objects.filter(status='closed')
        return render(request,'ac_admin/closed_complaints.html',{'object_list':qs})
    except KeyError:
        return redirect('admin_login')


# Complaints Assign to officer
def complaints_assign(request):
    try:
        username = request.session['username']
        dept = request.GET.get('dept')
        qs1 = Complaint_Table.objects.filter(dept_name_id=dept)
        if qs1:
            Complaint_Table.objects.filter(dept_name_id=dept).update(status='assigned')
            return redirect('admin_pending_complaints')
        else:
            return render(request, 'ac_admin/admin_pending_complaints.html')
    except KeyError:
        return redirect('admin_login')


# Display Feedbacks
def admin_feedbacks_list(request):
    try:
        username = request.session['username']
        qs = Feedback_Table.objects.all()
        return render(request, 'ac_admin/admin_feedback_list.html', {'data':qs})
    except KeyError:
        return redirect('admin_login')


# feedbsck replay
def admin_feedback_replay(request):
    try:
        username = request.session['username']
        qs1 = request.GET.get('id')
        if request.method == 'POST':
            feed_id = request.POST.get('feed_id')
            message = request.POST.get('rep_message')
            Reply_Table(feed_id_id=feed_id, message=message).save()
            return render(request, 'ac_admin/admin_feedbacks_replay.html',
                          {'data': qs1, 'rep_message': 'Replay send successfully'})
        else:
            return render(request, 'ac_admin/admin_feedbacks_replay.html', {'data': qs1})
    except KeyError:
        return redirect('admin_login')


# Delete Feedbaacks
def delete_feedbacks(request):
    try:
        username = request.session['username']
        del_id = request.GET.get('id')
        qs = Feedback_Table.objects.filter(feed_id=del_id)
        if qs:
            qs.delete()
            return redirect('admin_feedback_list')
        else:
            return redirect('admin_feedback_list')
    except KeyError:
        return redirect('admin_login')


# admin_suggestions_list
def admin_suggestions_list(request):
    try:
        username = request.session['username']
        qs = Suggestion_Table.objects.all()
        return render(request,'ac_admin/admin_suggestions_list.html',{'list':qs})
    except KeyError:
        return redirect('admin_login')


# Contact Us view
def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        message = request.POST.get('message')
        Contact_Us(
            name=name,email=email,mobile=mobile,message=message,).save()
        return render(request,'ac_admin/contact_us.html',{'cmessage':'message send successfully'})
    else:
        return render(request,'ac_admin/contact_us.html')


# Notifications about contact us
def notification_list(request):
    try:
        username = request.session['username']
        qs = Contact_Us.objects.all()
        return render(request,'ac_admin/contact_us_list.html',{'list':qs})
    except KeyError:
        return redirect('admin_login')


# delete_notification
def delete_notification(request):
    try:
        username = request.session['username']
        id = request.GET.get('id')
        qs = Contact_Us.objects.get(email=id)
        qs.delete()
        messages.success(request,'Notification Deleted')
        return render(request,'ac_admin/contact_us_list.html')
    except KeyError:
        return redirect('admin_login')


# Display feedbacks on main index
def display_feedbacks(request):
    qs1 = Feedback_Table.objects.all()
    qs2 = Article_Table.objects.all()
    return render(request,'main_index.html',{'feed_list':qs1,'art_list':qs2})