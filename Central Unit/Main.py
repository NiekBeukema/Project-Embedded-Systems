from UnoNetworking import UnoNetworkController
import time

controller = UnoNetworkController();

controller.connect()
controller.getType()
print(controller.getTemp())



