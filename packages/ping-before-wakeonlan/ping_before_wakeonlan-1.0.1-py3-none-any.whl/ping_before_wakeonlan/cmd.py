# -*- encoding: utf-8 -*-
import sys
import json
import argparse
import os.path
import re
import random
import socket
import subprocess
import select

from ping_before_wakeonlan import __version__

def jsonOutput(data):
    return json.dumps(data, sort_keys=True, indent=4)

def isValidMac(mac_address):
    mac_pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
    if re.match(mac_pattern, mac_address):
        return True
    else:
        return False

def sendMagicPacket(mac_address):
    data = b'FF' * 6 + bytes.fromhex(mac_address.replace(':', '').replace('-', '')) * 16
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(data, ('<broadcast>', 7))

def main():
    parser = argparse.ArgumentParser(description='A Simple Tool for Ping and WOL Usage')
    parser.add_argument('--max-wol-device', type=int, default=5, help='WOL device number per a run')
    parser.add_argument('--send-mode', type=str, choices=['sequential', 'random'], default='random', help='Adjust the order of input device')
    parser.add_argument('--silently', action='store_true', default=False, help='Process Report')
    parser.add_argument('--ping-cmd', type=str, default='ping -c 1 -W 3', help='Ping command for test device')
    parser.add_argument('--device-info', type=str, default=None, help='a file path with JSON format with [{"ip": "192.168.1.2", "macAddress":"XX:XX:XX:XX:XX:XX"} ]')
    args = parser.parse_args()

    output = {'ping': args.ping_cmd, 'maxCount': args.max_wol_device ,'count': 0, 'device': {'input': [], 'handled': [], 'online': [], 'skip':[], 'failed': []}, 'info': [],  'version': __version__ }

    if not args.device_info:
        output['info'].append(f"--device-info not set empty")
        testStdin, _, _ = select.select([sys.stdin], [], [], 0.8) 
        if not testStdin:
            output['info'].append(f"stdin empty")
        else:
            args.device_info = sys.stdin.read().strip()
    else:
        try:
            rawFileContent = None
            with open(args.device_info, 'r') as f:
                rawFileContent = f.read().strip()
                args.device_info = rawFileContent
        except Exception as e:
            output['info'].append(f"file read error: {args.device_info}, exception: {e}")
            pass

    if not args.device_info:
        print(jsonOutput(output))
        parser.print_help()
        sys.exit()

    deviceInfo = []
    try:
        for item in json.loads(args.device_info):
            passDeviceInfoCheck = True
            for field in ['ip', 'mac_address']:
                if field not in item:
                    passDeviceInfoCheck = False
            try:
                socket.inet_aton(item['ip'])
            except:
                output['info'].append(f'test ip failed: {item}')
                passDeviceInfoCheck = False
            if not isValidMac(item['mac_address']):
                output['info'].append(f'test mac_address failed: {item}')
                passDeviceInfoCheck = False
            if passDeviceInfoCheck:
                deviceInfo.append(item)
    except Exception as e:
        output['info'].append(f'device_info format error: {args.device_info}, error: {e}')
        print(jsonOutput(output))
        parser.print_help()
        sys.exit()

    if len(deviceInfo) == 0:
        output['info'].append(f'device_info not found: {args.device_info}')
        print(jsonOutput(output))
        parser.print_help()
        sys.exit()

    if args.send_mode == 'random':
        random.shuffle(deviceInfo)

    for index, item in enumerate(deviceInfo):
        output['device']['input'].append(item)
        if output['count'] >= output['maxCount']:
             output['device']['skip'].append(item)
             continue
        if not args.silently:
            print(f'Process: { index + 1} / {len(deviceInfo)}: Device: {item}', file=sys.stderr)
        try:
            #response = os.system(f"{args.ping_cmd} '{item['ip']}'")
            #if response == 0:
            cmd = args.ping_cmd.split(" ") + [item['ip']]
            output['info'].append(f"cmd: {cmd}, item: {item}")
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            processOutput, processError = process.communicate()
            output['info'].append(f"processOutput: {processOutput}, processError: {processError}")
            if process.returncode == 0:
               output['device']['online'].append(item)
            else:
               try:
                   sendMagicPacket(item['mac_address'])
                   output['device']['handled'].append(item)
                   output['count'] += 1
               except Exception as e:
                   output['device']['failed'].append(item)
                   output['info'].append(f'sendMagicPacket failed: {item}, {e}')
        except Exception as e:
            output['device']['failed'].append(item)
            output['info'].append(f'ping failed: {item}, {e}')
    output['status'] = len(output['device']['failed']) == 0
    print(jsonOutput(output))

if __name__ == '__main__':
    main()
