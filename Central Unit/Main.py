from UnoNetworking import UnoNetworkController
import time

controller = UnoNetworkController();

controller.connect()
print(controller.getType())
#print(controller.rollOut(88))
print(controller.getTemp())
print(controller.getType())
print(controller.getLight())


