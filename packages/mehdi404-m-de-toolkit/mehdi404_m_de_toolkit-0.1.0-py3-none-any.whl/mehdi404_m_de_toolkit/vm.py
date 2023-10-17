import click
import subprocess

@click.command()
def start():
    """Start your vm"""
    subprocess.run(["gcloud", "compute" , "instances", "start",
                "data-eng-vm"])

@click.command()
def stop():
    """Stop your vm"""
    subprocess.run(["gcloud", "compute" , "instances", "stop",
                "data-eng-vm"])

@click.command()
def connect():
    """Connect to your vm"""
    subprocess.run(["code", "--folder-uri",
        "vscode-remote://ssh-remote+mehdi_DE/home/mehdi.messaoudi/code/code/mehdi404-m/"])
