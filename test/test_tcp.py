#!/usr/bin/env ipython

FAKE_IP = "10.0.4.4"
MAC_ADDR = "60:67:20:eb:7b:bc"
from scapy.all import send, Ether, ARP
import sys
import os
from unittest.case import SkipTest
from logging_tcp_socket import LoggingTCPSocket
import time
import tcp
from tcp_listener import TCPListener

# The tests can't run as not-root
RUN = True
try:
    for _ in range(4):
        send(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(psrc=FAKE_IP, hwsrc=MAC_ADDR))
except:
    RUN = False


google_ip = "173.194.43.39"
listener = TCPListener(FAKE_IP)

def test_connect_google():
    if not RUN: raise SkipTest
    conn = LoggingTCPSocket(listener)

    conn.connect(google_ip, 80)
    time.sleep(2)
    conn.close()
    time.sleep(2)
    assert conn.state == "CLOSED"
    assert len(conn.received_packets) == 2
    assert conn.states == ["CLOSED", "SYN-SENT", "ESTABLISHED", "FIN-WAIT-1", "CLOSED"]

def test_get_google_homepage():
    if not RUN: raise SkipTest
    payload = "GET / HTTP/1.0\r\n\r\n"
    conn = LoggingTCPSocket(listener)

    conn.connect(google_ip, 80)
    time.sleep(2)
    conn.send(payload)
    time.sleep(3)
    conn.close()
    time.sleep(3)

    data = conn.recv()
    assert "google" in data

