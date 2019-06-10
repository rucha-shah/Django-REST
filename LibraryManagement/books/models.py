from django.db import models
from django.core.validators import MaxLengthValidator,MinLengthValidator
from django.contrib.auth.models import User,Group
# Create your models here.
#department_choices=(for item[0][1] in Department)
#bookstatus_choices=(for item[0][1] in BookStatus)
class Department(models.Model):
    department_name=models.CharField(max_length=50)

    def __str__(self):
        return self.department_name

class BookStatus(models.Model):
    status=models.CharField(max_length=25)
    def __str__(self):
        return self.status

class Book(models.Model):
    owner=models.ForeignKey('auth.User',related_name='books',on_delete=models.CASCADE)
    isbn=models.BigIntegerField(primary_key=True)
    book_name=models.CharField(max_length=200)
    author=models.CharField(max_length=100)
    department_name=models.ForeignKey(Department,on_delete=models.CASCADE)
    status=models.ForeignKey(BookStatus,on_delete=models.CASCADE)
    def __str__(self):
        return self.book_name+' '+self.author

    def save(self,*args,**kwargs):
        isbn=self.isbn
        book_name=self.book_name
        author=self.author
        department_name=self.department_name
        status=self.status
        super(Book,self).save(*args,**kwargs)
    
class IssueStatus(models.Model):
    issue_status=models.CharField(max_length=20)
    def __str__(self):
        return self.issue_status

class IssueDetail(models.Model):
    student=models.ForeignKey('auth.User',related_name='issue_details',on_delete=models.CASCADE)
    isbn=models.ForeignKey(Book,on_delete=models.CASCADE)
    issued_on=models.DateField(null=True)
    returned_on=models.DateField(null=True)
    fine=models.IntegerField(default=0)
    issue_status=models.ForeignKey(IssueStatus,default=1,on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.isbn)+'- Issued On:'+str(self.issued_on)
        +'-Returned On:'+str(self.returned_on)+'-Fine:'+str(self.fine)
    
    def save(self,*args,**kwargs):
        isbn=self.isbn
        issued_on=self.issued_on
        returned_on=self.returned_on
        fine=self.fine
        # student=self.student
        super(IssueDetail,self).save(*args,**kwargs)