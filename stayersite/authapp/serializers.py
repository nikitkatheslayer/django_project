from rest_framework import serializers

from authapp.models import ShopUser


class ShopUsersSerializer(serializers.Serializer):
    # class Meta:
    #     model = ShopUser
    #     username = ShopUser.get_username
    #     email = ShopUser.get_email_field_name
    #     fields = ('username', 'email')

    username = serializers.CharField(max_length=15)
    password = serializers.CharField()
