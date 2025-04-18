import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import openrouteservice

# OpenRouteService API Key
API_KEY = "5b3ce3597851110001cf62481627160751fe47c7950d9114f79c2d95"
client = openrouteservice.Client(key=API_KEY)

# App setup
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title("Smart Route Finder")
root.geometry("600x500")
root.resizable(False, False)

# Header
header = ctk.CTkLabel(root, text="🚀 Smart Route Finder", font=("Arial Black", 24))
header.pack(pady=20)

# Input frame
input_frame = ctk.CTkFrame(root, corner_radius=15)
input_frame.pack(padx=20, pady=10, fill="x")

ctk.CTkLabel(input_frame, text="From:", font=("Arial", 16)).grid(row=0, column=0, padx=10, pady=15, sticky="e")
from_entry = ctk.CTkEntry(input_frame, width=250, height=35, font=("Arial", 14))
from_entry.grid(row=0, column=1, padx=10, pady=15)

ctk.CTkLabel(input_frame, text="To:", font=("Arial", 16)).grid(row=1, column=0, padx=10, pady=15, sticky="e")
to_entry = ctk.CTkEntry(input_frame, width=250, height=35, font=("Arial", 14))
to_entry.grid(row=1, column=1, padx=10, pady=15)

# Geocoding
def get_coordinates(city_name):
    try:
        geocode = client.pelias_search(text=f"{city_name}, India")
        features = geocode.get('features')
        if features:
            coords = features[0]['geometry']['coordinates']
            return coords
        else:
            return None
    except Exception as e:
        print("Geocode error:", e)
        return None

# Result vars
route_var = tk.StringVar()
distance_var = tk.StringVar()
duration_var = tk.StringVar()

# Main Logic
def find_route():
    start_city = from_entry.get().strip()
    end_city = to_entry.get().strip()

    coords_start = get_coordinates(start_city)
    coords_end = get_coordinates(end_city)

    if not coords_start or not coords_end:
        messagebox.showerror("Error", f"Could not find coordinates for:\n• {start_city}\n• {end_city}")
        return

    try:
        route = client.directions(
            coordinates=[coords_start, coords_end],
            profile='driving-car',
            format='geojson'
        )

        props = route['features'][0]['properties']
        segment = props['segments'][0]
        distance_km = segment['distance'] / 1000
        duration_min = segment['duration'] / 60

        route_var.set(f"{start_city.title()} → {end_city.title()}")
        distance_var.set(f"{distance_km:.2f} km")
        duration_var.set(f"{duration_min:.1f} minutes")

    except Exception as e:
        messagebox.showerror("Routing Error", str(e))

def reset_fields():
    from_entry.delete(0, tk.END)
    to_entry.delete(0, tk.END)
    route_var.set("")
    distance_var.set("")
    duration_var.set("")
    from_entry.focus()

# Buttons
button_frame = ctk.CTkFrame(root, fg_color="transparent")
button_frame.pack(pady=10)

ctk.CTkButton(button_frame, text="Find Route", width=120, height=40, font=("Arial", 14), command=find_route).grid(row=0, column=0, padx=15)
ctk.CTkButton(button_frame, text="Reset", width=120, height=40, font=("Arial", 14), command=reset_fields, fg_color="red", hover_color="#cc0000").grid(row=0, column=1, padx=15)

# Result display
result_frame = ctk.CTkFrame(root, corner_radius=15)
result_frame.pack(padx=20, pady=20, fill="x")

ctk.CTkLabel(result_frame, text="Route:", font=("Arial", 16, "bold")).pack(pady=(15, 5))
ctk.CTkLabel(result_frame, textvariable=route_var, font=("Arial", 14)).pack()

ctk.CTkLabel(result_frame, text="Distance:", font=("Arial", 16, "bold")).pack(pady=(15, 5))
ctk.CTkLabel(result_frame, textvariable=distance_var, font=("Arial", 14)).pack()

ctk.CTkLabel(result_frame, text="Time:", font=("Arial", 16, "bold")).pack(pady=(15, 5))
ctk.CTkLabel(result_frame, textvariable=duration_var, font=("Arial", 14)).pack()

# Start app
from_entry.focus()
root.mainloop()
