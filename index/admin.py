from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Product, Blog, Team, Comments


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'price', 'image')
    search_fields = ('id', 'name')
    ordering = ('id',)


@admin.register(Blog)
class BlogAdmin(ImportExportModelAdmin):
    list_display = ('id', 'title', 'author')
    search_fields = ('id', 'title')
    ordering = ('id',)


@admin.register(Team)
class TeamAdmin(ImportExportModelAdmin):
    list_display = ('id', 'first_name', 'last_name')
    search_fields = ('id', 'first_name', 'last_name')
    ordering = ('id', )


@admin.register(Comments)
class TeamAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user', )
    search_fields = ('id', )
    ordering = ('id', )