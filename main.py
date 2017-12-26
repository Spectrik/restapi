#!/usr/bin/python3

# Modules
import argparse
from http.server import HTTPServer
from daemonize import Daemonize
from handler import WebApiHandler

### Configuration

# PID file
pidfile = "/var/run/webapi.pid"

# HTTP server bind address
bind_address = ""

# HTTP server bind port
port = 80

# Foreground mode - useful i.e running this in docker container
foreground = False

# Main function to be run within the daemon
def main():
    # Create HTTP server object
    httpd = HTTPServer((bind_address, port), WebApiHandler)
    httpd.serve_forever()

# Command line arguments parsing
parser = argparse.ArgumentParser()
parser.add_argument("action", help="start, stop or restart", default="start", type=str)
parser.add_argument("--no-daemon", help="Use this option to run in foreground mode", action="store_true")
args = parser.parse_args()

if args.action not in ("start", "stop"):
    parser.error("Action must be either start or stop")

# Run daemonized or foreground?
if args.no_daemon:
    foreground = True

# Main
if __name__ == "__main__":

    # Create daemon class
    daemon = Daemonize(app="web_api", pid=pidfile, action=main, foreground=foreground)

    # Start / Stop logic
    if args.action == "start":
        print("Starting daemon...")
        daemon.start()

    elif args.action == "stop":
        print("Stopping daemon...")
        daemon.stop()
