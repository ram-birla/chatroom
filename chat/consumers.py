import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

database={}
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.person_name = self.scope['url_route']['kwargs']['person_name']
        self.room_group_name = 'chat_%s' % self.room_name  

        if self.room_name in database:
            if database[self.room_name]==2:
                return
            else: database[self.room_name]+=1
        else:database[self.room_name]=1   
        print(database)                
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
            )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        if self.room_name in database:database[self.room_name]-=1

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        message_type = text_data_json['message_type']
        print(message)
        wid=text_data_json['id']
        print(wid)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'id':wid,
                'message': message,
                'message_type':message_type,
                # "person_name": self.person_name
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        message_type = event['message_type']
        # person_name = event['person_name']
        wid = event['id']
        print(message)
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'id':wid,
            'message_type': message_type,
            # 'person_name': person_name
        }))
