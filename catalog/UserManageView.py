from catalog.BaseManageView import BaseManageView
from catalog.views import  UserDestroyView, UserDetailsView, UserUpdateView


class UserManageView(BaseManageView):
    VIEWS_BY_METHOD = {
        'DELETE': UserDestroyView.as_view,
        'GET': UserDetailsView.as_view,
        'PUT': UserUpdateView.as_view,
        'PATCH': UserUpdateView.as_view
    }