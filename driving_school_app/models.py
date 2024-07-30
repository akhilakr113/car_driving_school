from django.db import models

# Create your models here.
class Login(models.Model):
    login_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    usertype = models.CharField(max_length=150)

class Categories(models.Model):
    categories_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=150)

class Drivingschool(models.Model):
    drivingschool_id = models.AutoField(primary_key=True)
    login = models.ForeignKey(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    place = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    license = models.CharField(max_length=1500)
    Latitude=models.CharField(max_length=225,default='000')
    Longitude=models.CharField(max_length=225,default='000')
    Cat=models.CharField(max_length=225,default='twowheeler')

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    login = models.ForeignKey(Login, on_delete=models.CASCADE)
    Drivingschool = models.ForeignKey(Drivingschool, on_delete=models.CASCADE,default='000')
    fname = models.CharField(max_length=150)
    lname = models.CharField(max_length=150)
    place = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    dob = models.CharField(max_length=150)
    gender = models.CharField(max_length=150)
    
class Trainer(models.Model):
    trainer_id = models.AutoField(primary_key=True)
    login = models.ForeignKey(Login, on_delete=models.CASCADE)
    drivingschool = models.ForeignKey(Drivingschool, on_delete=models.CASCADE)
    fname = models.CharField(max_length=150)
    lname = models.CharField(max_length=150)
    place = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    dob = models.CharField(max_length=150)
    gender = models.CharField(max_length=150)

class AssignedTrainer(models.Model):
    assigned_id = models.AutoField(primary_key=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='trainer')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trainee')
    date = models.CharField(max_length=150)
    status = models.CharField(max_length=150)

class DrivingRequest(models.Model):
    driving_request_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.CharField(max_length=150)
    date = models.CharField(max_length=150)
    status = models.CharField(max_length=150)

class LicenseRequest(models.Model):
    license_request_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.CharField(max_length=150)
    date = models.CharField(max_length=150)
    status = models.CharField(max_length=150)

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    request = models.ForeignKey('DrivingRequest', on_delete=models.CASCADE)
    type = models.CharField(max_length=150)
    amount = models.CharField(max_length=150)
    date = models.CharField(max_length=150)

class Complaint(models.Model):
    complaint_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    complaint = models.CharField(max_length=150)
    reply_text = models.CharField(max_length=150)
    date = models.CharField(max_length=150)

class Tutorial(models.Model):
    tutorial_id = models.AutoField(primary_key=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    tutorial = models.FileField()
    type = models.CharField(max_length=150)
    date = models.CharField(max_length=150)

class Queries(models.Model):
    queries_id = models.AutoField(primary_key=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE,default='1')
    drivingschool = models.ForeignKey(Drivingschool, on_delete=models.CASCADE)
    message = models.CharField(max_length=150)
    reply = models.CharField(max_length=150)
    date = models.CharField(max_length=150)
class chats(models.Model):
    chat_id=models.AutoField(primary_key=True)
    sender=models.IntegerField(max_length=225) 
    sender_type=models.CharField(max_length=225)
    receiver=models.IntegerField(max_length=225)  
    reciver_type=models.CharField(max_length=225)   
    message=models.CharField(max_length=225) 
    date_time=models.CharField(max_length=225) 
    