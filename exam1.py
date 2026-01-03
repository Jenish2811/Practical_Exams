import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
class FitnessTracker:
    def __init__(self):
        self.activities = pd.DataFrame(columns=['Date', 'ActivityType', 'DurationMin', 'CaloriesBurned', 'DistanceKM'])
        self.health_metrics = {}

    def log_activity(self, activity_type, duration_min, distance_km=0):
        """Logs a new fitness activity."""
        date = datetime.date.today().strftime("%Y-%m-%d")
        if activity_type == 'Running':
            calories = duration_min * 10
        elif activity_type == 'Cycling':
            calories = duration_min * 7
        else:
            calories = duration_min * 5 
        
        new_activity = {
            'Date': date,
            'ActivityType': activity_type,
            'DurationMin': duration_min,
            'CaloriesBurned': calories,
            'DistanceKM': distance_km
        }
        
        self.activities = pd.concat([self.activities, pd.DataFrame([new_activity])], ignore_index=True)
        print(f"\nActivity logged successfully: {activity_type} for {duration_min} minutes.")

    def log_health_metric(self, metric_name, value):
        """Logs a current health metric (e.g., weight, heart rate)."""
        date = datetime.date.today().strftime("%Y-%m-%d")
        if metric_name not in self.health_metrics:
            self.health_metrics[metric_name] = pd.DataFrame(columns=['Date', 'Value'])
        
        new_metric = {'Date': date, 'Value': value}
        self.health_metrics[metric_name] = pd.concat([self.health_metrics[metric_name], pd.DataFrame([new_metric])], ignore_index=True)
        print(f"Health metric '{metric_name}' logged: {value}.")

    def calculate_weekly_summary(self):
        """Calculates and returns a weekly summary of activities."""
        self.activities['Date'] = pd.to_datetime(self.activities['Date'])
    
        weekly_summary = self.activities.set_index('Date').resample('W').agg({
            'DurationMin': 'sum',
            'CaloriesBurned': 'sum',
            'DistanceKM': 'sum'
        })
        
        average_duration_all_time = np.mean(self.activities['DurationMin'].to_numpy())
        
        print("\n--- Weekly Activity Summary ---")
        print(weekly_summary)
        print(f"\nAverage duration across all logged activities: {average_duration_all_time:.2f} minutes.")
        return weekly_summary

    def get_activity_data(self):
        """Returns the main activity DataFrame."""
        return self.activities

    def get_health_data(self, metric_name):
        """Returns specific health metric data."""
        return self.health_metrics.get(metric_name, pd.DataFrame())

def visualize_activity_trends(df):
    """Generates a bar plot of total duration by activity type using Seaborn."""
    if df.empty:
        print("Not enough data to visualize activity trends.")
        return

    plt.figure(figsize=(10, 6))
    summary = df.groupby('ActivityType')['DurationMin'].sum().reset_index()
    sns.barplot(x='ActivityType', y='DurationMin', data=summary, palette='viridis')
    plt.title('Total Duration Spent per Activity Type')
    plt.xlabel('Activity Type')
    plt.ylabel('Total Duration (Minutes)')
    plt.show()

def visualize_progress_over_time(df, metric='CaloriesBurned'):
    """Generates a line plot for a specific metric over time using Matplotlib."""
    if df.empty:
        print(f"Not enough data to visualize {metric} over time.")
        return

    df['Date'] = pd.to_datetime(df['Date'])
    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df[metric], marker='o', linestyle='-', color='b')
    plt.title(f'{metric} Progress Over Time')
    plt.xlabel('Date')
    plt.ylabel(f'{metric} Amount')
    plt.grid(True)
    plt.show()

def main_dashboard():
    """The main interface for the Fitness Tracker Dashboard."""
    tracker = FitnessTracker()
    print("Welcome to the Personal Fitness Tracker Dashboard!")
    print("Logging initial sample data...")
    tracker.log_activity('Running', 30, 4.5)
    tracker.log_activity('Cycling', 60, 15)
    tracker.log_activity('Running', 45, 6.0)
    tracker.log_health_metric('Weight_KG', 75.2)
    tracker.log_health_metric('Weight_KG', 74.8)
    print("-" * 40)

    while True:
        print("\nMenu Options:")
        print("1. Log a new activity")
        print("2. Log a health metric (e.g., Weight)")
        print("3. View Weekly Activity Summary")
        print("4. Visualize Activity Type Breakdown")
        print("5. Visualize Health Metric (Weight) over time")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            act_type = input("Enter Activity Type (e.g., Running, Cycling): ")
            duration = float(input("Enter Duration in minutes: "))
            distance = float(input("Enter Distance in KM (optional, enter 0 if N/A): "))
            tracker.log_activity(act_type, duration, distance)
            
        elif choice == '2':
            metric_name = input("Enter Metric Name (e.g., Weight_KG, restingHR_BPM): ")
            value = float(input(f"Enter value for {metric_name}: "))
            tracker.log_health_metric(metric_name, value)

        elif choice == '3':
            tracker.calculate_weekly_summary()

        elif choice == '4':
            visualize_activity_trends(tracker.get_activity_data())

        elif choice == '5':
            weight_data = tracker.get_health_data('Weight_KG')
            if not weight_data.empty:
                visualize_progress_over_time(weight_data, metric='Value')
            else:
                print("No weight data logged yet.")

        elif choice == '6':
            print("Exiting Fitness Tracker Dashboard. Stay healthy!")
            break
            
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
if __name__ == "__main__":
    sns.set_style("darkgrid") 
    main_dashboard()
