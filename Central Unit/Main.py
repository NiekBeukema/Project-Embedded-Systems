from UnoNetworking import UnoNetworkController
import time

controller = UnoNetworkController();

controller.connect()

print(controller.getTemp())



