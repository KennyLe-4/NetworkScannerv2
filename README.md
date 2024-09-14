A simple web-based network scanner application built with Flask and Nmap. This application allows users to scan a target IP address or range for open ports and services, providing insights into the network's security posture.

## Features

- **Scan Types**: Choose from various scan types, including:
  - Quick Scan
  - Vulnerability Scan
  - Full Port Scan
  - Service Detection
  - OS Detection
- **User-Friendly Interface**: Easy-to-use web interface with tooltips for each scan type.
- **Scan Results**: View detailed scan results, including open ports and services.
- **Export Results**: Option to export scan results in different formats (coming soon).
- **Scan History**: Keep track of previous scans (coming soon).

## Requirements

- Python 3.x
- Flask
- Nmap (installed on your system)
- jinja2 (for rendering HTML templates)

## Installation
1. **Clone the Repository**, cd networkScannerv2
2. **Create a Virtual Environment** (optional but recommended):
bash python -m venv venv
source venv/bin/activate  # On Windows use venv\\Scripts\\activate

**Install Dependencies**:
bash
pip install -r requirements.txtæ

## Usage
**Run the Application**:
bash python app.py

**Access the Application**:
   - Open your web browser and go to `http://127.0.0.1:5000`.
