from django.contrib.auth.models import User
from django.db.models import query
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.serializers import MovieSerializer, RatingSerializer, UserSerializer
from api.models import Movie, Rating




class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )


class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        
        if 'stars' in request.data:
            movie = Movie.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user

            try:
                rating = Rating.objects.get(user=user.id, movie=movie.id)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many=False)

                response = {'message': 'rating updated', 'result': serializer.data}
                return Response(response, status.HTTP_200_OK)
            except:
                rating = Rating.objects.create(user=user, movie=movie, stars=stars)
                serializer = RatingSerializer(rating, many=False)

                response = {'message': 'rating created', 'result': serializer.data}
                return Response(response, status.HTTP_200_OK)

        else:
            response = {'message': 'you need to provide stars'}
            return Response(response, status.HTTP_400_BAD_REQUEST)
    
    # def update(self, request, *args, **kwargs):
    #     response = {'message': 'cant update rating like that'}
    #     return Response(response, status.HTTP_400_BAD_REQUEST)

    # def create(self, request, *args, **kwargs):
    #     response = {'message': 'cant create rating like that'}
    #     return Response(response, status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny, )
    
    def update(self, request, *args, **kwargs):
        response = {'message': 'cant update rating like that'}
        return Response(response, status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {'message': 'cant create rating like that'}
        return Response(response, status.HTTP_400_BAD_REQUEST)