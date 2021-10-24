from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **other_fields):
        if not username:
            raise ValueError("dude username is required")

        user = self.model(username=username, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, *args, **kwargs):
        return NotImplemented


class User(AbstractBaseUser):
    username = models.CharField(max_length=120, unique=True)
    creationDate = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.id)


class RelationEnum(models.TextChoices):
    SIBLING = "sibling"
    PARENT = "parent"
    CHILD = "child"
    COUSIN = "cousin"
    GRANDPARENT = "grandparent"
    GRANDCHILD = "grandchild"


class Relation(models.Model):
    person = models.ForeignKey("Person", on_delete=models.PROTECT)
    relative = models.ForeignKey("Person", on_delete=models.PROTECT, related_name="relative")
    relation = models.CharField(choices=RelationEnum.choices, max_length=12, default=RelationEnum.SIBLING.value)


class Person(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    phone_number = models.IntegerField()
    email_address = models.EmailField(blank=True)
    address = models.CharField(max_length=250, blank=True)
    birth_date = models.DateTimeField()  # Required to perform validation child_dob > parent_dob
    relations = models.ManyToManyField("Person", through="Relation")
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="families")

    def __str__(self):
        return str(f"{self.first_name} {self.last_name}")
