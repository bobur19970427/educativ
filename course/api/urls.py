from django.urls import path
from rest_framework.routers import SimpleRouter

from course.api.views import CategoryListApiView, CategoryApiView, CategoryCreateApiView, CourseListApiView, \
    CategoryDetailApiView, CourseDetailApiView, ReviewView, ReviewCreateView, MyCourseListApiView, remove_in_mycourse, \
    TeacherCourse, AdminDashboard, CourseTeacherViewSet, SectionTeacherViewSet, LessonTeacherViewSet, OrderViewSet, \
    OrderItemViewSet

urlpatterns = [
    path('category/', CategoryListApiView.as_view(), name='category-list'),
    path('category/create', CategoryCreateApiView.as_view(), name='category-create'),
    path('category/<str:value_from_url>/detail', CategoryDetailApiView.as_view(), name='category-detail'),
    path('category/<str:value_from_url>/crud', CategoryApiView.as_view(), name='category-crud'),

    path('course/', CourseListApiView.as_view(), name='course-list'),
    path('course/<str:value_from_url>/detail', CourseDetailApiView.as_view(), name='course-detail'),

    path('review/', ReviewView.as_view(), name='review-list-by-course'),
    path('review/create', ReviewCreateView.as_view(), name='review-create'),

    path('mycourse/', MyCourseListApiView.as_view(), name='mycourse-list'),
    # student-dashboard and student buy courses (My Courses)
    path('mycourse/remove', remove_in_mycourse, name='remove_in_mycourse'),

    path('teacher_course/', TeacherCourse.as_view(), name='teacher-course-list'),  # tacher-dashboard

    path('admin-dashboard/', AdminDashboard.as_view(), name='admin-dashboard'),  # admin-dashboard

]
router = SimpleRouter()

router.register(r'teacher/course', CourseTeacherViewSet, basename='course-teacher')
router.register(r'teacher/section', SectionTeacherViewSet, basename='section-teacher')
router.register(r'teacher/lesson', LessonTeacherViewSet, basename='lesson-teacher')
router.register(r'order', OrderViewSet, basename='order')
router.register(r'order-item', OrderItemViewSet, basename='order-item')


urlpatterns += router.urls