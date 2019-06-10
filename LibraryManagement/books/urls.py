from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from books import views
from books.views import (
        UserViewSet, 
        BookViewSet, 
        IssueRequestsView,
        IssueRequestStaffView,
        RequestHandlingViewSet,)
        #ApprovePendingView
from rest_framework.routers import DefaultRouter
user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})
book_list = BookViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
book_detail = BookViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
#Student side
issue_request_student = IssueRequestsView.as_view({
    'get': 'list',
    'post': 'create'
})
#Student Side
'''view_detail=IssueRequestDetails.as_view({
    'get': 'retrieve',
    #'put': 'update',
    #'patch': 'partial_update',
    #'delete': 'destroy'
})'''
#Student Side
return_book=IssueRequestsView.as_view({
    'get':'retrieve',
})
#Staff Side
issue_request_all = IssueRequestStaffView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
#Staff Side
issue_request_options=IssueRequestStaffView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
#Staff Side
approve_issue=RequestHandlingViewSet.as_view({
    'get': 'retrieve',
    # 'put': 'update',
    #'patch': 'partial_update',
    # 'delete': 'destroy'

})
#Staff side
approve_return=RequestHandlingViewSet.as_view({
    'get': 'retrieve',
    # 'put': 'update',
    #'patch': 'partial_update',
    # 'delete': 'destroy'

})

'''

router=DefaultRouter()
router.register(r'books',views.BookViewSet)
router.register(r'users',views.UserViewSet)

router.register(r'issuebook',views.IssueRequestsView,base_name='issuebook')

'''
urlpatterns = [
    #path('books/', views.BookList.as_view()),
    #path('books/<int:pk>/', views.BookDetail.as_view()),
    path('',views.api_root),

    path('books/', book_list,name='book-list'),
    path('books/<int:pk>/', book_detail,name='book-detail'),
    path('issuebook/',views.issue_details,name='issue-book'),
    path('users/', user_list,name='user-list'),
    path('users/<int:pk>/', user_detail,name='user-detail'),
    
    #Student
    path('issuebook/issue-list',issue_request_student,name='view-issue-list'),
    #path('issuebook/issue-list/<int:pk>/',view_detail,name='view-detail'),
    path('issuebook/issue-list/<int:pk>/return-book',return_book,name='return-book'),#student-side
    
    #Staff
    path('issuebook/issue-list',issue_request_all,name='view-all-issues'),
    path('issuebook/issue-list/<int:pk>/',issue_request_options,name='view-options'),
    path('issuebook/issue-list/<int:pk>/approve-issue',approve_issue,name='approve-issue'),
    path('issuebook/issue-list/<int:pk>/approve-return',approve_return,name='approve-return'),
]

urlpatterns = format_suffix_patterns(urlpatterns)