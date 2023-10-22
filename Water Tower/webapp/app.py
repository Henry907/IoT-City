from flask import Flask, jsonify, render_template, request
import os
import paho.mqtt.client as mqtt
import paramiko

red = False
yellow = False
green = False

app = Flask(__name__)

@app.route('/run-script')
def run_script():
    
    # Define the path to the HTML file on the remote server
    remote_file_path = '/home/lbc2/Desktop/BillboardManager/display.html'

    # Establish an SSH connection and update the specific line

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('192.168.2.10', username='lbc2', password='promhub')
        print("SSH Connection Successful")
        ssh.exec_command('sudo python3 lightsflash.py')
        ssh.close()

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('192.168.2.11', username='lbc2', password='promhub')

        # Read the current content of the HTML file
        stdin, stdout, stderr = ssh.exec_command(f'cat {remote_file_path}')
        current_html_content = stdout.read().decode('utf-8')

        # Use a regular expression to find and replace the line with the image tag
        pattern = r"<img src='.+\.png'>"
        updated_html_content = re.sub(pattern, "<img src='flood.png'>", current_html_content)

        # Write the updated content back to the HTML file
        with ssh.open_sftp().file(remote_file_path, 'w') as remote_file:
            remote_file.write(updated_html_content)

        # Close the SSH connection
        ssh.close()
        os.system('sudo python3 /home/lbc2/Desktop/test.py')

        
    except Exception as e:
        # Print the error to the Flask console terminal
        print(f"SSH Error: {str(e)}")
        return jsonify({'error': str(e)})
    #return




# ----- BILLBOARD CODE DO NOT TOUCH -----


import re

@app.route('/update_display', methods=['POST'])
def update_display():
    # Get the selected HTML content from the request
    new_html_content = request.form.get('new_html_content')

    # Define the path to the HTML file on the remote server
    remote_file_path = '/home/lbc2/Desktop/BillboardManager/display.html'

    # Establish an SSH connection and update the specific line
    import paramiko

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('192.168.2.11', username='lbc2', password='promhub')
        print("SSH Connection Successful")

        # Read the current content of the HTML file
        stdin, stdout, stderr = ssh.exec_command(f'cat {remote_file_path}')
        current_html_content = stdout.read().decode('utf-8')

        # Use a regular expression to find and replace the line with the image tag
        pattern = r"<img src='.+\.png'>"
        updated_html_content = re.sub(pattern, new_html_content, current_html_content)

        # Write the updated content back to the HTML file
        with ssh.open_sftp().file(remote_file_path, 'w') as remote_file:
            remote_file.write(updated_html_content)

        # Close the SSH connection
        ssh.close()

        return jsonify({'message': 'HTML file updated successfully'})
    except Exception as e:
        # Print the error to the Flask console terminal
        print(f"SSH Error: {str(e)}")
        return jsonify({'error': str(e)})
        
        
        
# ----- END OF BILLBOARD CODE ----



    
@app.route('/', methods=['GET', 'POST'])
def index():
    global red
    global yellow
    global green
    lights = request.form.get('lights')
    street = request.form.get('street')
    if street:
        client = mqtt.Client("streetlights")
        client.username_pw_set(username="lbc2", password="promhub")
        client.connect('192.168.2.7', 1883)
        print('street')
        if street == 'red':
            if red == True:
                client.publish(topic='lights/red',payload="off".encode('utf-8'),qos=0)
                red = False
            elif red != True:
                client.publish(topic='lights/red',payload="on".encode('utf-8'),qos=0)
                red = True
        if street == 'yellow':
            if yellow == True:
                client.publish(topic='lights/yellow',payload="off".encode('utf-8'),qos=0)
                yellow = False
            elif yellow != True:
                client.publish(topic='lights/yellow',payload="on".encode('utf-8'),qos=0)
                yellow = True
        if street == 'green':
            if green == True:
                client.publish(topic='lights/green',payload="off".encode('utf-8'),qos=0)
                green = False
            elif green != True:
                client.publish(topic='lights/green',payload="on".encode('utf-8'),qos=0)
                green = True
        print(red, yellow, green)
        client.disconnect()

    if lights:
        print('lights')
        if lights == 'on':
            print("on")
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('192.168.2.10', username='lbc2', password='promhub')
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('cd /home/lights')
            print(ssh_stdout.read().decode('utf-8'))
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo python3 lightson.py')
            print(ssh_stdout.read().decode('utf-8'))
            ssh.close()
        elif lights == 'off': 
            print("off") 
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('192.168.2.10', username='lbc2', password='promhub')
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('cd /home/lights')
            print(ssh_stderr.read().decode('utf-8'))
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo python3 lightsoff.py')
            print(ssh_stderr.read().decode('utf-8'))
            ssh.close()

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='80')
