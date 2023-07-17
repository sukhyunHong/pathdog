import psutil

pid = 2347  # Change this to your process ID

#if psutil.pid_exists(pid):
process = psutil.Process(pid)
print(f"PID: {process.pid}")
print(f"Name: {process.name()}")
print(f"Status: {process.status()}")
print(f"CPU percent: {process.cpu_percent()}")
print(f"Memory percent: {process.memory_percent()}")
#else:
print(f"No process with PID {pid}")

