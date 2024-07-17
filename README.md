
DNS Lookup Tool



This Python script performs DNS lookups for a range of IP addresses, leveraging custom DNS servers where specified. It utilizes multithreading for concurrent DNS queries, logging results and errors to aid troubleshooting. Results are saved to a CSV file for easy analysis.

Features:


1: Custom DNS Server Support: Configure specific DNS servers for different IP ranges.
2: Concurrent Execution: Uses multithreading to speed up DNS queries.
3: Error Handling: Logs errors for each IP address if DNS lookup fails.
4: CSV Output: Results are saved to dns_results.csv, categorizing IP addresses with and without DNS names.


Usage:


1:Configure custom_dns_servers dictionary with appropriate IP ranges and DNS servers.
2:Run the script to perform DNS lookups concurrently.
3: View results in dns_results.csv for matched IP-DNS pairs and IPs without DNS names
