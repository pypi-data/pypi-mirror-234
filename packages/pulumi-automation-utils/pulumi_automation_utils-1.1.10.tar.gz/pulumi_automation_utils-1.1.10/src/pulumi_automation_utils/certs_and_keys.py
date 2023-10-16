#!/usr/bin/env python3
import os
import subprocess

from pulumi_automation_utils.common import send_os_command

# The key pair needs to be put somewhere secure after creation
def create_key_pair(filename : str):
    if filename and os.path.isfile(filename) and os.path.exists(filename):
        if input("Would you like to overwrite the existing SSH key pair? [y/n]: ") == "y":
            pub_key_filename = os.path.join(os.path.dirname(filename), os.path.basename(filename) + ".pub")
            print("Removing " + filename)
            print("Removing " + pub_key_filename)
            os.remove(filename)
            os.remove(pub_key_filename)
        else:
            print("Using existing key pair.")
            return

    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    command = "ssh-keygen -t rsa -b 4096 -f " + filename + " -N ''"
    try:
        output = send_os_command(command=command, shell=True)
    except subprocess.CalledProcessError as e:
        print("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))

# The signed certificate and keypair need to be put somewhere secure after creation
def create_signed_certificate(ca_filename : str, cert_key_filename : str, hostname : str, username : str=None):
    if cert_key_filename and os.path.isfile(cert_key_filename) and os.path.exists(cert_key_filename):
        if input("Would you like to overwrite the existing SSH key pair? [y/n]: ") == "y":
            pub_key_filename = os.path.join(os.path.dirname(cert_key_filename), os.path.basename(cert_key_filename) + ".pub")
            print("Removing " + cert_key_filename)
            print("Removing " + pub_key_filename)
            os.remove(cert_key_filename)
            os.remove(pub_key_filename)
        else:
            print("Using existing key pair.")
            return

    if not os.path.exists(os.path.dirname(cert_key_filename)):
        os.makedirs(os.path.dirname(cert_key_filename))
    try:
        command = "ssh-keygen -f " + cert_key_filename + " -N '' -b 4096 -t rsa"
        output = send_os_command(command=command, shell=True)
        if username is None:
            command = "ssh-keygen -s " + ca_filename + " -I " + hostname + " -h -n " + hostname + " -P '' -V +52w " + cert_key_filename + ".pub"
        else:
            command = "ssh-keygen -s " + ca_filename + " -I " + username + "@" + hostname + " -n " + username + " -P '' -V +52w " + cert_key_filename + ".pub"
        output = send_os_command(command, shell=True)
    except subprocess.CalledProcessError as e:
        print("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
