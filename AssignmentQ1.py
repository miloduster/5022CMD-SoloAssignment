"""
Hash Table (Open Addressing + Linear Probing) vs One-Dimensional Array search.
"""

import random
import time


# PART 2 - ENTITY CLASS: one pharmacy product
class Product:

    # __init__ runs automatically when you write Product(...).
    # "self" means "this particular product object".
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id    # int   : unique ID, used as the hash key
        self.name = name                # str   : e.g. "Paracetamol 500mg"
        self.price = price              # float : price in RM
        self.stock = stock              # int   : units on the shelf

    # __str__ decides what print(product) shows.
    def __str__(self):
        return ("ID: " + str(self.product_id) +
                " | Name: " + self.name +
                " | Price: RM" + format(self.price, ".2f") +
                " | Stock: " + str(self.stock))


# ======================================================================
# PART 1 - HASH TABLE
# ======================================================================

# Table size used by the inventory system. 101 is prime, which spreads
# keys more evenly when using the % (modulo) hash function.
TABLE_SIZE = 101

# The three possible states of a slot. Named constants are easier to read
# than the bare numbers 0, 1, 2.
EMPTY = 0       # never used: a search can stop here
OCCUPIED = 1    # holds a product
DELETED = 2     # "tombstone": used before; a search must keep going past it


class Slot:
    """One bucket of the hash table."""

    def __init__(self):
        self.state = EMPTY
        self.product = None     # None means "nothing stored"


class HashTable:
    """Hash table using open addressing with linear probing."""

    def __init__(self, size):
        self.size = size
        self.slots = []                 # make a list of empty slots
        for i in range(self.size):
            self.slots.append(Slot())
        self.count = 0                  # how many OCCUPIED slots

    # ---- hash function -------------------------------------------------
    def hash_function(self, key):
        """Division method: the remainder of key / size."""
        return key % self.size

    # ---- insert --------------------------------------------------------
    def insert(self, product):
        """Insert a product. Returns the slot index used.
        Raises ValueError if the product ID already exists."""

        start = self.hash_function(product.product_id)
        first_deleted = -1      # -1 means "no tombstone seen yet"

        # Linear probing: try start, start+1, start+2, ... wrapping around.
        for i in range(self.size):
            index = (start + i) % self.size     # % wraps back to 0 at the end
            slot = self.slots[index]

            if slot.state == OCCUPIED:
                # Same ID already stored? Then it is a duplicate.
                if slot.product.product_id == product.product_id:
                    raise ValueError("Product ID " + str(product.product_id) +
                                     " already exists.")

            elif slot.state == DELETED:
                # Remember the first tombstone but keep looking, because the
                # same ID might still be further along the chain.
                if first_deleted == -1:
                    first_deleted = index

            else:
                # EMPTY: the ID is definitely not in the table.
                if first_deleted != -1:
                    return self.place(first_deleted, product)
                return self.place(index, product)

        # Went all the way round without meeting an EMPTY slot.
        if first_deleted != -1:
            return self.place(first_deleted, product)
        raise RuntimeError("Hash table is full. Cannot insert.")

    def place(self, index, product):
        """Put the product into the slot at index and update counters."""
        slot = self.slots[index]
        slot.state = OCCUPIED
        slot.product = product
        self.count = self.count + 1
        return index

    # ---- search --------------------------------------------------------
    def search(self, key):
        """Return the Product with this ID, or None if it is not found."""
        start = self.hash_function(key)

        for i in range(self.size):
            index = (start + i) % self.size
            slot = self.slots[index]

            if slot.state == EMPTY:
                return None             # chain ended, so it is not in the table
            if slot.state == OCCUPIED and slot.product.product_id == key:
                return slot.product
            # DELETED or a different product: keep probing

        return None

    # ---- delete --------------------------------------------------------
    def delete(self, key):
        """Delete by ID using a tombstone. Returns True if removed."""
        start = self.hash_function(key)

        for i in range(self.size):
            index = (start + i) % self.size
            slot = self.slots[index]

            if slot.state == EMPTY:
                return False
            if slot.state == OCCUPIED and slot.product.product_id == key:
                slot.state = DELETED    # tombstone, NOT empty
                slot.product = None
                self.count = self.count - 1
                return True
        return False

    # ---- display -------------------------------------------------------
    def display(self):
        print("Table size: " + str(self.size) +
              " | Records: " + str(self.count))
        for index in range(self.size):
            slot = self.slots[index]
            if slot.state == OCCUPIED:
                print("  [" + str(index) + "] " + str(slot.product))


# ======================================================================
# PART 4 - ARRAY SEARCH AND BENCHMARK
# ======================================================================
def array_search(array, key):
    """Linear search: check every item from the start until found."""
    for product in array:
        if product.product_id == key:
            return product
    return None


def time_hash_search(table, keys):
    """Average seconds per search in the hash table over the list of keys."""
    start_time = time.perf_counter()        # high-resolution timer
    for key in keys:
        table.search(key)
    end_time = time.perf_counter()
    return (end_time - start_time) / len(keys)


def time_array_search(array, keys):
    """Average seconds per search in the array over the list of keys."""
    start_time = time.perf_counter()
    for key in keys:
        array_search(array, key)
    end_time = time.perf_counter()
    return (end_time - start_time) / len(keys)


