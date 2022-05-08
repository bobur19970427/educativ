from django.contrib import admin

# Register your models here.
from course import models

admin.site.register(models.Category)
admin.site.register(models.Course)
admin.site.register(models.Whom)
admin.site.register(models.Knowledge)
admin.site.register(models.Lesson)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.Review)
admin.site.register(models.Section)
admin.site.register(models.UserBuy)
admin.site.register(models.Requirement)
