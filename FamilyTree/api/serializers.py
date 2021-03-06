from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import Person, Relation, RelationEnum, User


RELATIONS = {
    "sibling": "sibling",
    "parent": "child",
    "child": "parent",
    "grandparent": "grandchild",
    "cousin": "cousin",
}


class PersonSerializer(serializers.ModelSerializer):
    added_by = serializers.HiddenField(default=serializers.CurrentUserDefault(), write_only=True)

    class Meta:
        model = Person
        fields = (
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "email_address",
            "address",
            "birth_date",
            "added_by",
        )

    def validate_phone_number(self, number):
        if len(str(number)) < 10:
            raise ValidationError("Phone Number not valid")

        num_count = sum(num.isdigit() for num in str(number))

        if num_count < 10 or num_count > 12:
            raise ValidationError("Phone Number not valid")

        return number


class PersonRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return Person.objects.filter(added_by=self.context.get("request").user)


class RelationSerializer(serializers.ModelSerializer):
    person = PersonRelatedField()
    relative = PersonSerializer()
    relation = serializers.ChoiceField(RelationEnum.choices)

    class Meta:
        model = Relation
        fields = ("id", "person", "relative", "relation")

    def create(self, validated_data):
        relative_data = validated_data.pop("relative")
        relative = Person.objects.create(**relative_data)
        relation = validated_data.pop("relation")
        person = validated_data.pop("person")
        Relation.objects.create(person=relative, relative=person, relation=RELATIONS[relation])
        relation = Relation.objects.create(person=person, relative=relative, relation=relation)
        return relation


class SignUpSerializer(serializers.ModelSerializer):
    token = serializers.SlugRelatedField(source="auth_token", slug_field="key", read_only=True)

    class Meta:
        model = User
        fields = ("username", "password", "token")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, data):
        user = User.objects.create_user(data["username"], data["password"])
        return user
