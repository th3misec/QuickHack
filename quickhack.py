#!/usr/bin/env python3

import argparse
import subprocess
import sys
import os


def save_results(folder, filename, content):
    
    if folder:
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, filename)
        
        with open(path, "w") as f:
            f.write(content)
        print(f"\n[+] Results saved in: {path}\n")



# The user can choose between different types of scanning
def main():

    parser = argparse.ArgumentParser(
        description="Multi scan and recon tool",
        epilog="Ex: python quickhack.py ping 192.168.1.1",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument("--dir", dest="dir", help="The main folder for scan output and recon.", required=False)
    
    subparsers = parser.add_subparsers(
        dest="command",
        metavar="COMMAND",
        help="Types of scan",
        required=True
    )
    
    father = argparse.ArgumentParser(add_help=False)
    father.add_argument("target", help="IP or Domain target to scan")

    parser_whistle = subparsers.add_parser(
        "whistle", 
        parents=[father], 
        help="Scan the network like a ninja"
    )

    parser_ping = subparsers.add_parser(
        "ping", 
        parents=[father], 
        help="Normal scan"
    )

    parser_overheat = subparsers.add_parser(
        "overheat", 
        parents=[father], 
        help="The most agressive scan (use it carefully, too much noise but fast)"
    )

    args = parser.parse_args()


    if args.command == "whistle":
        try:
            comando = [
                'nmap', 
                '-sC', '-sV',
                '-Pn',
                '-T2',
                '--spoof-mac', '0', 
                '--min-rate', '300', 
                '-p-',
                '-D', 'RND:5',
                '--data-length', '25', 
                '-g 53',
                '--stats-every=5s',
                args.target
            ]
             
            print(f"\n[*] Executing: {' '.join(comando)}\n") 
        
            whistle_scan = subprocess.run(
                comando, 
                capture_output=True, 
                text=True, 
                check=True
            )
            
            print(whistle_scan.stdout)
            save_results(args.dir, "whistle_scan.txt", whistle_scan.stdout)

        except subprocess.CalledProcessError as e:
            print(f"\n[!] Error on Nmap (Exit Code: {e.returncode})")
    


    elif args.command == "ping":
        try:
            comando = [
                'nmap', 
                '-sS',
                '-Pn', '-n',
                '--open', 
                '--min-rate', '3000', 
                '--top-ports', '1000',
                '--stats-every=5s',
                args.target
            ]
             
            print(f"\n[*] Executing: {' '.join(comando)}\n") 
        
            ping_scan = subprocess.run(
                comando, 
                capture_output=True, 
                text=True, 
                check=True
            )
            
            print(ping_scan.stdout)
            save_results(args.dir, "ping_scan.txt", ping_scan.stdout)

        except subprocess.CalledProcessError as e:
            print(f"\n[!] Error on Nmap (Exit Code: {e.returncode})")



    elif args.command == "overheat":
        try:
            comando = [
                'nmap', 
                '-sC', '-sV',
                '-Pn', '-n',
                '-O', 
                '--min-rate', '5000',
                '-T5',
                '-p-',
                '-vvv',
                '--max-retries', '2',
                '--stats-every=5s',
                args.target
            ]
             
            print(f"\n[*] Executing: {' '.join(comando)}\n") 
        
            ping_scan = subprocess.run(
                comando, 
                capture_output=True, 
                text=True, 
                check=True
            )
            
            print(ping_scan.stdout)
            save_results(args.dir, "ping_scan.txt", ping_scan.stdout)

        except subprocess.CalledProcessError as e:
            print(f"\n[!] Error on Nmap (Exit Code: {e.returncode})")


    else:
    # This block throws an error due to an instruction or command error on the part of the user.
        print(f"\n[!] Error: The command '{args.command}' is not implemmented.")
        exit(1)




if __name__ == "__main__":
    main()
