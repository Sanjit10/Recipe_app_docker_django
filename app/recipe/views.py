"""
Views for the recipe api
"""

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """"View for manage recipe APIs"""
    serializers_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication)
    permission_classes = (IsAuthenticated)

    def get_queryset(self):
        """Retrive recipes for authenticated user"""
        return self.queryset.filter(suer=self.request.user).order_by(-id)


