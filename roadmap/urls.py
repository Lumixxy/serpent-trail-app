from django.urls import path
from .views import (
    AllCourseRoadmapsView,
    create_roadmap,
    update_delete_roadmap,
    CourseRoadmapByTitleView,
    create_node,
    update_delete_node,
    node_resources,
    create_resource,
    update_delete_resource
)

urlpatterns = [
    # Course Roadmap Endpoints
    path('roadmap/', AllCourseRoadmapsView.as_view(), name='roadmap_list'),
    path('roadmap/create/', create_roadmap, name='create_roadmap'),
    path('roadmap/<int:roadmap_id>/', update_delete_roadmap, name='update_delete_roadmap'),
    path('roadmap/<str:title>/', CourseRoadmapByTitleView.as_view(), name='roadmap_by_title'),

    # Node Endpoints
    path('roadmap/node/create/', create_node, name='create_node'),
    path('roadmap/node/<str:node_id>/', update_delete_node, name='update_delete_node'),
    path('roadmap/node/<str:node_id>/resources/', node_resources, name='roadmap_node_resources_list'),

    # Resource Endpoints
    path('roadmap/node/resource/create/', create_resource, name='create_resource'),
    path('roadmap/node/resource/<int:resource_id>/', update_delete_resource, name='update_delete_resource'),
]
