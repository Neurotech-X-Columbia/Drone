from djitellopy import Tello
tello = Tello()
def takeoff_land():
    tello.connect()
    tello.takeoff()
    tello.land()
