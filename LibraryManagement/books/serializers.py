from rest_framework import serializers
from books.models import Book,BookStatus,Department,IssueDetail
from django.contrib.auth.models import User,Group
class BookSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    #status=serializers.StringRelatedField(read_only=True)
    #department_name=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Book
        fields=('isbn','book_name','author','department_name','status','owner')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','username','groups')

class IssueBookSerializer(serializers.ModelSerializer):
    student=serializers.ReadOnlyField(source='student.username')
    issue_status=serializers.StringRelatedField(read_only=True)
    #issue_request='REQUEST'
    class Meta:
        model=IssueDetail
        fields=('id','isbn','issued_on','returned_on','fine','issue_status','student')
        read_only_fields=('issued_on','returned_on','fine','issue_status')

class IssueBookStaffSerializer(serializers.ModelSerializer):
    student=serializers.ReadOnlyField(source='student.username')
    issue_status=serializers.StringRelatedField()
    #approve_request='APPROVE'
    class Meta:
        model=IssueDetail
        fields=('id','isbn','issued_on','returned_on','fine','issue_status','student')
        read_only_fields=('issued_on','returned_on','fine')
