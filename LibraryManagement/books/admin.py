from django.contrib import admin
from books.models import Department,IssueDetail,Book,BookStatus,IssueStatus
# Register your models here.

admin.site.register(Department)
admin.site.register(IssueDetail)
admin.site.register(IssueStatus)
admin.site.register(Book)
admin.site.register(BookStatus)