import json
import os
from django.core.management.base import BaseCommand
from roadmap.models import CourseRoadmap, RoadmapNode, RoadmapResource
from django.conf import settings


class Command(BaseCommand):
    help = 'Seed the database with roadmap data from JSON'

    def handle(self, *args, **kwargs):
        json_path = os.path.join(settings.BASE_DIR, 'roadmap', 'roadmap_data.json')

        if not os.path.exists(json_path):
            self.stderr.write(self.style.ERROR(f"JSON file not found at: {json_path}"))
            return

        with open(json_path, 'r') as f:
            data = json.load(f)

        # Create CourseRoadmap
        roadmap, created = CourseRoadmap.objects.get_or_create(
            title=data['title'],
            defaults={'description': data.get('description', '')}
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Roadmap: {roadmap.title}"))
        else:
            self.stdout.write(self.style.WARNING(f"Roadmap already exists: {roadmap.title}"))

        for node_data in data.get('nodes', []):
            node, created = RoadmapNode.objects.get_or_create(
                node_id=node_data['node_id'],
                roadmap=roadmap,
                defaults={
                    'label': node_data['label'],
                    'description': node_data.get('description', ''),
                    'position_x': node_data.get('position_x', 0),
                    'position_y': node_data.get('position_y', 0)
                }
            )

            # Always update dependencies from JSON
            node.dependencies = node_data.get('dependencies', [])
            node.save()

            if created:
                self.stdout.write(self.style.SUCCESS(f"  Created Node: {node.node_id}"))
            else:
                self.stdout.write(self.style.WARNING(f"  Node already exists: {node.node_id}"))

            for res_data in node_data.get('resources', []):
                res, created = RoadmapResource.objects.get_or_create(
                    title=res_data['title'],
                    url=res_data['url'],
                    node=node,  # Explicitly provide the FK here
                    defaults={
                        'type': res_data.get('type', 'note'),
                        'source': res_data.get('source', 'Unknown')
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"    Linked Resource: {res.title}"))
                else:
                    self.stdout.write(self.style.WARNING(f"    Resource already exists: {res.title}"))

        self.stdout.write(self.style.SUCCESS("\nSeeding complete!"))
