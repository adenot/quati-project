import sys


import Sensor


"""@package quati
This is the quati package


@title Monitor the network
@goal Probe the network, sniffing the packets and logging them
@context A network that System is connected in
@actor System, Sensor, Pcap
@resource Network
@episode Initialize Sensor
@episode Sniff Network
@episode Parse Network Packet



"""

__all__ = ["Sensor", "pcapy", "Sniffer"]

