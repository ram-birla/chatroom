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
            c = []
            cameraip = req.POST['cameraip'+str(i)] 
            cameraframe = req.POST['cameraframe'+str(i)]
            print(cameraip,cameraframe)
            # c['cameraip'+str(i)] = cameraip
            # c['cameraframe'+str(i)] = cameraframe
            c.append(cameraip)
            c.append(cameraframe)
            camera['cam'+str(i)] = c
        print(camera)
        

        ws = websocket.WebSocket()
        ws.connect("ws://52.90.40.194/ws/chat/python/")
        print("Sending")
        result = json.dumps(camera) 
  
        ws.send(json.dumps({"message":result,"id":4,"message_type":0}))
    return HttpResponse("SENDING TO CHAT SERVER")
