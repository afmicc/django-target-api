from rest_framework import mixins, viewsets

from .models import Contact
from .serializers import ContactSerializer


class ContactViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(writer=self.request.user)
        else:
            super().perform_create(serializer)