def benchmark():
    """Compare hash table vs array for growing numbers of records."""
    sizes = [100, 1000, 10000]
    searches = 200                          # repeat searches to average out noise
    random.seed(42)                         # same random numbers every run

    print("")
    print("       n |     Hash (s) |    Array (s) | Array/Hash")
    print("-" * 52)

    for n in sizes:
        # Make n unique IDs: 1000, 1001, ... then shuffle their order.
        ids = []
        for i in range(n):
            ids.append(1000 + i)
        random.shuffle(ids)

        # Build the SAME data in both structures.
        table = HashTable(n * 2)            # starts about 50% full
        array = []
        for pid in ids:
            product = Product(pid, "Medicine " + str(pid),
                              round(random.uniform(1, 100), 2),
                              random.randint(1, 500))
            table.insert(product)
            array.append(product)

        # Pick random IDs that exist in the data to search for.
        search_keys = []
        for i in range(searches):
            search_keys.append(ids[random.randint(0, n - 1)])

        # Time both structures with the same keys.
        t_hash = time_hash_search(table, search_keys)
        t_array = time_array_search(array, search_keys)
        print(str(n).rjust(8) + " | " + format(t_hash, ".8f").rjust(12) + " | " +
              format(t_array, ".8f").rjust(12) + " | " +
              format(t_array / t_hash, ".1f").rjust(8) + "x")


# ======================================================================
# PART 3 - COMMAND-LINE INVENTORY SYSTEM
# ======================================================================
def read_int(prompt):
    """Keep asking until the user types a whole number."""
    while True:
        text = input(prompt)
        try:
            return int(text)            # if text is not a number this fails
        except ValueError:              # ...and we catch the error here
            print("  Please enter a whole number.")


def read_float(prompt):
    """Keep asking until the user types a non-negative number."""
    while True:
        text = input(prompt)
        try:
            value = float(text)
            if value >= 0:
                return value
            print("  Price cannot be negative.")
        except ValueError:
            print("  Please enter a number.")


def load_sample_data(table, array):
    """Insert pre-defined records. IDs 1042 and 1143 collide on purpose."""
    add_product(table, array, Product(1042, "Paracetamol 500mg", 5.90, 120))
    add_product(table, array, Product(1143, "Ibuprofen 200mg", 8.50, 80))
    add_product(table, array, Product(2001, "Amoxicillin 250mg", 12.30, 45))
    add_product(table, array, Product(2002, "Cetirizine 10mg", 7.20, 60))
    add_product(table, array, Product(3005, "Vitamin C 1000mg", 15.00, 200))
    add_product(table, array, Product(3006, "Cough Syrup 100ml", 9.80, 35))
    add_product(table, array, Product(4010, "Omeprazole 20mg", 11.40, 50))
    add_product(table, array, Product(4011, "Loratadine 10mg", 6.90, 70))


def add_product(table, array, product):
    """Store one product in BOTH the hash table and the array."""
    index = table.insert(product)       # may raise ValueError on duplicates
    array.append(product)
    return index


def remove_from_array(array, key):
    """Return a new list containing every product except the one with key."""
    new_array = []
    for product in array:
        if product.product_id != key:
            new_array.append(product)
    return new_array


def menu():
    table = HashTable(TABLE_SIZE)
    array = []
    load_sample_data(table, array)

    running = True
    while running:
        print("")
        print("==== Pharmacy Inventory System ====")
        print("1. Insert Product")
        print("2. Search Product")
        print("3. Edit Product")
        print("4. Delete Product")
        print("5. Display Table")
        print("6. Run Benchmark")
        print("7. Exit")
        choice = read_int("Enter choice: ")

        if choice == 1:
            pid = read_int("Enter Product ID (Numbers Only): ")
            name = input("Enter Product Name: ")
            price = read_float("Enter Price (RM): ")
            stock = read_int("Enter Stock Quantity: ")
            product = Product(pid, name, price, stock)
            try:
                index = add_product(table, array, product)
                print("Product inserted successfully into slot [" + str(index) + "]")
            except (ValueError, RuntimeError) as error:
                print(error)

        elif choice == 2:
            pid = read_int("Enter Product ID to search: ")
            found = table.search(pid)
            if found is not None:
                print("Product Found!")
                print(found)
            else:
                print("Product not found.")

            # One search is too fast to time, so repeat it 1000 times and average.
            keys = []
            for i in range(1000):
                keys.append(pid)
            print("Search completed in " +
                  format(time_hash_search(table, keys), ".8f") + " seconds (Hash Table)")
            print("Search completed in " +
                  format(time_array_search(array, keys), ".8f") + " seconds (Array)")

        elif choice == 3:
            pid = read_int("Enter Product ID to edit: ")
            product = table.search(pid)
            # The array holds the SAME object, so editing it updates both.
            if product is None:
                print("Product not found.")
            else:
                new_name = input("New name (blank = keep '" + product.name + "'): ")
                if new_name != "":
                    product.name = new_name
                product.price = read_float("New price: ")
                product.stock = read_int("New stock: ")
                print("Product updated.")

        elif choice == 4:
            pid = read_int("Enter Product ID to delete: ")
            if table.delete(pid):
                array = remove_from_array(array, pid)
                print("Product deleted.")
            else:
                print("Product not found.")

        elif choice == 5:
            table.display()

        elif choice == 6:
            benchmark()

        elif choice == 7:
            print("Exiting Inventory System. Goodbye!")
            running = False

        else:
            print("Invalid choice.")

menu()