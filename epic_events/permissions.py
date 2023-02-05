from rest_framework import permissions
from django.contrib.auth.models import User
# permissions.DjangoModelPermissions


# class IsSupportTeam(permissions.BasePermission):
#     """
#     Allows access only to contributors or project owners.
#     """
#
#     def has_permission(self, request, view):
#         if 'pk' in view.kwargs:
#             obj = view.get_object()
#             return self.has_object_permission(request, view, obj)
#         else:
#             value = False
#             project = Project.objects.get(id=view.kwargs['project_pk'])
#             if request.user in project.contributors.all() or \
#                     request.user == project.author:
#                 value = True
#             return value
#
#     def has_object_permission(self, request, view, obj):
#         value = False
#         project = Project.objects.get(id=view.kwargs['project_pk'])
#         try:
#             if request.user in project.contributors.all() or \
#                     request.user == obj.project.author:
#                 value = True
#         except AttributeError:
#             if request.user in project.contributors.all() or \
#                     request.user == obj.issue.project.author:
#                 value = True
#         return value