import sys

import broker

def process_args():
    print("Program loaded")
    if len(sys.argv) > 1:
        if sys.argv[1] == "login":
            print("Logging in...")
            broker.Login().login()

if __name__ == "__main__":
    process_args()

