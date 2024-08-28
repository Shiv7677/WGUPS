# define hash table
class HashTable:
    def __init__(self, size=40):    ## Size based on number of packages provided
        self.size = size
        self.table = []
        for i in range(size):
            self.table.append([])
        
## key for the hash table   
    def hash_function(self, package_id):
        return package_id % self.size
    
## insert function to insert packages from the csv file to the hash table
    def insert(self,package_id,package):
        index = self.hash_function(package_id)
        for item in self.table[index]:
            if item['package_id'] == package_id:
                item.update(package)
                return
        self.table[index].append(package)
        
        
    # Lookup function, search packages in hash table after packages are inserted into hash table
    def lookup(self, package_id):
        index = self.hash_function(package_id)
        for item in self.table[index]:
            if item['package_id'] == package_id:
                return item
        return None
    
    
    ## function to get all packages stored in hash table
    def get_all_packages(self):
        all_packages = []
        for bucket in self.table:
            all_packages.extend(bucket)
        return all_packages

    ## function to remove packages from hash table
    def remove_packages(self, package_id):
        index = self.hash_function(package_id)
        for item in self.table[index]:
            if item['package_id'] == package_id:
                self.table[index].remove(item)
                return 
        
## it makes HashTable object global as a value hash_table, so that we can use in different locations    
hash_table = HashTable()
    
    