from django.contrib import admin
from .models import CourseRoadmap, RoadmapNode, RoadmapEdge, RoadmapResource

@admin.register(CourseRoadmap)
class CourseRoadmapAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at']
    search_fields = ['title']
    ordering = ['created_at']

@admin.register(RoadmapNode)
class RoadmapNodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'label', 'node_id', 'roadmap']
    list_filter = ['roadmap']
    search_fields = ['label', 'node_id']
    ordering = ['roadmap', 'node_id']

@admin.register(RoadmapEdge)
class RoadmapEdgeAdmin(admin.ModelAdmin):
    list_display = ['id', 'from_node', 'to_node']
    search_fields = ['from_node__label', 'to_node__label']

@admin.register(RoadmapResource)
class RoadmapResourceAdmin(admin.ModelAdmin):
    list_display = ['id', 'node', 'title', 'type', 'source']
    list_filter = ['type']
    search_fields = ['title', 'source']
    ordering = ['node']
