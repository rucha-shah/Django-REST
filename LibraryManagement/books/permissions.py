from rest_framework import permissions
from django.contrib.auth.models import User,Group
BASIC_METHODS=('GET','POST','PATCH','DELETE','HEAD','OPTIONS')
STAFF_ISSUE=('GET','PATCH')
class IsOwnerOrReadOnly(permissions.BasePermission):
    message="You don't have permissions to edit this content"
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner==request.user

#If the User is student, then it is only allowed to view books
class IsStaffOrStudent(permissions.BasePermission):
    def has_permission(self,request,view):
        if request.user.groups.filter(name='Student'):
            return request.method in permissions.SAFE_METHODS
        else:
            return request.method in BASIC_METHODS

class IsStaff(permissions.BasePermission):
    def has_permission(self,request,view):
        if request.user.groups.filter(name='Student'):
            return request.method in BASIC_METHODS
        else:
            return request.method in STAFF_ISSUE
'''
class IsIssuerOrReadOnly(permissions.BasePermission):
    message="You don't have permissions to edit this content"
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.student==request.user           
'''