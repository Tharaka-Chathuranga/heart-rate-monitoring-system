from analysis import calculate_baseline

def main():
    user_id = 'example_user_id'
    baseline_info = calculate_baseline(user_id)
    print(f"Baseline info for user {user_id}: {baseline_info}")

if __name__ == "__main__":
    main()