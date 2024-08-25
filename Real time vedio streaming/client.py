import socket, pickle, struct
import cv2


# create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#ipv4,tcp
host_ip = '172.16.2.64'  # server ip address
port = 9999
client_socket.connect((host_ip, port))  # client socket connecting to the server
data = b""#1 byte string type of data #we update the frame into this
payload_size = struct.calcsize("Q") # we accept 8Bytes of data from the server#it calculates the size

#receive data frames
while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4 * 1024)  # packet size is 4kB(1024 byte to 64KB)
        if not packet: break
        data += packet # append the data packet got from server 
    packed_msg_size = data[:payload_size] #find the packed message size (8 byte,packed on the server side)
    data =data[payload_size:] # Actual frame data
     
    msg_size = struct.unpack("Q", packed_msg_size)[0] # meassage size # unpack 
    

    while len(data) < msg_size:
        data += client_socket.recv(4 * 1024) # will receive all frame data from client socket
    frame_data = data[:msg_size] #recover actual frame data
    data =data[msg_size:]
    frame = pickle.loads(frame_data) # de-serialize bytes into actual frame 
    cv2.imshow("RECEIVING VIDEO", frame) #show video frame on client side
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): # press q to exit video 
        break
client_socket.close()


