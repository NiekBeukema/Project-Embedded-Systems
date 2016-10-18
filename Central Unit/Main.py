from UnoNetworking import UnoNetworkController
import time

controller = UnoNetworkController();

controller.connect()

controller.rollOut(88)
print("Temperatuur:")
print(controller.getTemp())
print("Licht:")
print(controller.getLight())


