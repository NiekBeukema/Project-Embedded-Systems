from UnoNetworking import UnoNetworkController
import time

controller = UnoNetworkController();

controller.connect()
time.sleep(1)
controller.rollOut(20)
print(controller.getLength())


