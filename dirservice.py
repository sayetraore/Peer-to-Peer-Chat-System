import sys
import socket
import json

def main():
    if len(sys.argv) != 3:
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        server_socket.bind((server_ip, server_port))
    except:
        sys.exit(1)

    user_dict = {}  # {user_id: (user_ip, user_port)}

    while True:
        try:
            data, addr = server_socket.recvfrom(2048)
            request = json.loads(data.decode())

            user_id     = request.get("UID")
            user_ip     = request.get("user IP")
            user_port   = request.get("user PORT")
            target_user = request.get("target user")

            
            user_dict[user_id] = (user_ip, user_port)

            # response
            if target_user in user_dict:
                dest_ip, dest_port = user_dict[target_user]
                response = {
                    "error code": 400,
                    "destination IP": dest_ip,
                    "destination port": dest_port
                }
            else:
                response = {
                    "error code": 600,
                    "destination IP": "",
                    "destination port": 0
                }

            server_socket.sendto(json.dumps(response).encode(), addr)
        except:
            pass

if __name__ == "__main__":
    main()
