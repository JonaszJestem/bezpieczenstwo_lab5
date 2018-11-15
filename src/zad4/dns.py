import socket

UDP_IP = "192.168.0.1"
UDP_PORT = 53
MESSAGE = "4fa28180000100020000000103777777086d79646f6d61696e03636f6d0000010001c00c00050001000002580002c010c0100001000100000258000441fef2b40000290200000000000000"

def fake_dns_response():
    print("UDP target IP:", UDP_IP)
    print("UDP target port:", UDP_PORT)
    print("message:", MESSAGE)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes.fromhex(MESSAGE), (UDP_IP, UDP_PORT))

fake_dns_response()