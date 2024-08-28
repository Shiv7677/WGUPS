from datetime import datetime, timedelta

class Package:
    
    ## Initialize package object
    def __init__(self, package_id, delivery_address, delivery_city, delivery_state, delivery_zip, delivery_deadline, delivery_notes):
        self.package_id = package_id
        self.delivery_address = delivery_address
        self.delivery_city = delivery_city
        self.delivery_state = delivery_state
        self.delivery_zip = delivery_zip
        self.delivery_deadline = datetime.strptime(delivery_deadline, '%Y-%m-%d')
        self.delivery_notes = delivery_notes
        self.delivery_status = 'at the hub'
        self.delivery_time = None
        

## method provides a string representation of the Package object
    def __str__(self):
        return f"Package ID: {self.package_id}, Delivery Address: {self.delivery_address}, Delivery City: {self.delivery_city}, Delivery State: {self.delivery_state}, Delivery Zip: {self.delivery_zip}, Delivery Deadline: {self.delivery_deadline.strftime('%Y-%m-%d')}, Delivery Notes: {self.delivery_notes}, Delivery Status: {self.delivery_status}, Delivery Time: {self.delivery_time.strftime('%Y-%m-%d %H:%M:%S')}"
    

## Function to update the status of the packages 
def update_status(self, new_status, delivery_time=None):
    delivery_status = new_status
    if delivery_time:
        self.delivery_time = datetime.strptime(delivery_time, '%Y-%m-%d %H:%M:%S')
            