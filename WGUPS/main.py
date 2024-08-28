# Main.py
# Shiv Patel
# Student ID: 011415280

from hash_table import hash_table
from package import Package, update_status
from truck import Truck
import csv
from datetime import datetime, timedelta


    
#definig file names
package_filename = 'Package.csv'
distance_filename = 'Distance.csv'
address_filename = 'Address.csv'

# Function to load package data from a Csv file
def load_package_data():
    packages = []
    with open(package_filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            
            # headers = reader.fieldnames
            # print("Headers in CSV:", headers)
            
            # for row in reader:
             #   print(row)    ## to check if the function can read csv file properly...
            
            package_id = int(row['ID'])
            delivery_address = row['Address']
            delivery_city = row['City']
            delivery_state = row['State']
            delivery_zip = row['Zip']
            delivery_deadline = row['Deadline']
            delivery_weight = row['Weight']
            delivery_notes = row['Notes']
            
            package = {
                'package_id': package_id,
                'delivery_address': delivery_address,
                'delivery_city': delivery_city,
                'delivery_state': delivery_state,
                'delivery_zip': delivery_zip,
                'delivery_deadline': delivery_deadline,
                'package_weight': delivery_weight,
                'delivery_notes': delivery_notes,
                'delivery_status': 'at the hub',
                'delivery_time': None,
                'departure_time': None
            }
            
            packages.append(package)
            hash_table.insert(package_id, package)
            
    return packages            
            

packages = load_package_data()
## print(packages)

# Function to load address information from the csv file...
def load_address():
    addresses = []
    with open(address_filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >=3:
                id = row[0]
                name = row[1]
                address = row[2]
                addresses.append({'ID': id, 'name': name, 'address': address})
    return addresses
addresses = load_address()
## print(addresses)

## Function to get address id...
def address_id(address):
    for row in addresses:
        if address.strip().lower() == row['address'].strip().lower():
            return int(row['id']) 
    return None 


"""test = "4001 South 700 East"
get_id = address_id(test)
print(f"The ID for the address '{test}' is: {get_id}")  ### """


# function to load distance from csv file...      
def load_distance(addresses):
    distances = []
    with open(distance_filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for index, row in enumerate(reader):
            completed_row = [float(dist.strip()) if dist.strip() else 0.0 for dist in row]
            distances.append(completed_row)
    for i in range(len(distances)):
        for j in range(i + 1, len(distances)):
            distances[i][j] = distances[j][i] 
    return distances

distances = load_distance(addresses)

## print(distances)

# Function to claclulate distance between two addresses, this function takes address itself as a input.
def calculate_distance(address1, address2, addresses,):
    address1 = address1.strip().lower()
    address2 = address2.strip().lower()

    index1 = next((index for (index, d) in enumerate(addresses) if d['address'].strip().lower() == address1), None)
    index2 = next((index for (index, d) in enumerate(addresses) if d['address'].strip().lower() == address2), None)

    if index1 is not None and index2 is not None:
        return distances[index1][index2]
    else:
        return None
    
## distances = (calculate_distance( '1330 2100 S',  '1488 4800 S', addresses ))
## print(distances)  ## to debug and check

## Truck Objects..Manually loading the trucks with packages
truck1 = Truck([1,14,16,15,29,30,31,34,37,40,19,20,13,4,8,10], datetime.strptime('08:00 AM', '%I:%M %p') )
truck2 = Truck([3,18,36,38,2,11,39,25,6], datetime.strptime('9:10 AM', '%I:%M %p'))
truck3 = Truck([9,32,28,5,7,12,17,21,22,23,24,26,27,33,35], datetime.strptime('10:30 AM', '%I:%M %p'))
trucks = [truck1, truck2, truck3]

## All special case and time delays are being taken care of... and packages are loaded accordingly

address_update_time = datetime.strptime('10:20 AM', '%I:%M %p')

## Function to find nearest next package
def nearest_neighbor(truck):
    not_delivered = [hash_table.lookup(package_id) for package_id in truck.packages]
    
    truck.packages.clear()
    
    while not_delivered:
        nearest_package, nearest_distance = None, float('inf')
        
        for package in not_delivered:
                            
            distance = calculate_distance(truck.address, package['delivery_address'], addresses) # as calculate function takes address as input
            
            if distance <= nearest_distance:
                nearest_distance = distance
                nearest_package = package
                
        truck.packages.append(nearest_package['package_id'])
        not_delivered.remove(nearest_package)
        truck.total_mileage += nearest_distance
        truck.address = nearest_package['delivery_address']
        truck.time += timedelta(hours=nearest_distance / truck.speed)
        
        nearest_package['delivery_time'] = truck.time
        nearest_package['departure_time'] = truck.departure_time
        
nearest_neighbor(truck1)
nearest_neighbor(truck2)

# truck 3 departs after first 2 truck finish

truck3.departure_time = max(truck1.time, truck2.time)
nearest_neighbor(truck3)


#Function to output information of a particular package based on user input as package ID...
def packages_info(package_id):
    package = hash_table.lookup(package_id)
    if package:
        print(f"\n--- Package Information for Package ID {package_id}---")
        print(f"Address: {package['delivery_address']}")
        print(f"City: {package['delivery_city']}")
        print(f"State: {package['delivery_state']}")
        print(f"Zip: {package['delivery_zip']}")
        print(f"Delivery Deadline: {package['delivery_deadline']}")
        print(f"Package Weight: {package['package_weight']} kg")
        print(f"Status: {package['delivery_status']}")
        if package['delivery_time']:
            print(f"Delivery Time: {package['delivery_time'].strftime('%I:%M %p')}")
        print("\n")
    else:
        print(f"Package with ID {package_id} not found.")


## Function to output status of all packages at a particular time(user input)  
def status_particular_time(user_input_time):
    print(f"\n---All Packages information at {user_input_time}---")
    user_input_time_dt = datetime.strptime(user_input_time, '%I:%M %p') # convert input to datetime object
    all_packages = hash_table.get_all_packages()
    for package in all_packages: 
        if package:
            if package['package_id'] == 9 and user_input_time_dt >= address_update_time:
                package['delivery_address'] = "410 S State St"
                
            print(f"{package['package_id']}, {package['delivery_address']}, {package['delivery_city']}, {package['delivery_state']}, {package['delivery_zip']}, {package['delivery_deadline']}, {package['package_weight']}, {package['delivery_notes']}", end=" ")
            
            ### Helps to get particular trucks in which packages are there
            
            truck = next((truck for truck in trucks if package['package_id'] in truck.packages), None)
            
            if truck and user_input_time_dt < truck.departure_time:
                print(f"Status at {user_input_time}: At the Hub")
                
            elif package['delivery_time']:
                delivery_time_dt = package['delivery_time']
                
                if user_input_time_dt > delivery_time_dt:
                    print(f" Status at {user_input_time}: delivered at {package['delivery_time'].strftime('%I:%M %p')}")
                else:
                    print(f" Statuse at {user_input_time}: en route")
            else: 
                print(f" Status at {user_input_time}: at the hub")
 
 
 ## Function to get summary of all trucks at the end of the day, total miles and packages delivered by that truck               
def truck_info(trucks):
    print("\n--- Truck Information Summary ---")
    for i, truck in enumerate(trucks, start=1):             ## gets truck indes startinf from 1
        return_time_str = truck.time.strftime('%I:%M %p')
        total_mileage = truck.total_mileage
        packages = truck.packages
        
        print(f"Truck {i} -> Return Time: {return_time_str}, Total Mileage: {total_mileage}, Packages: {packages}")

    print("\n--- End of Summary ---")
    
    
### Shows total miles traveled by all 3 trucks
def total_mileage_by_all(trucks):
    total_mileage = sum(truck.total_mileage for truck in trucks)
    print(f"\nTotal Mileage of all trucks: {total_mileage}")

def main():

        
    while True:
        print("\n---Menu---")
        print("1. Check Package Details")
        print("2. Check Package Details at a specific time")
        print("3. All Trucks Information")
        print("4. Total mileage of all trucks")
        print("5. Exit")
        
        option = input("Enter your choice from above menue: ")
        
        if option == "1":
            package_id = int(input("Enter the package ID: "))
            
            packages_info(package_id)
        
        elif option == "2":
            input_time = input("Enter the time to check the delivery status for all packages (e.g., '10:30 AM'): ")
            status = status_particular_time(input_time)
            print(status)
        
        elif option == "3":
            truck_info(trucks)
            
        elif option == "4":
            total_mileage_by_all(trucks)
            
        elif option == "5":
            print("Goodbye!")
            break
        

if __name__ == "__main__":
    main()                           # """        
                      