import datetime
import timedelta
from django.db import models

# Create your models here.
from accounts.models import User
from config.utils import generate_unique_slug


def get_category(instance, filename):
    return "categories/%s" % (filename)


def get_course(instance, filename):
    return "courses/%s" % (filename)


def get_lesson(instance, filename):
    return "lessons/%s" % (filename)


class Category(models.Model):
    name = models.CharField(max_length=255, blank=False, null=True)
    image = models.ImageField(upload_to=get_category, default='categories/default.png', blank=True, null=True)
    video = models.FileField(upload_to=get_category, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, unique=True, max_length=250)
    order = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    description = models.CharField(max_length=1000, blank=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            if len(self.name) > 0:
                self.slug = generate_unique_slug(self, 'name')
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "/categories/%s/" % self.slug


class Course(models.Model):
    TYPE_CHOICES = (
        ('easy', "Easy"),
        ('medium', "Medium"),
        ('difficult', "Difficult"),
    )
    name = models.CharField(max_length=255, blank=False, null=True)
    description = models.TextField(max_length=1000, blank=False, null=True)
    image = models.ImageField(upload_to=get_course, default='courses/default.png')
    video = models.FileField(upload_to=get_course, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, unique=True, max_length=250)
    author = models.ForeignKey(User, related_name='author_courses', on_delete=models.DO_NOTHING, null=True, blank=True)
    status = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    difficulty = models.CharField(choices=TYPE_CHOICES, max_length=255, default='easy')
    category = models.ForeignKey(Category, related_name='category', on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            if len(self.name) > 0:
                self.slug = generate_unique_slug(self, 'name')
        super(Course, self).save(*args, **kwargs)

    def hasPermission(self, user_id):
        return self.course_buy.filter(user_id=user_id, end_date__gt=datetime.datetime.now()).exists()

    def get_absolute_url(self):
        return "/categories/%s/%s/" % (self.slug, self.slug)


class Whom(models.Model):
    name = models.CharField(max_length=255, blank=False, null=True)
    description = models.CharField(max_length=1000, blank=False, null=True)
    course = models.ManyToManyField(Course, related_name='whoms', )
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Requirement(models.Model):
    name = models.CharField(max_length=255, blank=False, null=True)
    description = models.CharField(max_length=1000, blank=False, null=True)
    course = models.ManyToManyField(Course, related_name='requiremnts', )
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Knowledge(models.Model):
    name = models.CharField(max_length=255, blank=False, null=True)
    course = models.ManyToManyField(Course, related_name='knowledges',)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=255, blank=False, null=True)
    description = models.CharField(max_length=1000, blank=False, null=True)
    course = models.ForeignKey(Course, related_name='sections', on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(blank=True, null=True, unique=True, max_length=250)
    status = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            if len(self.name) > 0:
                self.slug = generate_unique_slug(self, 'name')
        super(Section, self).save(*args, **kwargs)

    class Meta(object):
        ordering = ['order']


class Lesson(models.Model):
    name = models.CharField(max_length=255, blank=False, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True, default='')
    content = models.TextField(blank=True, null=True, default='')
    file = models.FileField(upload_to=get_lesson, blank=True, null=True)
    section = models.ForeignKey(Section, blank=True, null=True, related_name='lessons', on_delete=models.SET_NULL)
    course = models.ForeignKey(Course, blank=True, null=True, related_name='lessons', on_delete=models.SET_NULL)
    status = models.BooleanField(default=True)
    is_demo = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    duration = models.FloatField(default=0)
    slug = models.SlugField(blank=True, null=True, unique=True, max_length=250)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.name)
    def save(self, *args, **kwargs):
        if not self.slug:
            if len(self.name) > 0:
                self.slug = generate_unique_slug(self, 'name')
        super(Lesson, self).save(*args, **kwargs)

    def hasPermission(self, user_id):
        if self.is_demo == 1:
            return True
        return self.section.course.course_buy.filter(user_id=user_id, end_date__gt=datetime.datetime.now()).exists()


class Review(models.Model):
    comment = models.TextField(max_length=255, blank=False, null=True)
    rating = models.IntegerField(default=5)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.DO_NOTHING)
    # lesson = models.ForeignKey(Lesson, related_name='reviews', null=True, blank=True, on_delete=models.DO_NOTHING)
    course = models.ForeignKey(Course, related_name='reviews', null=True, blank=True, on_delete=models.DO_NOTHING)
    # is_home = models.BooleanField(verbose_name="is home", default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.comment)


class UserBuy(models.Model):
    user = models.ForeignKey(User, related_name='user_buy', on_delete=models.DO_NOTHING)
    course = models.ForeignKey(Course, related_name='course_buy', on_delete=models.SET_NULL, null=True, blank=True)
    duration = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    code_sum = models.FloatField(default=0)
    description = models.CharField(max_length=1000, blank=True, null=True, default='')
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.description

    def is_buy(self, obj):
        if self.context['request'].user.is_anonymous:
            return 0
        buy = UserBuy.objects.filter(course=obj, user=self.context['request'].user,
                                     end_date__gt=datetime.datetime.now()).count()
        if buy >= 1:
            return 1
        else:
            return 0


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', "Pending"),
        ('accept', "Accept"),
        ('error', 'Payment error')
    )
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="myorders")
    comment = models.CharField(default='', max_length=1000, null=True)
    payment_url = models.CharField(default='', blank=True, max_length=1000, null=True)
    total = models.FloatField(blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, default='pending', max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.user.username


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', blank=False, null=False, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, blank=False, null=False, on_delete=models.CASCADE)
    price = models.FloatField(blank=True, null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.course.name
