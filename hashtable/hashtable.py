from linkedlist import LinkedList
import sys
sys.path.append('../hashtable/linked_list')


class HashTableEntry:
    """
    Linked List hash table key/value pair
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8
MAX_LOAD_FACTOR = 0.7
MIN_LOAD_FACTOR = 0.2


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys
    Implement this.
    """

    def __init__(self, capacity):
        # Your code here
        if capacity >= MIN_CAPACITY:
            self.capacity = max(capacity, MIN_CAPACITY)
            self.storage = [LinkedList()] * self.capacity
            self.load = 0

    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)
        One of the tests relies on this.
        Implement this.
        """
        # Your code here
        return self.capacity

    def get_load_factor(self):
        """
        Return the load factor for this hash table.
        Implement this.
        """
        # Your code here
        return self.load / self.capacity

    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit
        Implement this, and/or DJB2.
        """

        """
        Returns: The FNV-1a (alternate) hash of a given string
        """

        FNV_offset_basis = 14695981039346656037
        FNV_prime = 1099511628211

        hashed = FNV_offset_basis

        bytes_to_hash = key.encode()

        for byte in bytes_to_hash:
            hashed = hashed * FNV_prime
            hashed = hashed ^ byte  # XOR	Sets each bit to 1 if only one of two bits is 1
            return hashed

    def djb2(self, key):
        """
        DJB2 hash, 32-bit
        Implement this, and/or FNV-1.
        """
        # Your code here
        hash = 5381
        for character in key:
            hash = ((hash << 5)+hash)+ord(character)
        return hash & 0xFFFFFFFF

    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        # returns an index value for a key
        # return self.fnv1(key) % len(self.storage)
        return self.djb2(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.
        Hash collisions should be handled with Linked List Chaining.
        Implement this.
        """
        # Your code here
        # stores value in a particular slot
        slot = self.hash_index(key)
        current = self.storage[slot].head

        while current:
            # search for the slot with the specifiv key
            if current.key == key:
                # if found update the value
                current.value = value
            # move to the next slot
            current = current.next
        # if there is no slot with the specifik key we create a hashtabel entry
        entry = HashTableEntry(key, value)
        # we insert the entry at the head of our linked list
        self.storage[slot].insert_at_head(entry)
        self.load += 1

    def delete(self, key):
        """
        Remove the value stored with the given key.
        Print a warning if the key is not found.
        Implement this.
        """
        # Your code here
        # we use the put method and instead of adding the value we add None
        self.put(key, None)
        self.load -= 1

    def get(self, key):
        """
        Retrieve the value stored with the given key.
        Returns None if the key is not found.
        Implement this.
        """
        # Your code here
        # get the slot
        slot = self.hash_index(key)
        # use the slot as index to find the linked list head
        current = self.storage[slot].head

        while current:  # while the LL head is not none
            # if the LL head's key is equal withhthe key that we are searching
            if current.key == key:
                # we return the value
                return current.value
            # move to the next slot until we find it
            current = current.next
        # we return non if there is no node in the LL with that key we are searching for
        return None

    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.
        Implement this.
        """
        # Your code here

        old_storage = self.storage
        # make a newlist with the new capacity
        self.storage = [LinkedList()] * new_capacity

        # if the present load factor is equal or bigger that 0.7
        if self.get_load_factor() >= MAX_LOAD_FACTOR:
            # iterate over the old list
            for item in old_storage:
                current = item.head
                while current:
                    # move all the old kv to the new list
                    self.put(current.key, current.value)
                    current = current.next
            # set the capacity to the new capacity
            self.capacity = new_capacity


if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")
