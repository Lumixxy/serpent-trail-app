from rest_framework import serializers
from .models import CourseRoadmap, RoadmapNode, RoadmapResource
import uuid


class RoadmapResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadmapResource
        fields = ['id', 'title', 'url', 'type', 'source']


class RoadmapNodeSerializer(serializers.ModelSerializer):
    resources = RoadmapResourceSerializer(many=True, read_only=True)

    class Meta:
        model = RoadmapNode
        fields = [
            'node_id',
            'label',           # ✅ Changed from 'title' to 'label'
            'description',
            'position_x',
            'position_y',
            'dependencies',  # <-- add this line
            'resources',
        ]
        read_only_fields = ['node_id', 'label']

    def create(self, validated_data):
        validated_data['node_id'] = uuid.uuid4()
        return super().create(validated_data)


class CourseRoadmapSerializer(serializers.ModelSerializer):
    nodes = RoadmapNodeSerializer(many=True, read_only=True)

    class Meta:
        model = CourseRoadmap
        fields = ['id', 'title', 'description', 'created_at', 'nodes']
