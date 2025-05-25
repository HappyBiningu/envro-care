from rest_framework import serializers
from users.models import CustomUser
from rest_framework.validators import UniqueValidator

class CustomUserSerializer(serializers.ModelSerializer):
    """ Serializer for custom user model. Turning user data to json """
    password =serializers.CharField(write_only=True, required=True)
    full_name = serializers.SerializerMethodField(read_only=True)

    email = serializers.EmailField(validators=[UniqueValidator(queryset=CustomUser.objects.all())])

    def get_full_name(self, obj):
        try:
            return f"{obj.first_name} {obj.last_name}"
        except Exception as e:
            return None

    class Meta:
        model = CustomUser
        exclude = ["groups", "last_login", "date_joined", "user_permissions"]

    def create(self, validated_data):
        """ Overriding create method to create a user via APIs properly """
        return CustomUser.objects.create_user(**validated_data)

class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["username", "last_name", "first_name", "id", "email"]