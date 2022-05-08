import datetime

from rest_framework import status, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, get_object_or_404, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from accounts.models import User
from course.api.serializers import CategorySerializer, CourseSerializer, CourseListSerializer, ReviewSerializer, \
    ReviewCreateSerializer, MyCourseListSerializer, TeacherCourseListSerializer, AdminDashboardListSerializer, \
    CourseCreateSerializer, SectionCreateSerializer, LessonCreateSerializer, OrderSerializer, OrderItemsSerializer
from course.models import Category, Course, Review, UserBuy, Section, Lesson, Order, OrderItem
from course.permissions import IsAuthenticatedOrReadOnly, IsTeacherCreate, IsCourseOwner


class CategoryListApiView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().filter(status=True)

    def get(self, request):
        category = Category.objects.all().filter(status=True)
        serializer = CategorySerializer(category, many=True, context={'request': request})
        return Response(serializer.data)


class CategoryDetailApiView(RetrieveAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    queryset = Category.objects.all().filter(status=True)

    def get_object(self, value_from_url):
        category = get_object_or_404(Category, slug=value_from_url)
        return category

    def get(self, request, value_from_url):
        category = self.get_object(value_from_url)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


class CategoryCreateApiView(CreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsTeacherCreate]
    queryset = Category.objects.all().filter(status=True)

    def post(self, request, *args, **kwargs):
        try:
            category = Category.objects.create(
                name=request.data.get('name', None),
                image=request.data.get('image', None),
                video=request.data.get('video', None),
                description=request.data.get('description', None),
            )
            res = {
                'status': 1,
                'data': CategorySerializer(category, many=False, context={'request': request}).data
            }

            return Response(res, status=status.HTTP_201_CREATED)
        except Exception as e:
            res = {
                "status": 0,
                "msg": str(e)
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)


class CategoryApiView(APIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all().filter(status=True)

    def get_object(self, value_from_url):
        category = get_object_or_404(Category, slug=value_from_url)
        return category

    def get(self, request, value_from_url):
        category = self.get_object(value_from_url)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, value_from_url):
        try:
            category = self.get_object(value_from_url=value_from_url)
            category.name = request.data.get('name', category.name)
            category.image = request.data.get('image', category.image)
            category.video = request.data.get('video', category.video)
            category.description = request.data.get('description', category.description)
            serializer = CategorySerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                res = {
                    "status": 1,
                    "data": serializer.data,
                }
                return Response(res, status=status.HTTP_201_CREATED)

            res = {
                "status": 0,
                "msg": serializer.errors,
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, value_from_url):
        category = self.get_object(value_from_url)
        category.delete()
        res = {
            "status": 1,
            "msg": f"slug={value_from_url} storage was deleted"
        }
        return Response(res, status=status.HTTP_204_NO_CONTENT)


class CourseListApiView(ListAPIView):
    serializer_class = CourseListSerializer
    queryset = Course.objects.all().filter(status=True)

    def get(self, request):
        course = Course.objects.all().filter(status=True)
        serializer = CourseListSerializer(course, many=True, context={'request': request})
        return Response(serializer.data)


class MyCourseListApiView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MyCourseListSerializer

    def get(self, request):
        user = request.user
        course = Course.objects.filter(course_buy__isnull=False, course_buy__user=user,
                                       course_buy__end_date__gt=datetime.datetime.now())
        serializer = MyCourseListSerializer(course, many=True, context={'request': request})
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def remove_in_mycourse(request):
    try:
        user = request.user
        course = request.POST.get('course_id')
        user_by_course = UserBuy.objects.filter(user=user, course_id=course)
        if user_by_course:
            user_by_course.delete()
            return Response({'status': 1, 'msg': f'The course with id = {course} was successfully deleted'})
        else:
            return Response({'status': 0,
                             'msg': f'A course with id = {course} has not yet been purchased or has already been deleted'})

    except Exception as e:
        return Response({'status': 0, 'msg': str(e)})


class CourseDetailApiView(RetrieveAPIView):
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]
    queryset = Course.objects.all().filter(status=True)

    def get_object(self, value_from_url):
        category = get_object_or_404(Course, slug=value_from_url)
        return category

    def get(self, request, value_from_url):
        category = self.get_object(value_from_url)
        serializer = CourseSerializer(category, many=False, context={"request": request})
        return Response(serializer.data)


