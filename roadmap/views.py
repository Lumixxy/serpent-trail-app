from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics, serializers
from .models import CourseRoadmap, RoadmapNode, RoadmapResource
from .serializers import CourseRoadmapSerializer, RoadmapNodeSerializer, RoadmapResourceSerializer

from drf_spectacular.utils import extend_schema, OpenApiExample


# === Swagger Request Schemas ===

class RoadmapCreateSchema(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()

class NodeCreateSchema(serializers.Serializer):
    roadmap = serializers.IntegerField()
    title = serializers.CharField()
    content = serializers.CharField()
    parent_node = serializers.CharField(required=False, allow_null=True)

class ResourceCreateSchema(serializers.Serializer):
    node = serializers.CharField()
    title = serializers.CharField()
    url = serializers.URLField()
    type = serializers.ChoiceField(choices=["video", "article", "book"])


# === Roadmap ===

class AllCourseRoadmapsView(generics.ListAPIView):
    queryset = CourseRoadmap.objects.all()
    serializer_class = CourseRoadmapSerializer


class CourseRoadmapByTitleView(generics.RetrieveAPIView):
    serializer_class = CourseRoadmapSerializer
    lookup_field = 'title'

    def get_queryset(self):
        return CourseRoadmap.objects.all()


@extend_schema(
    request=RoadmapCreateSchema,
    responses={201: CourseRoadmapSerializer},
    examples=[
        OpenApiExample(
            "Example Roadmap",
            value={"title": "Python Fundamentals", "description": "Introductory Python course"}
        )
    ]
)
@api_view(['POST'])
def create_roadmap(request):
    serializer = CourseRoadmapSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def update_delete_roadmap(request, roadmap_id):
    try:
        roadmap = CourseRoadmap.objects.get(id=roadmap_id)
    except CourseRoadmap.DoesNotExist:
        return Response({"error": "Roadmap not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = CourseRoadmapSerializer(roadmap, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        roadmap.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# === Node ===

@extend_schema(
    request=NodeCreateSchema,
    responses={201: RoadmapNodeSerializer},
    examples=[
        OpenApiExample(
            "Example Node",
            value={
                "roadmap": 1,
                "title": "Variables and Data Types",
                "content": "Learn about variables in Python.",
                "parent_node": None
            }
        )
    ]
)
@api_view(['POST'])
def create_node(request):
    serializer = RoadmapNodeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def update_delete_node(request, node_id):
    try:
        node = RoadmapNode.objects.get(node_id=node_id)
    except RoadmapNode.DoesNotExist:
        return Response({"error": "Node not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = RoadmapNodeSerializer(node, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        node.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def node_resources(request, node_id):
    try:
        node = RoadmapNode.objects.get(node_id=node_id)
    except RoadmapNode.DoesNotExist:
        return Response({"error": "Node not found"}, status=status.HTTP_404_NOT_FOUND)

    resources = node.resources.all()
    serializer = RoadmapResourceSerializer(resources, many=True)
    return Response(serializer.data)


# === Resource ===

@extend_schema(
    request=ResourceCreateSchema,
    responses={201: RoadmapResourceSerializer},
    examples=[
        OpenApiExample(
            "Example Resource",
            value={
                "node": "abc123",
                "title": "Python Basics Video",
                "url": "https://youtube.com/example",
                "type": "video"
            }
        )
    ]
)
@api_view(['POST'])
def create_resource(request):
    serializer = RoadmapResourceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def update_delete_resource(request, resource_id):
    try:
        resource = RoadmapResource.objects.get(id=resource_id)
    except RoadmapResource.DoesNotExist:
        return Response({"error": "Resource not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = RoadmapResourceSerializer(resource, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        resource.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
