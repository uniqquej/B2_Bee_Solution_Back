from rest_framework import serializers
from message.models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id","title","content","receiver","created_at","sender","delete_receiver","delete_sender"]
        read_only_fields = ["created_at","sender","id","delete_receiver","delete_sender"]
        