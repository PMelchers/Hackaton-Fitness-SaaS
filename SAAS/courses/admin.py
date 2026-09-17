from django.contrib import admin

from .models import Course, CourseType


@admin.register(CourseType)
class CourseTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "availability")
    filter_horizontal = ("customers",)
