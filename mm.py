import json
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, messagebox

# Mapping of event codes to colors.
event_colors = {
    'mm': 'blue',  # mousemove
    'md': 'red',  # mousedown
    'cl': 'green',  # click
    'mu': 'orange',  # mouseup
    'ts': 'purple',  # touchstart
    'tm': 'brown',  # touchmove
    'te': 'pink',  # touchend
    'tc': 'gray',  # touchcancel
    'me': 'olive'  # mouseenter
}


def load_json():
    """Open a file dialog to select a JSON file and return its data."""
    file_path = filedialog.askopenfilename(
        title="Select JSON file",
        filetypes=[("JSON Files", "*.json")]
    )
    if not file_path:
        return None
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        messagebox.showerror("Error", f"Could not load JSON file:\n{e}")
        return None


def parse_event(event_str):
    """
    Parses an event string.

    Expected format: "|<event_code>|<x>,<y>|<...>"
    Returns:
      event_code (str): e.g. "mm", "cl", etc.
      coords (tuple): coordinates (x, y) as floats, or None if not found.
    """
    parts = event_str.split('|')
    if len(parts) < 3:
        return None, None
    event_code = parts[1]
    coord_str = parts[2]
    coords = None
    if ',' in coord_str:
        try:
            x_str, y_str = coord_str.split(',')
            coords = (float(x_str), float(y_str))
        except Exception as e:
            print(f"Error parsing coordinates '{coord_str}': {e}")
    return event_code, coords


def plot_all_events(data):
    """Plots all events (from 'el' in the JSON) using different colors."""
    events = data.get("el", [])
    event_data = {}

    # Group coordinates by event code.
    for event in events:
        event_code, coords = parse_event(event)
        if event_code is None or coords is None:
            continue
        event_data.setdefault(event_code, {"x": [], "y": []})
        event_data[event_code]["x"].append(coords[0])
        event_data[event_code]["y"].append(coords[1])

    plt.figure(figsize=(10, 8))
    for ev_code, coords in event_data.items():
        color = event_colors.get(ev_code, 'black')
        plt.scatter(coords["x"], coords["y"], c=color,
                    alpha=0.6, edgecolors='none', label=ev_code)

    plt.title("All Events")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)
    plt.legend(title="Event Type")
    # Invert the y-axis so 0,0 appears at the top left.
    plt.gca().invert_yaxis()
    plt.show()


def plot_clicks_only(data):
    """Plots only click ('cl') events and annotates their order with improved readability."""
    events = data.get("el", [])
    clicks = []

    # Only keep events with event code "cl".
    for event in events:
        event_code, coords = parse_event(event)
        if event_code == "cl" and coords is not None:
            clicks.append(coords)

    if not clicks:
        messagebox.showinfo("No Data", "No click ('cl') events found!")
        return

    plt.figure(figsize=(10, 8))
    x_coords = [pt[0] for pt in clicks]
    y_coords = [pt[1] for pt in clicks]

    plt.scatter(x_coords, y_coords, c=event_colors.get("cl", 'green'),
                alpha=0.8, edgecolors='none', s=100, label="cl")

    # Annotate each click with its order using a bounding box for clarity.
    for idx, (x, y) in enumerate(clicks, start=1):
        plt.text(x, y, str(idx),
                 fontsize=12, color='black', fontweight='bold',
                 ha='center', va='center',
                 bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

    plt.title("Click Events (Order Annotated)")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)
    plt.legend()
    # Invert the y-axis so 0,0 appears at the top left.
    plt.gca().invert_yaxis()
    plt.show()


def launch_plot(mode):
    """Loads the JSON and plots based on the selected mode."""
    data = load_json()
    if not data:
        return
    if mode == "all":
        plot_all_events(data)
    elif mode == "click":
        plot_clicks_only(data)
    else:
        messagebox.showerror("Error", "Unknown mode selected.")


def create_main_window():
    """Creates the main Tkinter window for mode selection."""
    root = tk.Tk()
    root.title("JSON Movement Viewer")
    root.geometry("300x150")

    label = tk.Label(root, text="Select a Mode to Display Events:",
                     font=("Arial", 12))
    label.pack(pady=10)

    btn_all = tk.Button(root, text="Show All Events",
                        command=lambda: [root.destroy(), launch_plot("all")],
                        width=20)
    btn_all.pack(pady=5)

    btn_click = tk.Button(root, text="Show Click Events Only",
                          command=lambda: [root.destroy(), launch_plot("click")],
                          width=20)
    btn_click.pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    create_main_window()
