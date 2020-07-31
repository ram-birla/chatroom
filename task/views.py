from django.shortcuts import render,redirect
from django.http import HttpResponse
import websocket
import json

def index(req):
    return render(req,'indx.html')

def accept(req):
    if req.method == 'POST':
        number = int(req.POST['devices'])
        print(number)
        camera = {}
        for i in range(1,number+1):
            cameraip = req.POST['cameraip'+str(i)] 
            print(cameraip)
            camera['cameraip'+str(i)] = cameraip
        print(camera)

        ws = websocket.WebSocket()
        ws.connect("ws://172.31.84.9:8000/ws/chat/python/")
        print("Sending")
        result = json.dumps(camera) 
  
        ws.send(json.dumps({"message":result,"id":4,"message_type":0}))
    return HttpResponse("SENDING TO CHAT SERVER")
