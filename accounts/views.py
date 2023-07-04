from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import UserSerializer

User = get_user_model()

@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def user_detail(request, username):

    target_user = get_object_or_404(User, username=username)

    def get_user_detail():
        serializer = UserSerializer(target_user)
        return Response(serializer.data)
    
    def delete_user():
        if request.user == target_user:
            
            # django 에서 제공해주는 check pw 기능을 통해 입력된 pw와 db의 pw 비교
            if target_user.check_password(request.POST["password"]):
                target_user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            print('다른 유저')
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    if request.method == 'GET':
        return get_user_detail()    
    elif request.method == 'DELETE':
        return delete_user()