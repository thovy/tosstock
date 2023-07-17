from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .serializers import UserSerializer

User = get_user_model()

@api_view(['GET', 'DELETE'])
def current_user_detail(request):
    
    target_user = get_object_or_404(User, pk=request.user.pk)

    def get_user_detail():
        serializer = UserSerializer(target_user)
        return Response(serializer.data)
    
    def delete_user():
        if request.user == target_user:
            # django 에서 제공해주는 check pw 기능을 통해 입력된 pw와 db의 pw 비교
            # if target_user.check_password(request.POST["password"]):
            if target_user.check_password(request.data):
                target_user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                print('비밀번호가 틀렸습니다.')
                return Response('비번틀림', status=status.HTTP_401_UNAUTHORIZED)
        else:
            # print('다른 유저')
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    if request.method == 'GET':
        return get_user_detail()
    elif request.method == 'DELETE':
        return delete_user()

@api_view(['GET'])
# @permission_classes([IsAuthenticatedOrReadOnly])
def user_detail(request, username):

    target_user = get_object_or_404(User, username=username)
    serializer = UserSerializer(target_user)
    if target_user:
        return Response(serializer.data)
    return Response(status=status.HTTP_404_NOT_FOUND)
        

    
# 로그인 했을 때 자동으로 심사해서 팔로워가 100명이 넘으면 influ로 만들려고 했는데,
# 로그인 할 때마다 작동되는 것도 이상할테고,
# 뉴스를 크롤링할 때 팔로워 100명 넘는 사람들 filter해서 등급올리고,
# influ 중에서 팔로워 100안되는 애들 normal 로 내리는 것도 좋을 것 같다.
# 일단, 승급신청하면 심사하는 메서드로 만들어놓자.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_rankup(request):
    target_user = get_object_or_404(User, pk=request.user.pk)
    serializer = UserSerializer(target_user)
    
    # 작성한 게시글이 10개 이상일 때
    # 후에 follower 를 만들면 follwer 의 수도 체크하도록 합시다.
    if len(serializer.data['articles']) >= 10:
        target_user.isInfluencer = True
        target_user.save()
        # 조건에 맞으면 새로고침하라고 알려줍니다.(조건이 바뀌었으니 새로고침하면 명패(influ 인지 normal 인지)도 바뀔겁니다.)
        return Response(status=status.HTTP_205_RESET_CONTENT)
    else:
        # 조건에 미달되면 바뀌지 않습니다.
        return Response(status=status.HTTP_204_NO_CONTENT)