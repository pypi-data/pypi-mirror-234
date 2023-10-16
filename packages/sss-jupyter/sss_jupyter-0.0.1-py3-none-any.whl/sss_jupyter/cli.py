import argparse
import os
import subprocess

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8888,
        help="The port the server will listen on."
    )
    parser.add_argument(
        "-l",
        "--token_length",
        type=int,
        default=50,
        help="The character length of a secret token."
    )
    args = parser.parse_args()
    return args

def main():
    args = get_args()
    file_dir = os.path.dirname(__file__)
    file_shell = os.path.join(file_dir, "launch.sh")
    subprocess.run(f"bash {file_shell} -p {args.port} -l {args.token_length}", shell=True)

