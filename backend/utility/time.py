def getTime(timeInSeconds):
    hours = timeInSeconds // 3600
    displayHours = hours if hours > 1 else 0
    minutes = timeInSeconds % 3600 / 60
    seconds = timeInSeconds % 60
    print(f"Il c'est écoule {displayHours} H {minutes} M {seconds} S")