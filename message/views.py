from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from message.serializers import MessageSerializer
from message.models import Message

class MessageView(APIView):
    def post(self, request, check):
        message_serializer = MessageSerializer(data = request.data)
        if message_serializer.is_valid():
            message_serializer.save(sender = request.user)
            return Response({"message":"전송완료"},status=status.HTTP_200_OK)
        return Response(message_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, check):
        me = request.user
        
        if check:
            sended_message = me.sended_message.all().order_by('-id')
            sended_message_serializer = MessageSerializer(sended_message, many= True)
            return Response(sended_message_serializer.data, status=status.HTTP_200_OK)
        else:
            received_message = me.received_message.all().order_by('-id')
            received_message_serializer = MessageSerializer(received_message, many= True)
            return Response(received_message_serializer.data, status=status.HTTP_200_OK)
        
class DetailMessageView(APIView):
    def delete(self, request, message_id):
        message = Message.objects.get(id=message_id)
        if request.user == message.receiver:
            message.delete_receiver = True
            message.save()
            
        elif request.user == message.sender:
            message.delete_sender = True
            message.save()
             
        if message.delete_receiver and message.delete_sender: #받은 사람과 보낸 사람이 모두 삭제하면 db 삭제
            if request.user == message.receiver or request.user == message.sender:
                message.delete()
                return Response({"message":"삭제 완료"},status=status.HTTP_204_NO_CONTENT)
            return Response({"message":"권한이 없음"},status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({"message":"삭제 완료"},status=status.HTTP_200_OK)
       