import random
import string
from django.contrib.auth.models import User
from django.db import models

class Hospital(models.Model):
    name = models.CharField(max_length=100, unique=True, default='N/A')
    address = models.TextField()
    telephone = models.CharField(max_length=20, default='N/A')

    def __str__(self):
        return self.name

class Pharmacie(models.Model):
    nom = models.CharField(max_length=255, unique=True, default='N/A')
    adresse = models.TextField()
    telephone = models.CharField(max_length=20, default='N/A')

    def __str__(self):
        return self.nom

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', default='profile_images/default.jpg', blank=True)
    ROLES = [
        ('admin', 'Admin'),
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('pharmacist', 'Pharmacist'),
    ]
    role = models.CharField(max_length=20, choices=ROLES, default='patient')

    def __str__(self):
        return f"{self.user.username} ({self.role})"

class Pharmacien(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    license_number = models.CharField(max_length=50, null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    pharmacie = models.OneToOneField(Pharmacie, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name or "Pharmacien"

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    SPECIALISATIONS = [
        ('generaliste', 'Généraliste'),
        ('radiologue', 'Radiologue'),
        ('laborantin', 'Laborantin'),
        ('cardiologue', 'Cardiologue'),
        ('dermatologue', 'Dermatologue'),
        ('endocrinologue', 'Endocrinologue'),
        ('gastroenterologue', 'Gastro-entérologue'),
        ('gynecologue', 'Gynécologue'),
        ('neurologue', 'Neurologue'),
        ('ophtalmologue', 'Ophtalmologue'),
        ('orthopediste', 'Orthopédiste'),
        ('otorhinolaryngologiste', 'ORL (Oto-rhino-laryngologiste)'),
        ('pediatre', 'Pédiatre'),
        ('psychiatre', 'Psychiatre'),
        ('pneumologue', 'Pneumologue'),
        ('rhumatologue', 'Rhumatologue'),
        ('urologue', 'Urologue'),
        ('anesthesiste', 'Anesthésiste'),
        ('oncologue', 'Oncologue'),
        ('hematologue', 'Hématologue'),
        ('medecin_du_travail', 'Médecin du Travail'),
        ('medecin_urgentiste', 'Médecin Urgentiste'),
    ]

    specialization = models.CharField(max_length=100, choices=SPECIALISATIONS, default='generaliste')
    name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    license_number = models.CharField(max_length=50, null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    hospital = models.OneToOneField(Hospital, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name or "Doctor"

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField()
    medical_history = models.TextField(blank=True)
    email = models.EmailField(blank=True, null=True)
    MRN = models.CharField(max_length=20, unique=True, null=True)

    def __str__(self):
        return self.username or "Patient"

    def save(self, *args, **kwargs):
        if not self.MRN:
            self.MRN = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))
        super().save(*args, **kwargs)

class DossierMedical(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctors = models.ManyToManyField(Doctor, related_name="dossiers_medicals")
    date_creation = models.DateTimeField(auto_now_add=True)
    contenu = models.TextField()
    diagnosis = models.CharField(max_length=100, blank=True, null=True)
    drug = models.CharField(max_length=100, blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"Dossier {self.id} - {self.patient}"

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    statut = models.CharField(max_length=20, choices=[('en_attente', 'En attente'), ('confirme', 'Confirmé'), ('annule', 'Annulé')], default='en_attente')
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    detail = models.TextField()
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    def __str__(self):
        return f"RDV {self.id} - {self.patient} avec {self.doctor}"

class Prescription(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'patient'})
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date_prescription = models.DateTimeField(auto_now_add=True)
    medicaments = models.TextField()

    def __str__(self):
        return f"Prescription {self.id} - {self.patient.username}"