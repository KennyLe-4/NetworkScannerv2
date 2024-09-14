from flask import Flask, render_template, request, redirect, url_for, flash
import nmap  # Import the nmap library for network scanning

# Initialize the Flask application
app = Flask(__name__)

# Set a secret key for the session to enable flash messages
app.secret_key = 'your_secret_key'

# Define the route for the home page
@app.route('/', methods=['GET', 'POST'])
def home():
  # Check if the request method is POST
  if request.method == 'POST':
      # Retrieve form data
      target = request.form['target']  # Target IP address or range
      scan_type = request.form['scan_type']  # Type of scan selected by the user

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
      scan_args = '-T4 -F'  # Quick scan (common ports)
  elif scan_type == 'vuln':
      scan_args = '--script vuln'  # Vulnerability scan using nmap's scripts
  elif scan_type == 'full':
      scan_args = '-p-'  # Full port scan
  elif scan_type == 'aggressive':
      scan_args = '-T4 -A'  # Aggressive scan with OS detection and version info
  else:
      scan_args = '-T4'  # Default fast scan

  # Execute the scan
  try:
      print(f"Scanning {target} with arguments: {scan_args}")  # Debugging line
      nm.scan(target, arguments=scan_args)
      print("Scan executed successfully.")  # Debugging line
  except Exception as e:
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
                  'service': nm[host][proto][port]['name']
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