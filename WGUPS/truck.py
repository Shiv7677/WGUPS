from hash_table import hash_table
from datetime import datetime, timedelta

class Truck:
    
    ## Initialization of Truck object
    def __init__(self, packages, departure_time, capacity = 16, speed = 18, total_mileage = 0.0, address = "4001 South 700 East"):
        self.packages = packages
        self.departure_time = departure_time
        self.capacity = capacity
        self.speed = speed
        self.total_mileage = total_mileage
        self.address = address
        self.time = departure_time


## method provides a string representation of the Truck object  
    def __str__(self):
        return f"Truck: {self.address}, Departure Time: {self.departure_time}, Capacity: {self.capacity}, Speed: {self.speed}, Total Mileage: {self.total_mileage}"