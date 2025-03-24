from django.dispatch import receiver
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .forms import *
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.http import HttpResponseRedirect
# from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login as auth_login



def home(request):
    appointments = Appointment.objects.all()
    patient_total=Patient.objects.count()
    doctor_total=Doctor.objects.count()
    appointment_total=Appointment.objects.count()
    hospital_total=Hospital.objects.count()
    return render(request, "patient/home.html", {"appointments": appointments, "patient_total":patient_total, "doctor_total":doctor_total, "appointment_total":appointment_total, "hospital_total":hospital_total})


def login(request):
    if request.user.is_authenticated:
        return redirect("patient_home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect("/home")


    return render(request, "registration/login.html")

# def redirect_based_on_role(user):
#     if user.role == 'patient':
#         return redirect("patient_home")
#     elif user.role == 'medecin':
#         return redirect("doctor_home")
#     elif user.role == 'pharmacien':
#         return redirect("pharmacist_home")
#     # Add other roles as needed
#     return redirect("default_home")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'patient'  # Set the role to patient
            user.save()
            return redirect("/home")
    else:
        form = RegisterForm()

    return render(request, "patient/register.html", {"form": form})


@login_required
def profile(request):
    user = request.user

    try:
        profile = Profile.objects.get(user=user)
        if profile.role == 'patient':
            # Check if the user is already in the Patient model
            patient, created = Patient.objects.get_or_create(user=user)

            # Check if there is an existing medical record for the patient
            dossier_medical, created = DossierMedical.objects.get_or_create(patient=patient)

            if request.method == 'POST':
                patient_form = PatientProfileForm(request.POST, instance=patient)
                if patient_form.is_valid():
                    patient_form.save()
                    return redirect('profile')
            else:
                patient_form = PatientProfileForm(instance=patient)

            dossier_form = ReadOnlyDossierMedicalForm(instance=dossier_medical)
            return render(request, 'patient/profile.html', {
                'patient_form': patient_form,
                'dossier_form': dossier_form,
                'is_patient': True,
                'dossier_medical': dossier_medical,
            })
        elif profile.role == 'doctor':
            # Check if the user is already in the Doctor model
            doctor, created = Doctor.objects.get_or_create(user=user)

            # Implement the doctor-specific logic here
            # For now, we just redirect to a placeholder page
            return render(request, 'patient/profile.html', {'user': user, 'is_doctor': True ,  'doctor':doctor})

        else:
            # For users who are not patients or doctors, display user information
            return render(request, 'patient/profile.html', {'user': user, 'is_patient': False, 'is_doctor': False})
    except Profile.DoesNotExist:
        # Handle case where profile does not exist
        return render(request, 'patient/profile.html', {'user': user, 'is_patient': False, 'is_doctor': False})


# mdofication des informations du patient 

@login_required
def Patient_profile_edit(request):
    patient = Patient.objects.filter(user=request.user).first()

    if request.method == "POST":
        patient.email = request.POST.get("email")
        patient.address = request.POST.get("address")
        patient.date_of_birth = request.POST.get("date_of_birth")
        patient.medical_history = request.POST.get("medicalHistory")
        patient.save()
        return redirect('profile')

    return render(request, 'patient/patient_profile_edit.html', {"patient": patient})

@login_required
def edit_patient_info(request, field):
    patient = Patient.objects.get(user=request.user)
    # form_class = dynamic_Patient_form(field)  # Get the dynamic form class
    class DynamicPatientForm(EditPatientFieldForm):
        class Meta(EditPatientFieldForm.Meta):
            fields = [field]

    form = DynamicPatientForm(instance=patient)
    if request.method == 'POST':
        form = DynamicPatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('profile')

    return render(request, 'patient/edit_patient_field.html', {
        'form': form,
        'field': field
    })

# modification des informations du médecin    

@login_required
def doctor_profile_edit(request):
    doctor = Doctor.objects.filter(user=request.user).first()

    if request.method == "POST":
        doctor.name = request.POST.get("name")
        doctor.gender = request.POST.get("gender")
        doctor.specialization = request.POST.get("specialization")
        doctor.license_number = request.POST.get("license_number")
        doctor.contact_number = request.POST.get("contact_number")
        doctor.bio = request.POST.get("bio")
        doctor.save()
        return redirect('doctor_profile')

    return render(request, 'patient/edit_doctor_profile.html', {"doctor": doctor})
     
    
@login_required
def edit_doctor_info(request, field):
    doctor = Doctor.objects.get(user=request.user)

    class DynamicDoctorForm(EditDoctorFieldForm):
        class Meta(EditDoctorFieldForm.Meta):
            fields = [field]

    form = DynamicDoctorForm(instance=doctor)

    if request.method == 'POST':
        form = DynamicDoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('profile')

    return render(request, 'patient/edit_doctor_field.html', {
        'form': form,
        'field': field
    })

# modification de la photo

@login_required
def update_profile_photo(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfilePhotoForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfilePhotoForm(instance=profile)
    return render(request, 'patient/update_photo.html', {'form': form})


# réserver un rdv 

@login_required
def book_appointment(request):
    user = request.user
    try:
        patient = Patient.objects.get(user=user)
    except Patient.DoesNotExist:
        return redirect('profile')  # Redirect to profile if the user is not a patient

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.statut = 'en_attente'
            appointment.save()
            return redirect('patient_appointments')
    else:
        form = AppointmentForm()

    return render(request, 'patient/book_appointment.html', {'form': form})


@login_required
def patient_appointments(request):
    user = request.user
    try:
        patient = Patient.objects.get(user=user)
    except Patient.DoesNotExist:
        return redirect('profile')  # Redirige vers le profil si l'utilisateur n'est pas un patient

    appointments = Appointment.objects.filter(patient=patient).order_by('-start_datetime')
    return render(request, 'patient/appointments.html', {'appointments': appointments})













def patientinformation(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        email = request.POST.get("email")
        if Patient.objects.filter(email = email).exists():
            form = PatientForm()
            messages.error(request,".")
        else:
            if form.is_valid():
                form.save()
            return redirect("/patientlist")
    else:
        form = PatientForm()

    return render(request, "patient/patient.html", {"form":form})

@login_required
def patientlist(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        name = request.POST.get("name")
        email = request.POST.get("email")

        # if Patient.objects.filter(email = email, name = name).exists():
        #     print("pa")
        #     messages.error(request,".")

        # elif Patient.objects.filter(email = email).exists():
        #     messages.warning(request,".")

        if form.is_valid():
            form.save()
    else:
        form = PatientForm()
        information = Patient.objects.all()
        return render(request, "patient/patientlist.html",{"information":information, "form":form})

@login_required

def doctorinformation(request):
    if request.method == "POST":
        form = DoctorForm(request.POST)
        license_number = request.POST.get("license_number")
        if Doctor.objects.filter(license_number = license_number).exists():
            messages.error(request,"License number is already taken")

        username = request.POST.get("username")
        if Doctor.objects.filter(username = username).exists():
            messages.error(request,"username is already taken")
            
        else:
            if form.is_valid():
                form.save()
            return redirect("/doctorlist")
    else:
        form = DoctorForm()

    return render(request, "patient/doctorinformation.html", {"form":form})


@login_required
    
def doctorlist(request):
    if request.method == "POST":
        form = DoctorForm(request.POST, instance=image)
        # name = request.POST.get('name')
        # specialization = request.POST.get('specialization')
        # contact_number = request.POST.get('contact_number')
        # license_number = request.POST.get('license_number')
        # if Doctor.objects.filter(name = name, specialization = specialization, contact_number = contact_number, license_number = license_number).exists():
        #     messages.error(request,"Fields already in the Table")
        if form.is_valid():
            form.save()
    else:
        form = DoctorForm()
    information = Doctor.objects.all()
    return render(request, "patient/doctorlist.html", {"information":information, "form":form})
    
    


def doctor_delete(request, pk):
    pk = pk
    try:
        image_sel = Doctor.objects.get(pk = pk)
    except Doctor.DoesNotExist:
        return redirect('doctorlist')
    image_sel.delete()
    return redirect('doctorlist')


def patient_delete(request, pk):
    pk = pk
    try:
        image_sel = Patient.objects.get(pk = pk)
    except Patient.DoesNotExist:
        return redirect('patientlist')
    image_sel.delete()
    return redirect('patientlist')

class  PatientUpdate(View):
    def  post(self, request, pk):
        data =  dict()
        patient = Patient.objects.get(pk=pk)

        form = PatientForm(instance=patient, data=request.POST)

        name = request.POST.get('name')
        email = request.POST.get('email')

        if Patient.objects.filter(name = name).exists() or Patient.objects.filter(email = email).exists():
            print("PatientUpdate2")
            # messages.error(request,"Inputs already in the table")
            error_msg = "Inputs already exist"
            title = "Update Error"
            error_var = True
            information = Patient.objects.all()
            return render(request, "patient/patientlist.html",{"information":information, "error_msg":error_msg, "title":title,"error_var":error_var })
            
        else:           
            if form.is_valid():
                patient = form.save()
            
        information = Patient.objects.all()
        return render(request, "patient/patientlist.html",{"information":information})
        


class  DoctorUpdate(View):

    def  post(self, request, pk):
        data =  dict()
        doctor = Doctor.objects.get(pk=pk)
        form = DoctorForm(instance=doctor, data=request.POST)
        # name = request.POST.get('name')
        # specialization = request.POST.get('specialization')
        # contact_number = request.POST.get('contact_number')
        # license_number = request.POST.get('license_number')
        # if Doctor.objects.filter(name = name, specialization = specialization, contact_number = contact_number, license_number = license_number).exists():
        #     form = DoctorForm()
        #     messages.error(request,"Already in the Table")

        # elif Doctor.objects.filter(license_number = license_number).exists():
        #     form = DoctorForm()
        #     messages.error(request,"License number already exists")
        if form.is_valid():
            form = form.save()
            
        information = Doctor.objects.all()
        return render(request, "patient/doctorlist.html",{"information":information, "form":form})  

class  HospitalUpdate(View):

    def  post(self, request, pk):
        data =  dict()
        hospital = Hospital.objects.get(pk=pk)
        form = HospitalForm(instance=hospital, data=request.POST)
        if form.is_valid():
            form = form.save()
            
        information = Hospital.objects.all()
        return render(request, "patient/hospitallist.html",{"information":information, "form":form}) 

@login_required
def hospitalinformation(request):
    if request.method == "POST":
        form = HospitalForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("/hospitallist")
    else:
        form = HospitalForm()

    return render(request, "patient/hospitalinformation.html", {"form":form})


@login_required
def hospitallist(request):
    if request.method == "POST":
        form = HospitalForm(request.POST, instance=image)
       
        if form.is_valid():
            form.save()
    else:
        form = HospitalForm()
    information = Hospital.objects.all()
    return render(request, "patient/hospitallist.html", {"information":information, "form":form})


def hospital_delete(request, pk):

    pk = pk
    try:
        image_sel = Hospital.objects.get(pk = pk)
    except Hospital.DoesNotExist:
        return redirect('hospitallist')
    image_sel.delete()
    return redirect('hospitallist')


@login_required
def appointment_list(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
        form = AppointmentForm()
        appointments = Appointment.objects.all()
        doctors = Doctor.objects.all()
        patients = Patient.objects.all()

        return render(request, 'appointments/appointment_list.html', {'appointments': appointments, "doctors":doctors,"patients" : patients, "form":form})
    else:
        form = AppointmentForm()
    appointments = Appointment.objects.all()
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()

    return render(request, 'appointments/appointment_list.html', {'appointments': appointments, "doctors":doctors,"patients" : patients, "form":form})

def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'appointments/appointment_form.html', {'form': form})

def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        return redirect('appointment_list')
    return render(request, 'appointments/appointment_confirm_delete.html', {'appointment': appointment})

def doctor_appointment_view(request):
    user = request.user  # This should be a logged-in doctor user
    try:
        doctor = Doctor.objects.get(name=user)
    except Doctor.DoesNotExist:
        doctor = None  # Handle the case where there is no matching doctor
    if doctor:
        appointments = Appointment.objects.filter(doctor=doctor)
        return render(request, 'patient/doctor_appointment_view.html', {'appointments': appointments})
    else:
        appointments = Appointment.objects.all()
        return render(request, 'patient/doctor_appointment_view.html', {'appointments': appointments})
        
    

    
     #user.groups = 