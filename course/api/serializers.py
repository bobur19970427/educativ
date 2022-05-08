import datetime

from django.db.models import Avg
from rest_framework import serializers

from accounts.api.serializers import UserSerializer
from accounts.models import User
from config import settings
from config.utils import format_seconds_to_hhmmss
from course.models import Category, Course, Lesson, UserBuy, Section, Knowledge, Whom, Requirement, Review, Order, \
    OrderItem


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()
    course_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "image", 'video', "description", "course_count", "slug"]

    def get_image(self, obj):
        image = obj.image
        if (len(str(image)) > 0):
            return settings.APP_URL + settings.MEDIA_URL + str(image)
        else:
            return ''

    def get_video(self, obj):
        video = obj.video
        if (len(str(video)) > 0):
            return settings.APP_URL + settings.MEDIA_URL + str(video)
        else:
            return ''

    def get_course_count(self, obj):
        return Course.objects.filter(category=obj).distinct().count()


class CourseListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()

    # author = UserSerializer()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "name", "image", 'video', 'price', "slug", "category"]

    def get_image(self, obj):
        image = obj.image
        if (len(str(image)) > 0):
            return settings.APP_URL + settings.MEDIA_URL + str(image)
        else:
            return ''

    def get_video(self, obj):
        video = obj.video
        if (len(str(video)) > 0):
            return settings.APP_URL + settings.MEDIA_URL + str(video)
        else:
            return ''

    def get_category(self, obj):
        return obj.category.name


class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class SectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = "__all__"


class LessonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class MyCourseListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "name", "slug", "image"]

    def get_image(self, obj):
        image = obj.image
        if (len(str(image)) > 0):
            return settings.APP_URL + settings.MEDIA_URL + str(image)
        else:
            return ''


class TeacherCourseListSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "name", "slug", "student"]

    def get_student(self, obj):
        return UserBuy.objects.all().filter(course=obj).count()


class AdminDashboardListSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'course')

    def get_course(self, obj):
        courses = obj.author_courses.all()
        print(courses)

        return TeacherCourseListSerializer(courses, many=True, context={'request': self.context['request']}).data


class LessonSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ["id", "name", "description", "slug", "content", "file", "is_demo", "duration", ]

    def get_duration(self, obj):
        if obj.duration:
            return format_seconds_to_hhmmss(obj.duration)
        else:
            return ""


class LessonListSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()
    has_permission = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ["id", "name", "slug", "is_demo", "duration", "has_permission", ]

    def get_duration(self, obj):
        if obj.duration:
            return format_seconds_to_hhmmss(obj.duration)
        else:
            return ""

    def get_has_permission(self, obj):
        user = self.context['request'].user
        return obj.hasPermission(user_id=user.id if user else -1)

    def get_slug(self, obj):
        user = self.context['request'].user
        permission = obj.hasPermission(user_id=user.id if user else -1)
        return obj.slug if permission else ''


class SectionSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = ["id", "name", "description", "slug", "lessons", ]

    def get_lessons(self, obj):
        lesson = Lesson.objects.all().filter(status=True, section=obj, course=self.context.get('course'))
        serializer = LessonListSerializer(lesson, many=True, context={'request': self.context['request']})
        return serializer.data


class CourseSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    lectures = serializers.SerializerMethodField()
    students_count = serializers.SerializerMethodField()
    knowladge = serializers.SerializerMethodField()
    whom = serializers.SerializerMethodField()
    requirement = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    overal_rating = serializers.SerializerMethodField()
    is_buy = serializers.SerializerMethodField()

    author = UserSerializer()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "name", "image", 'video', 'order', 'price', 'difficulty', "description", "slug",
                  "overal_rating", "is_buy",
                  "category", "author", "duration", "lectures", "students_count", "knowladge", "whom", "requirement",
                  "content"]

    def get_image(self, obj):
        image = obj.image
        if (len(str(image)) > 0):
            return settings.APP_URL + settings.MEDIA_URL + str(image)
        else:
            return ''

    def get_video(self, obj):
        video = obj.video
        if (len(str(video)) > 0):
            return settings.APP_URL + settings.MEDIA_URL + str(video)
        else:
            return ''

    def get_category(self, obj):
        return obj.category.name

    def get_duration(self, obj):
        objs = Lesson.objects.all().filter(course=obj)
        print(objs)
        seconds = 0

        for lesson in objs:
            seconds += lesson.duration
        return format_seconds_to_hhmmss(seconds)

    def get_lectures(self, obj):
        objs = Lesson.objects.all().filter(course=obj)
        return objs.count()

    def get_students_count(self, obj):
        objs = UserBuy.objects.all().filter(course=obj)
        return objs.count()

    def get_content(self, obj):

        section = Section.objects.all().filter(status=True, course=obj)
        serializer = SectionSerializer(section, many=True, context={'request': self.context['request'], "course": obj})
        return serializer.data

    def get_knowladge(self, obj):

        knowladge = Knowledge.objects.all().filter(course=obj)
        serializer = KnowledgeSerializer(knowladge, many=True, context={'request': self.context['request']})
        return serializer.data

    def get_whom(self, obj):

        whom = Whom.objects.all().filter(course=obj)
        serializer = WhomSerializer(whom, many=True, context={'request': self.context['request']})
        return serializer.data

    def get_requirement(self, obj):

        requirement = Requirement.objects.all().filter(course=obj)
        serializer = RequirementSerializer(requirement, many=True, context={'request': self.context['request']})
        return serializer.data

    def get_overal_rating(self, obj):
        reviews = Review.objects.all().filter(course=obj)
        review = reviews.aggregate(Avg('rating'))
        review['review_count'] = reviews.count()
        return review

    def get_is_buy(self, obj):
        try:
            user = self.context['request'].user
            return True if UserBuy.objects.filter(user=user, course=obj) else False
        except Exception as e:
            return False


class KnowledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Knowledge
        fields = ['name']


class WhomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Whom
        fields = ['name', 'description']


class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = ['name', 'description']


class UserRevieSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'avatar')


class ReviewSerializer(serializers.ModelSerializer):
    user = UserRevieSerializer()

    class Meta:
        model = Review
        fields = ('comment', "rating", 'user', 'course', 'created_at', 'updated_at')


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('comment', "rating", 'user', 'course', 'created_at', 'updated_at')


class OrderItemsSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = "__all__"

    def get_course(self, obj):
        if obj.course:
            data = CourseListSerializer(obj.course, many=False, context={'request': self.context['request']}).data

            return data
        return []


class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "total", "status", "order_items", "created_at", "updated_at",
                  "payment_url"]

    def get_order_items(self, obj):
        qs = OrderItem.objects.filter(order=obj)
        return OrderItemsSerializer(qs, many=True, context={'request': self.context['request']}).data
