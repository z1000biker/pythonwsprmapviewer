import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import urllib.request
import urllib.parse
import json
import math
from tkintermapview import TkinterMapView

BAND_MAP = {
    "LF (-1)": (-1, 0.136),
    "MF (0)": (0, 0.4742),
    "160m (1)": (1, 1.8366),
    "80m (3)": (3, 3.5686),
    "60m (5)": (5, 5.2872),
    "40m (7)": (7, 7.0386),
    "30m (10)": (10, 10.1387),
    "20m (14)": (14, 14.0956),
    "17m (18)": (18, 18.1046),
    "15m (21)": (21, 21.0946),
    "12m (24)": (24, 24.9246),
    "10m (28)": (28, 28.1246),
    "8m (40)": (40, 40.680),  # Corrected frequency
    "6m (50)": (50, 50.293),
    "4m (70)": (70, 70.091),
    "2m (144)": (144, 144.489),
    "70cm (432)": (432, 432.3),
    "23cm (1296)": (1296, 1296.5),
}

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def fetch_wspr_spots(band_code):
    query = f"""
    SELECT
      time,
      tx_sign,
      tx_loc,
      tx_lat,
      tx_lon,
      snr,
      frequency,
      rx_sign,
      rx_loc,
      rx_lat,
      rx_lon
    FROM wspr.rx
    WHERE
      band = {band_code}
      AND time > now() - INTERVAL 1 HOUR
    ORDER BY time DESC
    LIMIT 500
    FORMAT JSON
    """
    url = "https://db1.wspr.live/?" + urllib.parse.urlencode({"query": query})
    try:
        with urllib.request.urlopen(url, timeout=25) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data["data"]
    except Exception as e:
        return str(e)

class WSPRApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WSPR Band Spot Viewer - SV1EEX (Fixed)")
        self.geometry("900x900")

        tk.Label(self, text="Select Band:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.band_var = tk.StringVar()
        band_list = list(BAND_MAP.keys())
        self.band_combo = ttk.Combobox(self, textvariable=self.band_var, values=band_list, state='readonly', width=25)
        self.band_combo.grid(row=0, column=1, padx=5, pady=5)
        self.band_combo.current(band_list.index("10m (28)"))

        self.fetch_button = tk.Button(self, text="Fetch Spots (last 1 hour)", command=self.on_fetch)
        self.fetch_button.grid(row=0, column=2, padx=5, pady=5)

        self.output_text = scrolledtext.ScrolledText(self, width=110, height=20, wrap=tk.NONE)
        self.output_text.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        self.map_widget = TkinterMapView(self, width=880, height=550, corner_radius=0)
        self.map_widget.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
        self.map_widget.set_position(30.0, 0.0)
        self.map_widget.set_zoom(2)

    def on_fetch(self):
        band_name = self.band_var.get()
        band_info = BAND_MAP.get(band_name)
        if band_info is None:
            messagebox.showerror("Error", "Please select a valid band.")
            return
        band_code, _ = band_info

        self.fetch_button.config(state=tk.DISABLED)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, f"Fetching spots for band {band_name}...\n\n")
        self.update()

        result = fetch_wspr_spots(band_code)
        if isinstance(result, str):
            self.output_text.insert(tk.END, f"Failed to fetch data: {result}\n")
            self.fetch_button.config(state=tk.NORMAL)
            return

        self.output_text.insert(tk.END, f"Found {len(result)} WSPR spots:\n\n")

        self.map_widget.delete_all_marker()
        self.map_widget.delete_all_path()

        for spot in result:
            try:
                time = spot.get("time")
                call = spot.get("tx_sign")
                loc = spot.get("tx_loc")
                lat = float(spot.get("tx_lat"))
                lon = float(spot.get("tx_lon"))
                snr = spot.get("snr")
                freq = float(spot.get("frequency"))
                recv_call = spot.get("rx_sign")
                recv_loc = spot.get("rx_loc")
                recv_lat = float(spot.get("rx_lat"))
                recv_lon = float(spot.get("rx_lon"))
                distance = haversine(lat, lon, recv_lat, recv_lon)
                freq_mhz = freq / 1e6

                line_text = (f"[{time}] Tx: {call} ({loc}) → Rx: {recv_call} ({recv_loc}) "
                             f"Dist: {distance:.1f} km SNR: {snr}dB\n")
                self.output_text.insert(tk.END, line_text)

                # --- MAPPING LOGIC FIX ---
                color = "blue"  # Default color for HF
                draw_path = True

                if freq_mhz > 50:
                    if 300 <= distance <= 1500:
                        color = "red"  # Possible Sporadic E
                    elif distance > 350:
                        color = "green"  # Possible Tropo or DX
                    else:
                        draw_path = False # Skip local VHF noise

                if draw_path:
                    self.map_widget.set_marker(lat, lon, text=f"Tx: {call}")
                    self.map_widget.set_marker(recv_lat, recv_lon, text=f"Rx: {recv_call}")
                    self.map_widget.set_path([(lat, lon), (recv_lat, recv_lon)], color=color, width=2)

            except (ValueError, TypeError):
                continue

        self.fetch_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    app = WSPRApp()
    app.mainloop()
