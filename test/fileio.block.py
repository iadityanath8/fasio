import time

CHUNK_SIZE = 4096  

def blocking_file_reader(filename):
    print("Starting file read (Blocking Mode)...")
    with open(filename, "r", encoding="utf-8") as f:
        data = f.read()  
    time.sleep(2)  
    print("File contents:\n", data)

def print_message():
    """Prints messages while waiting."""
    for i in range(5):
        print(f"Doing other work... {i}")  
        time.sleep(1)

def main():
    blocking_file_reader("large_file.txt")  
    print_message()  

main()
