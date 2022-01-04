from django.contrib.auth.models import Permission, User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    user_permissions = serializers.SlugRelatedField(many=True, read_only=True, slug_field="codename")

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "is_staff",
            "is_superuser",
            "user_permissions",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if representation["is_superuser"]:
            representation["user_permissions"].extend(Permission.objects.all().values_list("codename", flat=True))
        else:
            for group in User.objects.get(username=representation["username"]).groups.all():
                representation["user_permissions"].extend(group.permissions.values_list("codename", flat=True))

        return representation



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["user"] = UserSerializer(user).data

        return token
