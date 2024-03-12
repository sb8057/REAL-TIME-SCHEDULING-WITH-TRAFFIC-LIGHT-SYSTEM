import tkinter as tk
from threading import Thread
import time
import random
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TrafficControlSimulator:
    def __init__(self, master, signals, lanes):
        self.master = master
        self.signals = signals
        self.lanes = lanes
        self.total_time = 60
        self.current_time = 0
        self.current_signal_index = 0

        self.setup_gui()
        self.setup_gantt_chart()

    def setup_gui(self):
        self.master.title("Traffic Control Simulator")

        self.signal_label = tk.Label(self.master, text="Traffic Signals", font=("Helvetica", 16, "bold"))
        self.signal_label.pack()

        self.signal_frame = tk.Frame(self.master)
        self.signal_frame.pack()

        self.lane_label = tk.Label(self.master, text="Traffic Lanes", font=("Helvetica", 16, "bold"))
        self.lane_label.pack()

        self.lane_frame = tk.Frame(self.master)
        self.lane_frame.pack()

        self.start_button = tk.Button(self.master, text="Start Simulation", command=self.start_simulation, font=("Helvetica", 14))
        self.start_button.pack()

    def update_gui(self):
        for widget in self.signal_frame.winfo_children():
            widget.destroy()

        for signal in self.signals:
            label = tk.Label(self.signal_frame, text=f"Signal {signal['id']}: {signal['duration']} seconds", font=("Helvetica", 12))
            label.pack(side=tk.LEFT)

        for widget in self.lane_frame.winfo_children():
            widget.destroy()

        for lane in self.lanes:
            label = tk.Label(self.lane_frame, text=f"Lane {lane['id']}: {lane['vehicles']} vehicles", font=("Helvetica", 12))
            label.pack(side=tk.LEFT)

    def setup_gantt_chart(self):
        self.figure = Figure(figsize=(8, 2), tight_layout=True, facecolor='lightgray')
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Traffic Signal Gantt Chart")
        self.ax.set_yticks([])
        self.ax.set_xlabel("Time (seconds)")
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.get_tk_widget().pack()

    def update_gantt_chart(self, signal_id, start_time, duration):
        self.ax.barh(0, width=duration, left=start_time, color=f"C{signal_id}", edgecolor="black", height=0.5)
        self.canvas.draw()

    def simulate_traffic(self):
        for _ in range(self.total_time):
            current_signal = self.signals[self.current_signal_index]
            current_signal['duration'] -= 1
            self.update_gantt_chart(self.current_signal_index, self.current_time, 1)

            for lane_id in range(len(self.lanes)):
                if random.uniform(0, 1) < 0.3:  # Varying traffic density
                    if current_signal['id'] == self.lanes[lane_id]['id']:
                        self.lanes[lane_id]['vehicles'] += random.randint(0, 3)
                    else:
                        self.lanes[lane_id]['vehicles'] = max(0, self.lanes[lane_id]['vehicles'] - random.randint(0, 2))

            time.sleep(1)
            self.current_time += 1

            if current_signal['duration'] == 0:
                self.current_signal_index = (self.current_signal_index + 1) % len(self.signals)
                current_signal['duration'] = random.randint(5, 15)  # Variable signal duration

            self.update_gui()

        self.master.after(0, self.show_simulation_complete)

    def start_simulation(self):
        self.start_button.config(state=tk.DISABLED)
        simulation_thread = Thread(target=self.simulate_traffic)
        simulation_thread.start()

    def show_simulation_complete(self):
        self.start_button.config(state=tk.NORMAL)
        messagebox.showinfo("Simulation Complete", "Traffic simulation completed!")

if __name__ == "__main__":
    signals = [
        {"id": 1, "duration": random.randint(5, 15)},
        {"id": 2, "duration": random.randint(5, 15)},
        {"id": 3, "duration": random.randint(5, 15)},
    ]

    lanes = [
        {"id": 1, "signalId": 0, "vehicles": 0},
        {"id": 2, "signalId": 1, "vehicles": 0},
        {"id": 3, "signalId": 2, "vehicles": 0},
    ]

    root = tk.Tk()
    simulator = TrafficControlSimulator(root, signals, lanes)
    root.mainloop()
