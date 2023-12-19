from rest_framework import serializers
from authentication.models import CustomUser
from chatapp.models import GroupMessage, PlayerInformation

class chatSerializer(serializers.ModelSerializer):
    sender_email = serializers.SerializerMethodField()

    class Meta:
        model = GroupMessage
        fields = '__all__'

    def get_sender_email(self, obj):
        if obj.sender:
            return obj.sender.email
        return None

class playerSerializer(serializers.ModelSerializer):
    height=serializers.IntegerField(default=0.0)
    weight=serializers.IntegerField(default=0.0)

    class Meta:
        model = PlayerInformation
        fields = '__all__'