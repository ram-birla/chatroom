import websocket
import json

ws = websocket.WebSocket()
ws.connect("ws://localhost:8000/ws/chat/python/")
print("recieveing")
result =  ws.recv()
print(result)
final_dictionary = json.loads(result) 
print(final_dictionary)
with open('data.txt','w') as outfile:
    json.dump(final_dictionary['message'],outfile)