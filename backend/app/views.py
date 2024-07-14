from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from . models import *
from . serializer import *
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class RecipeView(APIView):
  serializer_class = RecipeSerializer
  def get(self, request):
    output = [{'id': output.id,'title': output.title, 'description': output.description} for output in Recipe.objects.all()]
    return Response(output)

  def post(self, request):
    serializer = RecipeSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      return Response(serializer.data)



class RecipeDetailView(APIView):
    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)

    def delete(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
