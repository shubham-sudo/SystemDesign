from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView

from .serializers import PersonSerializer, RelationSerializer
from .models import Person, Relation


class PersonAPIView(CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    serializer_class = PersonSerializer

    def get_queryset(self):
        return Person.objects.filter(added_by=self.request.user)


class RelationAPIView(CreateAPIView, ListAPIView):
    serializer_class = RelationSerializer

    def get_queryset(self):
        user = self.request.user
        person = self.kwargs.get("person")
        relation = self.kwargs.get("relation")
        return Relation.objects.filter(
            person__added_by=user,
            person=person,
            relation=relation,
        )


class RelationUpdateAPIView(UpdateAPIView, DestroyAPIView):
    serializer_class = RelationSerializer

    def get_queryset(self):
        user = self.request.user
        return Relation.objects.filter(person__added_by=user)
