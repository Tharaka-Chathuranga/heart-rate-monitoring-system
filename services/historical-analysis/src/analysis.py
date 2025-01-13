import pandas as pd
from sqlalchemy import create_engine

# Database connection
db_engine = create_engine('postgresql://user:password@localhost/timeseries_db')

def calculate_baseline(user_id):
    # Fetch historical data for user
    query = f"SELECT timestamp, heart_rate FROM heart_rate_data WHERE user_id = '{user_id}'"
    df = pd.read_sql(query, db_engine)

    # Calculate baseline statistics
    avg_heart_rate = df['heart_rate'].mean()
    std_heart_rate = df['heart_rate'].std()
    baseline_info = {
        'average': avg_heart_rate,
        'threshold_high': avg_heart_rate + (2 * std_heart_rate),
        'threshold_low': avg_heart_rate - (2 * std_heart_rate)
    }

    # Update user profile with baseline info (hypothetical function)
    update_user_profile(user_id, baseline_info)
    return baseline_info

def update_user_profile(user_id, baseline_info):
    # Hypothetical function to update user profile
    print(f"Updating user profile for {user_id} with {baseline_info}")