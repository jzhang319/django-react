from rest_framework import serializers
from . models import *

class RecipeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Recipe
    fields = ['title', 'description']
    # fields = '__all__'
