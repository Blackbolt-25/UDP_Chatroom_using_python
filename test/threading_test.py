import threading
import time

# Function to print numbers from 1 to 5
def print_numbers():
    for i in range(1, 6):
        print(i)
        time.sleep(1)  # Sleep for 1 second between each number

# Create two threads
thread1 = threading.Thread(target=print_numbers)
thread2 = threading.Thread(target=print_numbers)

# Start the threads
thread1.start()
thread2.start()

# Wait for the threads to finish
thread1.join()
thread2.join()

print("Both threads have finished.")
