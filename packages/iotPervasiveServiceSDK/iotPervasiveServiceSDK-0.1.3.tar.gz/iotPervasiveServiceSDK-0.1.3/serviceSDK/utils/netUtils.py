import subprocess
import platform


def getBssid():
  if platform.system() == "Windows":
    # Run the netsh command to get the BSSID of the connected WiFi network
    output = subprocess.check_output(["netsh", "wlan", "show", "interfaces"])
    # Extract the BSSID from the output
    return output.decode("gbk").split("BSSID")[1].split()[1]
  elif platform.system() == "Linux":
    # Run the iwconfig command to get the BSSID of the connected WiFi network
    output = subprocess.check_output(["iwconfig"])
    # Extract the BSSID from the output
    return output.decode().split("Access Point: ")[1].split()[0]


def getIPAndMac():
  import netifaces

  # Get the IP address and MAC address of the default network interface
  default_interface = netifaces.gateways()['default'][netifaces.AF_INET][1]
  addresses = netifaces.ifaddresses(default_interface)[netifaces.AF_INET]

  # Find the first non-loopback IP address
  ip_address = next((addr['addr'] for addr in addresses if not addr['addr'].startswith('127.')), None)

  # Get the MAC address
  mac_address = netifaces.ifaddresses(default_interface)[netifaces.AF_LINK][0]['addr']

  return ip_address, mac_address


def getNetInfo():
  ip, mac = getIPAndMac()
  bssid = getBssid()
  return ip, mac, bssid
    
