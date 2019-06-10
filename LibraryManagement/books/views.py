from django.shortcuts import render
import datetime
from books.models import (
        Book,
        BookStatus,
        Department,
        IssueDetail,
        IssueStatus)
from books.serializers import (
        BookSerializer,
        UserSerializer,
        IssueBookSerializer,
        IssueBookStaffSerializer,)
       
from django.http import Http404
#from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import (
        status,
        generics,
        permissions,
        viewsets,
        filters,
        )
from django.contrib.auth.models import User
from books.permissions import (
        IsOwnerOrReadOnly,
        IsStaffOrStudent,
        IsStaff,
        )
from rest_framework.decorators import action,api_view
from django.contrib.auth.models import User,Group

@api_view(['GET'])
def api_root(request,format=None):
    return Response({
        'users':reverse('user-list',request=request,format=format),
        'books':reverse('book-list',request=request,format=format),
        'issuebook':reverse('issue-book',request=request,format=format),

    })

#@permission_classes((IsAuthenticated))

@api_view(['GET'])
def issue_details(request,format=None):
    if request.user.groups.filter(name='Student'):
        return Response({
            #'users':reverse('user-list',request=request,format=format),
            #View Books Issued by me
            #Request for book issue
            #Request for book return
            'issue-list':reverse('view-issue-list',request=request,format=format),
        })
    else:
        return Response({
            #'users':reverse('user-list',request=request,format=format),
            #if staff then...
            #View all books issued
            #Approve issue request
            #Return Request approve
            #Reject issue requests
            'issue-list':reverse('view-all-issues',request=request,format=format),
        })

class IssueRequestsView(viewsets.ModelViewSet):
    permission_classes=(permissions.IsAuthenticated,IsStaff,)
    serializer_class=IssueBookSerializer
    def get_queryset(self):
        user=self.request.user
        if self.request.user.groups.filter(name='Student'):
            return IssueDetail.objects.filter(student=user)
        return IssueDetail.objects.all() 
    
    @action(detail=True)
    def perform_create(self,serializer):
        user=self.request.user
        obj=IssueDetail.objects.filter(student=user)
        issued=IssueDetail.objects.filter(student=user,issue_status_id=2).count()
        requestReturn=IssueDetail.objects.filter(student=user,issue_status_id=3).count()
        if issued+requestReturn<3:
            serializer.save(student=self.request.user)
        else:
            print("Error")
            raise ValidationError('More than 3 books cannot be issued.')
    
    def retrieve(self,request,pk=None):
        obj=IssueDetail.objects.get(pk=pk)
        if obj.issue_status_id==2:
            obj.issue_status_id=3
        obj.save()
        serializer=IssueBookStaffSerializer(obj)
        return Response(serializer.data)

class IssueRequestStaffView(viewsets.ModelViewSet):
    queryset=IssueDetail.objects.all()
    serializer_class=IssueBookStaffSerializer
    

class RequestHandlingViewSet(viewsets.ViewSet):
    permission_classes=(permissions.IsAuthenticated,IsStaffOrStudent,)
    def list(self, request):
        pass

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        obj=IssueDetail.objects.get(pk=pk)
        bookObj=Book.objects.get(isbn=obj.isbn_id)
        if obj.issue_status_id==1:#Pending
            print(obj.isbn)
            if bookObj.status_id==2:
                obj.issue_status_id=5
            else:  
                obj.issued_on=datetime.date.today()
                obj.issue_status_id=2
                bookObj.status_id=2 #Updating book status
                bookObj.save()
            obj.save()
        elif obj.issue_status_id==3:#Request for return
            obj.returned_on=datetime.date.today()
            idate=obj.issued_on
            rdate=obj.returned_on
            delta=rdate-idate
            diff=(delta.days)
            if diff>15:
                diff=diff-15
                obj.fine=1*diff
            bookObj.status_id=1 #Updating book status
            bookObj.save()
            obj.issue_status_id=4   
            obj.save()
        serializer=IssueBookStaffSerializer(obj)
        return Response(serializer.data)


    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass

class BookViewSet(viewsets.ModelViewSet):
    queryset=Book.objects.all()
    serializer_class=BookSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields=['book_name','department_name__department_name','status__status']
    #department_name before dunder belongs to book table(foreignKeyField) and 
    #after dunder belongs to the table from where it actually comes
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,IsStaffOrStudent,)
    @action(detail=True)
    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