class ReviewView(ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        queryset = Review.objects.all()
        course = self.request.GET.get('course_slug', None)
        if course:
            queryset = queryset.filter(course__slug=course)
        return queryset


class ReviewCreateView(CreateAPIView):
    serializer_class = ReviewCreateSerializer
    queryset = Review.objects.all()


class TeacherCourse(ListAPIView):
    serializer_class = TeacherCourseListSerializer
    permission_classes = [IsAuthenticated, IsCourseOwner]

    def get_queryset(self):
        queryset = Course.objects.all().filter(author=self.request.user)
        return queryset


class AdminDashboard(ListAPIView):
    serializer_class = AdminDashboardListSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = User.objects.all().filter(is_teacher=True)
        return queryset


class CourseTeacherViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                           mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Course.objects.all()
    serializer_class = CourseCreateSerializer
    ordering_fields = '__all__'
    ordering = ['id']

    def create(self, request, *args, **kwargs):
        # self.permission_classes = [IsAuthenticated]
        # self.check_permissions(request)
        serializer = CourseCreateSerializer(data=request.data)
        if serializer.is_valid():
            course = serializer.save()
            course.author = request.user
            course.save()
            res = {
                "status": status.HTTP_200_OK,
                "data": CourseCreateSerializer(course, many=False, context={"request": request}).data
            }
        else:
            res = {
                "status": status.HTTP_400_BAD_REQUEST,
                "error": serializer.errors
            }

        return Response(res)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = CourseCreateSerializer(instance, data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            course = serializer.save()
            res = {
                "status": status.HTTP_200_OK,
                "data": CourseCreateSerializer(course, many=False, context={"request": request}).data
            }
        else:
            res = {
                "status": status.HTTP_400_BAD_REQUEST,
                "error": serializer.errors
            }

        return Response(res)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"status": status.HTTP_200_OK, "msg": "Course deleted"}, status=status.HTTP_200_OK)


class SectionTeacherViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                            mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Section.objects.all()
    serializer_class = SectionCreateSerializer
    ordering_fields = '__all__'
    ordering = ['id']

    def create(self, request, *args, **kwargs):
        serializer = SectionCreateSerializer(data=request.data)
        if serializer.is_valid():
            section = serializer.save()
            section.save()
            res = {
                "status": status.HTTP_200_OK,
                "data": SectionCreateSerializer(section, many=False, context={"request": request}).data
            }
        else:
            res = {
                "status": status.HTTP_400_BAD_REQUEST,
                "error": serializer.errors
            }

        return Response(res)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = SectionCreateSerializer(instance, data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            course = serializer.save()
            res = {
                "status": status.HTTP_200_OK,
                "data": SectionCreateSerializer(course, many=False, context={"request": request}).data
            }
        else:
            res = {
                "status": status.HTTP_400_BAD_REQUEST,
                "error": serializer.errors
            }

        return Response(res)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"status": status.HTTP_200_OK, "msg": "Section deleted"}, status=status.HTTP_200_OK)


class LessonTeacherViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                           mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Lesson.objects.all()
    serializer_class = LessonCreateSerializer
    ordering_fields = '__all__'
    ordering = ['id']

    def create(self, request, *args, **kwargs):
        serializer = LessonCreateSerializer(data=request.data)
        if serializer.is_valid():
            lesson = serializer.save()
            lesson.save()
            res = {
                "status": status.HTTP_200_OK,
                "data": LessonCreateSerializer(lesson, many=False, context={"request": request}).data
            }
        else:
            res = {
                "status": status.HTTP_400_BAD_REQUEST,
                "error": serializer.errors
            }

        return Response(res)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = LessonCreateSerializer(instance, data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            lesson = serializer.save()
            res = {
                "status": status.HTTP_200_OK,
                "data": LessonCreateSerializer(lesson, many=False, context={"request": request}).data
            }
        else:
            res = {
                "status": status.HTTP_400_BAD_REQUEST,
                "error": serializer.errors
            }

        return Response(res)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"status": status.HTTP_200_OK, "msg": "Section deleted"}, status=status.HTTP_200_OK)


class OrderViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                   mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    ordering_fields = '__all__'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")


class OrderItemViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                       mixins.DestroyModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderItemsSerializer
    ordering_fields = '__all__'

    def get_queryset(self):
        course_id = self.request.query_params.get('course_id', -1)
        order_id = self.request.query_params.get('order_id', -1)

        queryset = OrderItem.objects.filter(order_id=order_id, course_id=course_id).order_by("-created_at")
        return queryset
