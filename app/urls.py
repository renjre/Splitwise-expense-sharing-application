from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *
router = DefaultRouter()
router.register('users', UsersViewSet)
router.register('rooms', RoomViewSet)
router.register('user-room', UserRoomViewSet)


urlpatterns = [
    # User endpoints
    path('', include(router.urls)),
    path('expenses/', ExpenseList.as_view(), name='expense_detail'),
    path('expenses/<int:pk>/', ExpenseDetailView.as_view(), name='expense_detail'),
    path('expense-splits/', ExpenseSplitList.as_view(), name='expense_split_list'),

    path('users-owes/', AllUsersOwesView.as_view(), name='all_users_owes_lends_view'),

]
