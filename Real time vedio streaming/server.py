# This code is for the server
# Lets import the libraries
import socket
import cv2#computer vision,for capturing the vedio(image processing)
import  pickle
import struct
import imutils

# Socket Create
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)#server will listen to that ip and the particular port number



server_socket.bind(socket_address)# Socket Bind


server_socket.listen(5)
print("LISTENING AT:", socket_address)# Socket Listen



while True:
    client_socket, addr = server_socket.accept()#accept client connection with accept method#will return the client addr and the port
    print('GOT CONNECTION FROM:', addr)
    if client_socket:
        vid = cv2.VideoCapture(0)#for vedio capturing from the cam->vedioacpture method ; and is stored into  vid

        while (vid.isOpened()):
            img, frame = vid.read()
            frame = imutils.resize(frame, width=320)
            a = pickle.dumps(frame) #serialize frame to bytes#string type
            message = struct.pack("Q", len(a)) + a # pack the serialized data(byte data)#Q->unsigned long long int(8B data)
            
            try:
                client_socket.sendall(message) #send message or data frames to client by using sendall
            except Exception as e:
                print(e)
                raise Exception(e)#if any exception is there then exception is raised


            cv2.imshow('TRANSMITTING VIDEO', frame) #show video frame on server side and the frame name is Transmitting vedio
            key = cv2.waitKey(1) #& 0xFF
            if key == ord('q'):# press q for quiting 
                 client_socket.close() 