from rest_framework import mixins, viewsets

from .models import Content
from .serializers import ContentSerializer


class ContentViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Content.objects.all()
    lookup_field = 'key'
    serializer_class = ContentSerializer
