import socket
import concurrent.futures
import logging
import csv


# Configure logging for debug and error messages
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


# Define the custom DNS server IP addresses for different networks
custom_dns_servers = {
"": "",
"": "",
"": "",
"": "",
"": "",
"": "",
"": "",
"": "",
"": "",
"": "",
"": "",
}

 

 
# Set a default timeout for DNS queries (in seconds)
socket.setdefaulttimeout(5)  # Adjust timeout as needed

# Function to perform DNS lookup for a given IP address
def get_dns_name(ip_address):
    try:
        logging.debug(f"Performing DNS lookup for {ip_address}")
        # Use custom DNS server if IP address falls within specific ranges
        if any(ip_address.startswith(network) for network in custom_dns_servers):
            dns_server = custom_dns_servers[ip_address.split('.')[2] + '.0']
            resolver = socket.gethostbyname_ex(ip_address, dns_server)
        else:
            resolver = socket.gethostbyaddr(ip_address)
            
        return ip_address, resolver[0]  # Return both IP address and DNS name
    except Exception as e:
        logging.error(f"Error occurred for {ip_address}: {e}")
        return ip_address, None  # Return IP address and indicate DNS name is None

# Function to find IP addresses and their corresponding DNS names concurrently
def find_matching_dns_names():
    matching_dns = []  # Initialize list to store matching IP-DNS pairs
    no_dns_names_found = []  # Initialize list to store IP addresses without DNS names
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=256) as executor:
        # Function to perform DNS lookup in parallel for each IP address
        def lookup(ip_address):
            ip, dns_name = get_dns_name(ip_address)
            if dns_name:
                nonlocal matching_dns
                matching_dns.append((ip, dns_name))
                logging.info(f"Found DNS name '{dns_name}' for IP Address: {ip}")
            else:
                nonlocal no_dns_names_found
                no_dns_names_found.append(ip)
                logging.info(f"No DNS name found for IP Address: {ip}")
        
        # Submit DNS lookup tasks for all IP addresses in the specified networks
        futures = []
        for network in custom_dns_servers.keys():
            for j in range(256):  # Fourth octet range (0 to 255)
                ip_address = f"{network.split('.')[0]}.{network.split('.')[1]}.{network.split('.')[2]}.{j}"
                futures.append(executor.submit(lookup, ip_address))
        
        concurrent.futures.wait(futures)  # Wait for all tasks to complete
    
    return matching_dns, no_dns_names_found  # Return list of IP-DNS pairs and IP addresses without DNS names

# Entry point of the script
if __name__ == "__main__":
    try:
        matching_dns_names, no_dns_names_found = find_matching_dns_names()  # Perform DNS lookups
        
        # Write results to a CSV file
        with open('dns_results.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['IP Address', 'DNS Name'])
            for ip, dns in matching_dns_names:
                csv_writer.writerow([ip, dns])
                print(f"IP Address: {ip}, DNS Name: {dns}")  # Print results to console
            
            # Write IP addresses without DNS names to a separate column
            csv_writer.writerow([])
            csv_writer.writerow(['IP Address without DNS Name'])
            for ip in no_dns_names_found:
                csv_writer.writerow([ip])
                print(f"IP Address without DNS Name: {ip}")  # Print results to console
    
        print("DNS lookup results saved to dns_results.csv")
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")  # Log any unexpected errors

