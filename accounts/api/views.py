from django.contrib.auth import authenticate
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from accounts.api.serializers import UserSerializer, UserEditSerializer
from accounts.models import User

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


@api_view(['POST'])
@permission_classes([AllowAny, ])
def login(request):
    try:
        username = request.data['username']
        password = request.data['password']
        if not username or not password:
            msg = 'Please fill in all required fields'
            return Response({
                "status": 0,
                "msg": msg

            })
        try:
            user = User.objects.all().filter(username=username).first()
            if user is None:
                msg = 'Can not authenticate with the given credentials or the account has been deactivated'
                res = {
                    'status': 0,
                    'msg': msg
                }
                return Response(res, status=status.HTTP_403_FORBIDDEN)
            pas = user.check_password(str(password))
            if not pas:
                msg = "Password doesn't correct"
                res = {
                    'status': 0,
                    'msg': msg
                }
                return Response(res, status=status.HTTP_403_FORBIDDEN)
            print(pas)

        except Exception as e:
            res = {
                'status': 0,
                'msg': str(e)
            }
            return Response(res)

        user_auth = authenticate(username=username, password=str(password))
        if (user_auth and pas) or (user.is_staff and pas):
            if user.complete == 0 and user.is_superuser == 0:
                msg = 'You did not complete the registration. Please check you email'
                res = {
                    'msg': msg,
                    'status': 0,
                }
                return Response(res)
            msg = 'User sign in'
            try:
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                user_details = {}
                user_details['status'] = 1
                user_details['msg'] = msg
                user_details['data'] = UserSerializer(user, many=False).data
                user_details['token'] = token
                return Response(user_details, status=status.HTTP_200_OK)

            except Exception as e:
                raise e
        else:
            msg = 'Can not authenticate with the given credentials or the account has been deactivated'
            res = {
                'status': 0,
                'msg': msg
            }
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:

        res = {
            'status': 0,
            'error': str(e)
        }

        return Response(res)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def register(request):
    try:

        first_name = request.data.get('first_name', None)
        last_name = request.data.get('last_name', None)
        username = request.data.get('username', None)
        is_teacher = request.data.get('is_teacher', None)
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        if not email or not password or not username:
            msg = 'Please fill in all required fields'
            return Response({
                "status": 0,
                "msg": msg

            })

        user = User.objects.filter(email=email).first()

        if user and user.complete == 1:

            msg = 'There is a registered user with the information provided'
            res = {
                'msg': msg,
                'status': 2,
            }
            return Response(res)

        else:
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                complete=1,
            )
            user.set_password(password)
            user.save()
            msg = 'Created User. '

            if is_teacher == '1':
                user.complete = 0
                user.is_teacher = True
                user.save()
                msg += 'Our admins will contact you'

            res = {
                'status': 1,
                'msg': msg
                }
            return Response(res, status=status.HTTP_200_OK)


    except Exception as e:
        res = {
            'status': 0,
            'msg': str(e)
        }
        return Response(res)

# from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
# 
# 
# @api_view(['POST', 'GET'])
# @permission_classes([AllowAny, ])
# def accept(request, uidb64, token):
#     try:
#         id = smart_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(id=id)
#         redirect_url = request.GET.get('redirect_url')
#         data = {'token': token}
#         valid_data = VerifyJSONWebTokenSerializer().validate(data)
#         user_valid = valid_data['user']
#         print(user_valid)
# 
#         if not user:
#             res = {
#                 'msg': 'user does not exists',
#                 'status': 0
#             }
#             return Response(res)
# 
# 
# 
#         elif user == user_valid:
#             print(user)
#             user.complate = 1
#             user.save()
#             res = {
#                 'status': 1,
#                 'msg': 'Tasdiqlandi',
#             }
#             return HttpResponseRedirect(redirect_to=redirect_url)
# 
#         res = {
#             'status': 0,
#             'msg': 'sms code xato kiritildi',
#         }
#         return Response(res)
#     except Exception as e:
#         res = {
#             'status': 'error',
#             'msg': str(e)
#         }
#         return Response(res)

class UserProfileEditView(APIView):
    permission_classes = [IsAuthenticated, ]

    def put(self, request):
        user = request.user
        serializer = UserEditSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
