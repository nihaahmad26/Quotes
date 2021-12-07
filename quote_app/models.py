from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    
    def validate(self, form):
        errors = {}
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = 'Invalid Email Address'
        
        email_check = self.filter(email=form['email'])
        if email_check:
            errors['email'] = "Email already in use"

        if len(form['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        
        if form['password'] != form['confirm']:
            errors['password'] = 'Passwords do not match'
        
        return errors

    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False

        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def register(self, form):
        pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name = form['first_name'],
            last_name = form['last_name'],
            email = form['email'],
            password = pw,
        )
class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length = 45)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    objects = UserManager()

class QuoteManager(models.Manager):
    def quote_validator(self, postData):
        errors = {}
        print(postData)
        if len(postData['author']) < 2:
                errors['author'] = "Authors must be atleast 2 characters long"
        if len(postData['description']) < 10:
                errors['description'] = "Quotes must at least 10 characters long."
        return errors

class Quote(models.Model):
    author = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name="has_created_quotes", on_delete=models.CASCADE)
    favorited_by = models.ManyToManyField(User, related_name="favorited_quotes")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = QuoteManager()