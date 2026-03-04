import paramiko
import paramiko.util
import win32com.client
from datetime import datetime
import socket

# Enable paramiko log
paramiko.util.log_to_file('paramiko.log')

# -------------------------------------------------------------------
# 🔐 SAFE FOR GITHUB: Placeholder credentials
# -------------------------------------------------------------------
common_credentials = {
    'username': 'YOUR_USERNAME_HERE',
    'password': 'YOUR_PASSWORD_HERE'
}

# -------------------------------------------------------------------
# 🔐 SAFE JSON TEMPLATE (your requested version)
# -------------------------------------------------------------------
commands_data = {
    "SERVER_NAME_1": [
        {
            "command": "your_command_here",
            "present": [
                "expected_output_1",
                "expected_output_2"
            ]
        }
    ],

    "SERVER_NAME_2": [
        {
            "command": "your_second_command_here",
            "present": [
                "expected_string_1",
                "expected_string_2"
            ]
        }
    ]
}

# Collect output and error messages in lists
output_list = []
error_messages = []

# Iterate through each server and its commands
for hostname, commands in commands_data.items():
    ssh = None
    try:
        output_list.append(f"<br><br><span style='color: blue; font-weight: bold;'><strong>Connecting to {hostname}...</strong></span><br>")
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname,
            username=common_credentials["username"],
            password=common_credentials["password"],
        )

        for command_info in commands:
            command = command_info['command']
            expected_output = command_info['present']

            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode('utf-8')

            for keyword in expected_output:
                if keyword in output:
                    output_list.append(f"<span style='color:green;'>{keyword} is running on {hostname}</span>")
                else:
                    output_list.append(f"<span style='color:red;'>{keyword} is not running on {hostname}</span>")

    except paramiko.AuthenticationException as e:
        error_messages.append("<br><br><br><strong style='color:red;'>Errors occurred while processing this automation: </strong>")
        error_messages.append(f"<br><span style='color:red;'>Error connecting to {hostname}: {str(e)} — Check login credentials 🔑</span>")

    except socket.gaierror as e:
        error_messages.append("<br><br><br><strong style='color:red;'>Errors occurred while processing this automation: </strong>")
        error_messages.append(f"<br><span style='color:red;'>Hostname resolution failed for {hostname}: {str(e)} ❌❌❌</span>")

    except paramiko.SSHException as e:
        error_messages.append("<br><br><br><strong style='color:red;'>Errors occurred while processing this automation: </strong>")
        error_messages.append(f"<br><span style='color:red;'>SSH error for {hostname}: {str(e)} ⚠️</span>")

    except Exception as e:
        error_messages.append("<br><br><br><strong style='color:red;'>Unexpected errors occurred while processing this automation: </strong>")
        error_messages.append(f"<br><span style='color:red;'>Unexpected error for {hostname}: {str(e)} ⚠️</span>")
        
    finally:
        if ssh:
            ssh.close()

# Join the output list and error_messages list into an HTML-formatted string
output_html = "<br>".join(output_list)
error_html = "<br>".join(error_messages)

# Get the current date & time
current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%m/%d/%Y %H: %M")

# Create an Outlook mail
outlook = win32com.client.Dispatch('Outlook.Application')
mail = outlook.CreateItem(0)

# -------------------------------------------------------------------
# 🔐 SAFE SUBJECT (changed here)
# -------------------------------------------------------------------
mail.Subject = f'COMMON AUTOMATION STATUS - {formatted_datetime}'

mail.HTMLBody = f'<span style="font-family: Courier New; font-size:10pt;">{output_html}<br>{error_html}</span>'

# -------------------------------------------------------------------
# 🔐 SAFE EMAIL PLACEHOLDERS
# -------------------------------------------------------------------
mail.To = 'recipient@example.com'
mail.Cc = 'cc@example.com'

# Display the mail
mail.Display()