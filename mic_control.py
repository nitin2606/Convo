import subprocess

def mute_microphone():
    try:
        # Run the pactl command to set the source (microphone) to mute
        subprocess.run(["pactl", "set-source-mute", "@DEFAULT_SOURCE@", "1"])
        print("Microphone muted")
    except subprocess.CalledProcessError as e:
        print(f"Unable to Mute Mic: {e}")

def unmute_microphone():
    try:
        # Run the pactl command to set the source (microphone) to unmute
        subprocess.run(["pactl", "set-source-mute", "@DEFAULT_SOURCE@", "0"])
        print("Microphone unmuted")
    except subprocess.CalledProcessError as e:
        print(f"Unable to Unmute Mic: {e}")


