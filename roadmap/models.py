from django.db import models
from django.utils import timezone


class CourseRoadmap(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class RoadmapNode(models.Model):
    roadmap = models.ForeignKey(CourseRoadmap, on_delete=models.CASCADE, related_name='nodes')
    node_id = models.CharField(max_length=100, unique=True)
    label = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    position_x = models.FloatField(default=0)
    position_y = models.FloatField(default=0)
    dependencies = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.label


class RoadmapEdge(models.Model):
    from_node = models.ForeignKey(RoadmapNode, on_delete=models.CASCADE, related_name='out_edges')
    to_node = models.ForeignKey(RoadmapNode, on_delete=models.CASCADE, related_name='in_edges')

    def __str__(self):
        return f"{self.from_node} -> {self.to_node}"


class RoadmapResource(models.Model):
    RESOURCE_TYPE_CHOICES = [
        ('article', 'Article'),
        ('video', 'Video'),
        ('book', 'Book'),
        ('course', 'Course'),
        ('docs', 'Documentation'),
        ('other', 'Other'),
    ]

    node = models.ForeignKey(RoadmapNode, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200)
    url = models.URLField()
    type = models.CharField(max_length=20, choices=RESOURCE_TYPE_CHOICES)
    source = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title
