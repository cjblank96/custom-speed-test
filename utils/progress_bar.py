import sys

def progress_bar(task_name, current, total, speed):
    """
    Displays a real-time progress bar in the terminal.

    :param task_name: Task name (Download/Upload/Ping)
    :param current: Current data transferred or progress value
    :param total: Total data to transfer or complete
    :param speed: Current speed in Mbps
    """
    bar_length = 50
    progress = current / total
    filled_length = int(bar_length * progress)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f"\r{task_name}: |{bar}| {progress * 100:.2f}% "
                     f"{current:.2f}/{total:.2f} MB "
                     f"Speed: {speed:.2f} Mbps")
    sys.stdout.flush()
    if current >= total:
        print(f"\n✅ {task_name} Completed!\n")