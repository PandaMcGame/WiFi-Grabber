import os

if os.name != "nt":
    quit()

import re
import subprocess


def wifi_display():
    """Display stored Wi-Fi SSID and password"""

    command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()
    profile_names = (re.findall("All User Profile     : (.*)\r", command_output))

    wifi_list = list()

    # Check if there is Wi-Fi stored in the computer.
    if len(profile_names) != 0:
        for name in profile_names:
            # Each Wi-Fi connection will have its own dictionary.
            wifi_profile = dict()

            profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name],
                                          capture_output=True).stdout.decode()

            # If Wi-Fi has no Security Key (Public Wi-Fi), we ignore them.
            if re.search("Security key           : Absent", profile_info):
                continue
            else:
                wifi_profile["ssid"] = name

                # Get Wi-Fi password.
                profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"],
                                                   capture_output=True).stdout.decode()
                password = re.search("Key Content            : (.*)\r", profile_info_pass)

                if password is None:
                    wifi_profile["password"] = None
                else:
                    wifi_profile["password"] = password[1]

                # Append the SSID and password to the dictionary.
                wifi_list.append(wifi_profile)

        return wifi_list


if __name__ == '__main__':
    # Display all the Wi-Fi and password
    wifi = wifi_display()

    # Check if the list is not empty
    if wifi:
        for i in range(len(wifi)):
            print(f"{wifi[i]}")
    else:
        print("\nThis computer does not have Wi-Fi stored inside!")

    input("\nPress enter to continue...")
