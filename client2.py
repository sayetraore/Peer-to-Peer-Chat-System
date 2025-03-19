import sys
import socket
import json
import threading
import time

def rdt_rcv(sock):
    data, addr = sock.recvfrom(2048)
    return data, addr

def isNAK(rcvpkt):
    #always false for this part
    return False

def udt_send(sock, sndpkt, dest_addr):
    sock.sendto(sndpkt, dest_addr)

def rcv_msg(sock, expected_seq):
    while True:
    
            data, addr = rdt_rcv(sock)
            if isNAK(data):
                continue

            msg = json.loads(data.decode())
            if msg.get("Seq. num") == expected_seq[0]:
                print(f"{msg.get('UID')}>>{msg.get('Message')}")
                expected_seq[0] += 1
    
            pass

def main():
    username    = sys.argv[1]
    src         = sys.argv[2]
    target_user = sys.argv[3]
    dir_service = sys.argv[4]

    # Parse src ip and port get in int form

    src_ip, src_port = src.split(':')
    src_port = int(src_port)

    # Parse dirservice IP and port get in int form

    dir_ip, dir_port = dir_service.split(':')
    dir_port = int(dir_port)

    chat_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    chat_socket.bind((src_ip, src_port))

    # Print username 
    print(username)

    destination_ip = ""
    destination_port = 0

    # Register phase
    while True:
        register_data = {
            "UID": username,
            "user IP": src_ip,
            "user PORT": src_port,
            "target user": target_user
        }
        try:
    
            udt_send(chat_socket, json.dumps(register_data).encode(), (dir_ip, dir_port))

            response_data, _ = chat_socket.recvfrom(2048)
            response = json.loads(response_data.decode())

            if response.get("error code") == 400:
                destination_ip = response.get("destination IP")
                destination_port = response.get("destination port")
                break
            else:
                # Wait 5 seconds and retry
                time.sleep(5)
        except:
            # Wait 5 seconds and retry
            time.sleep(5)

    # Chat
    expected_seq = [0]
    receiver_thread = threading.Thread(target=rcv_msg, args=(chat_socket, expected_seq), daemon=True)
    receiver_thread.start()

    seq = 0
    while True:
        try:
            message = input(f"{username}>> ")
            data_dict = {
                "Version": "v1",
                "Seq. num": seq,
                "UID": username,
                "DID": target_user,  # Destination ID
                "Message": message[:1024]
            }
            json_data = json.dumps(data_dict).encode()
            udt_send(chat_socket, json_data, (destination_ip, destination_port))
            seq += 1
        except:
            pass

if __name__ == "__main__":
    main()
