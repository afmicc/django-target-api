from rest_framework import mixins, permissions, viewsets

from .models import Topic
from .serializers import TargetSerializer, TopicSerializer
from .services import TargetMatchingService


class TargetViewSet(viewsets.ModelViewSet):
    serializer_class = TargetSerializer
    permission_classes = [permissions.IsAuthenticated]

    matching_service = TargetMatchingService()

    def perform_create(self, serializer):
        target = serializer.save(owner=self.request.user)

        self.matching_service.process_target(target)

    def get_queryset(self):
        return self.request.user.target_set.all()


class TopicViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAuthenticated]
