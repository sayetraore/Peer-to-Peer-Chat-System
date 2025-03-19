import sys
import socket
import json
import threading

def rcv_msg(sock, expected_seq):
    while True:
        try:
            data, addr = sock.recvfrom(2048)
            msg = json.loads(data.decode())

            # Check if sequence number matches expected
            if msg.get("Seq. num") == expected_seq[0]:
                print(f"{msg.get('UID')}>>{msg.get('Message')}")
                expected_seq[0] += 1
            # no match=> packet is dropped
        except:
            pass

def main():
    if len(sys.argv) != 4:
        sys.exit(1)

    username = sys.argv[1]
    src = sys.argv[2]
    dest = sys.argv[3]

    # retrieve src ip and src port to integers
    try:
        src_ip, src_port = src.split(':')
        src_port = int(src_port)
    except:
        sys.exit(1)

    # retrieve destination IP and port to integers
    try:
        dest_ip, dest_port = dest.split(':')
        dest_port = int(dest_port)
    except:
        sys.exit(1)

    # Create a UDP socket and bind it to the source IP and port using txtbook 2.7eg
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind((src_ip, src_port))
    except:
        sys.exit(1)

    # print username
    print(username)

    # Initialize the expected sequence number
    expected_seq = [0]

    # Start thread for rcv_msg
    receiver_thread = threading.Thread(
        target=rcv_msg, args=(sock, expected_seq), daemon=True
    )
    receiver_thread.start()

    # Initialize the sequence number to be incrremented
    seq = 0

    # Read message from the user and send it to the destination
    while True:
        try:
            message = input(f"{username}>> ")
            infoDict = {
                "Version": "v1",
                "Seq. num": seq,
                "UID": username,
                "DID": dest,  
                "Message": message[:1024]
            }
            json_data = json.dumps(infoDict).encode()
            sock.sendto(json_data, (dest_ip, dest_port))
            seq += 1
        except:
            # don't do anything
            pass

if __name__ == "__main__":
    main()

