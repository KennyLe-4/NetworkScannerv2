from flask import Flask, render_template, request, redirect, url_for, flash
import nmap  # Import the nmap library for network scanning
import os  # Import os for environment variable access
import re  # Import re for regular expressions
import time  # Import time for measuring scan duration

# Initialize the Flask application
app = Flask(__name__)
# Set the secret key for session management
app.secret_key = os.environ.get('FLASK_SECRET_KEY', os.urandom(24))  # Generates a random key if not set

# Function to validate IP address or domain
def is_valid_target(target):
    # Regular expression for validating an IP address
    ip_pattern = re.compile(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')
    # Regular expression for validating a domain name
    domain_pattern = re.compile(r'^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$')
    return ip_pattern.match(target) is not None or domain_pattern.match(target) is not None

# Define the route for the home page
@app.route('/', methods=['GET', 'POST'])
def home():
  # Check if the request method is POST
  if request.method == 'POST':
      # Retrieve form data
      target = request.form['target']  # Target IP address or range
      scan_type = request.form['scan_type']  # Type of scan selected by the user

      # Validate the IP address
      if not is_valid_target(target):
          flash('Invalid IP address, please check if it is correct', 'danger')  # Flash an error message
          return render_template('index.html')  # Render the home page again with the error

      # Redirect to the scan results page with the provided parameters
      return redirect(url_for('scan_results', target=target, scan_type=scan_type))

  # Render the home page template
  return render_template('index.html')

# Define the route for displaying scan results
@app.route('/scan_results', methods=['GET'])
def scan_results():
  # Retrieve query parameters from the URL
  target = request.args.get('target')
  scan_type = request.args.get('scan_type')

  # Initialize the nmap scanner
  nm = nmap.PortScanner()

  # Set scan arguments based on the selected scan type
  if scan_type == 'quick':
      scan_args = '-T4 -F'  # Quick scan (common ports and ping scan)
  elif scan_type == 'vuln':
      scan_args = '--script vuln'  # Vulnerability scan using Nmap's scripts
  elif scan_type == 'full':
      scan_args = '-p-'  # Full port scan (all ports)
  elif scan_type == 'aggressive':
      scan_args = '-A'  # Aggressive scan with OS detection and version detection
  else:
      scan_args = '-T4 -sn'  # Default fast scan (TCP SYN scan)

  # Execute the scan
  try:
      print(f"Starting scan on {target} with arguments: {scan_args}")  # Debugging line
      nm.scan(target, arguments=scan_args)
      print("Scan executed successfully.")  # Debugging line
  except Exception as e:
      print(f"An error occurred during scanning: {str(e)}")  # Debugging line
      flash(f"An error occurred: {str(e)}", 'danger')  # Display an error message
      return redirect(url_for('home'))  # Redirect back to the home page

  # Collect the scan results
  results = []
  recommendations = []

  # Iterate over all hosts found in the scan
  for host in nm.all_hosts():
      host_info = {'ip': host, 'ports': []}
      # Iterate over all protocols (e.g., TCP, UDP)
      for proto in nm[host].all_protocols():
          # Get all ports for the current protocol
          lport = nm[host][proto].keys()
          for port in lport:
              # Gather information about each port
              port_info = {
                  'port': port,
                  'state': nm[host][proto][port]['state'],
                  'service': nm[host][proto][port]['name'],
                  'version': nm[host][proto][port].get('version', 'N/A')  # Get version info, default to 'N/A'
              }
              host_info['ports'].append(port_info)

              # Provide basic security recommendations
              if nm[host][proto][port]['state'] == 'open':
                  recommendations.append(f"Port {port} ({nm[host][proto][port]['name']}) is open on {host}. Ensure proper firewall rules.")

      results.append(host_info)

  # Render the scan results page with the results and recommendations
  return render_template('scan_results.html', results=results, recommendations=recommendations)

# Run the Flask app
if __name__ == '__main__':
  app.run(debug=True)