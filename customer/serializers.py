from customer.models import Customer

from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True, required=True)

    class Meta:
        model = Customer
        fields = ['username', 'password', 'first_name', 'last_name', 'age', 'email', 'number',
                  'aadhaar', 'pan_card', 'address', 'date_of_birth']
        extra_kwargs = {
            'number': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
        }

    def create(self, validated_data):
        return Customer.objects.create_user(**validated_data)
