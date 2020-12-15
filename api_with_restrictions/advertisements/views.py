from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer


# class AdvertisementViewSet(ModelViewSet):
#     """ViewSet для объявлений."""
#
#     queryset = Advertisement.objects.all()
#     serializer_class = AdvertisementSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = AdvertisementFilter
#
#     def get_permissions(self):
#         """Получение прав для действий."""
#         if self.action in ["create", "update", "partial_update"]:
#             return [IsAuthenticated()]
#         elif self.action in ["destroy", "update", "partial_update"]:
#             return [IsAdminUser()]
#         return [OnlyGetPermissions()]
#
#
# class OnlyGetPermissions(permissions.BasePermission):
#
#     def has_object_permission(self, request, view, obj):
#         if request.method == 'GET':
#             return True
#         return request.user == obj


"""Вариант Александра Бардина"""

class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update"]:
            return [IsAuthenticated()]
        return []

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        # print("Удаление внутри транзакции")
        # Получаем имя пользователя, который сделал запрос
        ad_user = request.user
        # получаем имя пользователя, который создал сущность, которую нужно удалить
        instance = self.get_object()
        creator_ad = instance.creator

        if ad_user != creator_ad:
            raise ValidationError({"Advertisement": "Удалять можно только свои записи!"})

        return super().destroy(request, *args, **kwargs)
