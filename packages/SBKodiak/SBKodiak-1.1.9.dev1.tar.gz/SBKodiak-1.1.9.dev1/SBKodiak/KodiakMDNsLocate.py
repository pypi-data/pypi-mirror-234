import time
from zeroconf import ServiceBrowser, Zeroconf
import socket
from .KodiakGlobals import KodiakGlobals


class MyListener:
    def __init__(self):
        self.found_ip_addresses = []
    #
    # def remove_service(self, zeroconf, type, name):
    #     print(f"Service {name} removed")

    def add_service(self, zeroconf, type, name):
        """
        Overriding the add service method to get and add the kodiak IP addresses that were discovered over MDNs

        Args:
            zeroconf: ZeroConf service object
            type: Type you're looking for (kodiak's response)
            name: Name of the object

        Returns:
            Nothing
            But adds the found IPaddress to a list which can be accessed elsewhere
        """
        info = zeroconf.get_service_info(type, name)
        if info:
            # print(f"Service {name} added, service info: {info}")
            ip_addr = socket.inet_ntoa(info.addresses[0])
            # print(ip_addr)
            self.found_ip_addresses.append(ip_addr)

    def update_service(self):
        """
        Adding to stop the mdns warning message about this 'soon to be necessary' function.

        Returns:
            N/A
        """
        pass


def find_kodiak_ip_addresses(runtime=1):
    """
    Function to get the IPAddresses of the kodiaks discovered via MDNS

    Args:
        runtime: Time to wait for discovery

    Returns:
        List - List of IPAddresses (strings)

    """

    zeroconf = Zeroconf()
    listener = MyListener()

    browser = ServiceBrowser(zeroconf, KodiakGlobals.kodiak_mdns_locator, listener)

    try:
        time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        zeroconf.close()

    return listener.found_ip_addresses
    # print(listener.found_ip_addresses)

# find_kodiak_ip_addresses()