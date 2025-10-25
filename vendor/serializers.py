from rest_framework import serializers
from vendor.models import Vendor, VendorRequest

class VendorRequestSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = VendorRequest
        fields = ['id', 'user', 'user_email', 'message', 'is_approved', 'created_at']
        read_only_fields = ['is_approved', 'created_at']
