function showScanDescription(scanType) {
    console.log("Function called with scanType:", scanType); // Debugging line
    var description = '';

    switch (scanType) {
        case 'quick':
            description = 'Quick Scan: This scan checks the most common ports (e.g., 80, 443, 22) quickly to provide a fast overview of the network.';
            break;
        case 'vuln':
            description = 'Vulnerability Scan: This scan checks for known vulnerabilities like Heartbleed or open backdoors.';
            break;
        case 'full':
            description = 'Full Port Scan: Scans all 65,535 TCP ports to understand the full scope of available ports on a machine.';
            break;
        case 'service':
            description = 'Service Detection: Provides information about services running on open ports (useful for determining if a machine is running a web server, FTP, etc.).';
            break;
        case 'os':
            description = 'OS Detection: Tries to identify the operating system running on the target, useful for understanding what devices are on your network.';
            break;
        case 'aggressive':
            description = 'Aggressive Scan: Combines various techniques for a comprehensive scan, including OS detection, version detection, script scanning, and traceroute.';
            break;
        default:
            description = 'Please select a scan type to see its description.';
    }

    document.getElementById('description').value = description;
}