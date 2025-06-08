def get_time(time_in_seconds):
    hours = time_in_seconds // 3600
    display_hours = hours if hours > 1 else 0
    minutes = time_in_seconds % 3600 / 60
    seconds = time_in_seconds % 60
    print(f"Il c'est écoule {display_hours} H {minutes} M {seconds} S")