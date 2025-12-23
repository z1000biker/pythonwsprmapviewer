# WSPR Band Spot Viewer with Map 🌍🛰️

A powerful Python application using `Tkinter` and `TkinterMapView` for visualizing recent **WSPR (Weak Signal Propagation Reporter)** spots on an interactive map. This tool is designed for amateur radio enthusiasts to monitor real-time propagation conditions across all bands.

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 🌟 Features

- **Global Coverage**: Real-time data fetching from the [wspr.live](https://wspr.live) database with global scope.
- **Multi-Band Support**: Supports all amateur radio bands from LF (Low Frequency) to Microwave.
- **Advanced Mode Analysis**:
    - 🔵 **Blue Paths**: Standard HF propagation (F2 Layer).
    - 🔴 **Red Paths**: Potential **Sporadic E (Es)** detection for VHF/UHF (300km - 1500km).
    - 🟢 **Green Paths**: Possible **Tropospheric Ducting** or DX paths for VHF/UHF (> 350km).
- **Interactive Map**: View transmitter (Tx) and receiver (Rx) locations with clickable markers and detailed distance calculations.
- **Detailed Logs**: Real-time text output with timestamps, callsigns, SNR, and frequencies.

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher.
- `pip` package manager.

### Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/z1000biker/pythonwsprmapviewer.git
   cd pythonwsprmapviewer
   ```

2. **Install dependencies**:
   ```bash
   pip install tkintermapview
   ```

3. **Run the application**:
   ```bash
   python wsprbandmapviewer.py
   ```

## 🛠️ Configuration (pyproject.toml)
The project includes a `pyproject.toml` file for modern Python packaging and dependency management.

## 📖 How it works
The app queries the ClickHouse-based WSPR database to retrieve spots from the last hour. Using the **Haversine formula**, it calculates the Great Circle distance between stations. For frequencies above 50 MHz, it applies heuristic filters to identify likely propagation modes like Sporadic E or Tropospheric ducting.

## 📄 License
This project is licensed under the **MIT License**.

## 🤝 Acknowledgments
- Map interface powered by [TkinterMapView](https://github.com/TomSchimansky/TkinterMapView).
- Data provided by the incredible [WSPR Live](https://wspr.live) project.

---
**Created by SV1EEX**  
📧 [sv1eex@hotmail.com](mailto:sv1eex@hotmail.com)
