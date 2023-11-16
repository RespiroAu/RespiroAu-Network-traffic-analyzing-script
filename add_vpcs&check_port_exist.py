# This is a script to find the VPCs associated with the source and
# This is a script to find the VPCs associated with the source and
# destination addresses from the required source and destination
# addresses csv file


# imports

import pandas as pd
import ipaddress
import csv
import socket
from openpyxl import load_workbook

#Globals
unknown_address= []

def check_tcp_known(checking_on):
    found = []
    tcp = ""
    tcp_ports = pd.read_csv('tcp.csv')
    for x in tcp_ports.index:
        if checking_on == tcp_ports['port'][x]:
            tcp = tcp_ports['description'][x]
            found.append(tcp)
    if found:
        return tcp
    else:
        return 'unknown'

def run_req_dests(filename):
    print('in run_req_dests\n')
    req_dest = pd.read_csv(filename)
    vpcs = pd.read_csv('VPCs.csv')
    headers = ['Source Address', 'Source Port', 'Port Name', 'Destination Address', 'Destination Port',
               'Port Name', 'VPC Name']

    matched = []
    temp = []
    global unknown_address
    with open('Required Destination Addresses with VPCs.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        # print(req_dest)
        for index in req_dest.index:
            # print(req_dest['Source Address'][index])
            ip = req_dest['Src Address'][index]
            ip_port = req_dest['Src Port'][index]
            dest_ip = req_dest['Dst Address'][index]
            dest_port = req_dest['Dst Port'][index]

            # print(ip)
            # print(type(ip))
            for x in vpcs.index:
                #print(vpcs['VPC CIDR'][x])
                if ipaddress.ip_address(dest_ip) in ipaddress.ip_network(vpcs['VPC CIDR'][x]):
                    #print('match found for: ', dest_ip, ' in: ', vpcs['VPC CIDR'][x])
                    vpc = vpcs['VPC CIDR'][x]
                    matched.append(vpc)
                else:
                    unknown_address.append(dest_ip)
            if matched:
                #print('Matched found', matched)
                temp.append(ip)
                temp.append(ip_port)
                #check
                temp.append(check_tcp_known(ip_port))

                temp.append(dest_ip)
                temp.append(dest_port)
                # check
                temp.append(check_tcp_known(dest_port))

                temp.append(matched)
                #print('printing temp', temp)
                writer.writerow(temp)

                temp.clear()
                matched.clear()
            else:
                temp.append(ip)
                temp.append(ip_port)
                temp.append(check_tcp_known(ip_port))

                temp.append(dest_ip)
                temp.append(dest_port)
                temp.append(check_tcp_known(dest_port))

                matched.append('Internet')
                temp.append(matched)
                writer.writerow(temp)
                temp.clear()
                matched.clear()


def run_req_src(filename):
    print('in run_req_src\n')
    req_src = pd.read_csv(filename)
    vpcs = pd.read_csv('VPCs.csv')
    tcp_ports = pd.read_csv('tcp.csv')
    headers = ['Source Address', 'Source Port', 'Port Name', 'Destination Address', 'Destination Port',
               'Port Name', 'VPC Name']
    temp = []
    matched = []
    global unknown_address
    with open('Required Source Addresses with VPCs.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)


        for index in req_src.index:
            ip = req_src['Dst Address'][index]
            ip_port = req_src['Dst Port'][index]
            # print(ip)
            src_ip = req_src['Src Address'][index]
            src_ip_port = req_src['Src Port'][index]

            for x in vpcs.index:
                # print(vpcs['VPC CIDR'][x])
                if ipaddress.ip_address(ip) in ipaddress.ip_network(vpcs['VPC CIDR'][x]):
                    #print('match found for: ', ip, ' in VPC: ', vpcs['VPC CIDR'][x])
                    vpc = vpcs['VPC CIDR'][x]
                    matched.append(vpc)
                else:
                    unknown_address.append(src_ip)
            if matched:
                #print('Matched found', matched)
                temp.append(src_ip)
                temp.append(src_ip_port)
                # check tcp known or not
                temp.append(check_tcp_known(src_ip_port))
                temp.append(ip)
                temp.append(ip_port)
                #check
                temp.append(check_tcp_known(ip_port))
                temp.append(matched)
                #print('printing temp', temp)
                writer.writerow(temp)

                temp.clear()
                matched.clear()
            else:
                temp.append(src_ip)
                temp.append(src_ip_port)
                temp.append(ip)
                temp.append(ip_port)
                matched.append('Internet')
                temp.append(matched)
                writer.writerow(temp)
                temp.clear()
                matched.clear()


def test_ip():
    sub = '192.168.0.0/24'
    ip = '192.168.0.1'
    if ipaddress.ip_address(ip) in ipaddress.ip_network(sub):
        print('matched')


def count_VPCs():
    print('in count_VPCs\n')
    req_src = 'Required Source Addresses with VPCs.csv'
    req_dst = 'Required Destination Addresses with VPCs.csv'
    vpcs = [
        '10.245.80.0/20',
        '10.245.24.0/21',
        '10.249.0.0/16',
        '10.0.0.0/8',
        '172.16.0.0/12',
        '192.168.0.0/16',
        '139.5.174.0/23',
        '141.243.0.0/16',
        '143.119.0.0/16',
        '144.130.7.5/32',
        '148.145.102.0/23',
        '150.1.0.0/16',
        '153.107.196.0/24',
        '153.107.226.24/29',
        '172.32.254.248/29',
        '198.19.248.64/28',
        '203.3.220.80/28',
        '203.11.0.0/16',
        '203.44.42.112/28',
        '10.250.176.0/20',
        'Internet',
        '13.210.28.64',
        '13.236.198.200',
        '54.153.163.193',
        '52.64.202.191',
        '52.65.194.103',
        '52.62.199.95',
        '10.8.0.0/14'
    ]
    src = pd.read_csv(req_src)
    dst = pd.read_csv(req_dst)

    # print(src)
    # print(dst)

    # for items in vpcs:
    #     print('*********************')
    #     print(items, type(items))
    #     print('*********************')

    # for items in src.index:
    #     print('*********************')
    #     print(src['VPC Name'][items], type(src['VPC Name'][items]))
    #     print('*********************')

    src_vpcs = []
    dst_vpcs = []
    count = 0

    # print('********************** Counting VPC occurrence of VPCs in Required Source Addresses with VPCs '
    #       '**********************')
    for items in vpcs:
        # print('items: ', items)
        for index in src.index:
            # print('src[VPC Name][index]: ', src['VPC Name'][index])
            if items in src['VPC Name'][index]:
                count += 1
        # print(count)
        src_vpcs.append(count)
        count = 0

    # this is counting VPC occurrence of VPCs in Required Source Addresses with VPCs

    for x in range(len(vpcs)):
        print(vpcs[x], ' : ', src_vpcs[x])

    # print('********************** Counting VPC occurrence of VPCs in Required Destination Addresses with VPCs '
    #       '**********************')
    for items in vpcs:
        # print('items: ', items)
        for index in dst.index:
            # print('dst[VPC Name][index]: ', dst['VPC Name'][index])
            if items in dst['VPC Name'][index]:
                count += 1
        # print(count)
        dst_vpcs.append(count)
        count = 0

    print('\n************************************************************\n')

    # this is counting VPC occurrence of VPCs in Required Source Addresses with VPCs

    for x in range(len(vpcs)):
        print(vpcs[x], ' : ', dst_vpcs[x])

    # now we write the summary file
    with open('VPCs Summary.txt', 'w') as f:
        f.write('VPC count for the Required Source Addresses with VPCs file')
        f.write('\n')
        f.write('\n')
        for x in range(len(vpcs)):
            if vpcs[x] == '10.245.80.0/20':
                f.write(vpcs[x])
                f.write('  sharedVPC')
                f.write(' : ')
                f.write(str(src_vpcs[x]))
                f.write('\n')
            elif vpcs[x] == '10.245.24.0/21':
                f.write(vpcs[x])
                f.write('  dmzVPC')
                f.write(' : ')
                f.write(str(src_vpcs[x]))
                f.write('\n')
            elif vpcs[x] == '10.249.0.0/16':
                f.write(vpcs[x])
                f.write('  tradeVPC')
                f.write(' : ')
                f.write(str(src_vpcs[x]))
                f.write('\n')
            elif vpcs[x] == '10.250.176.0/20':
                f.write(vpcs[x])
                f.write('  oosnonprod-vpc01')
                f.write(' : ')
                f.write(str(src_vpcs[x]))
                f.write('\n')
            else:
                f.write(vpcs[x])
                f.write(' : ')
                f.write(str(src_vpcs[x]))
                f.write('\n')
        f.write('Total: ')
        f.write(str(len(src.index)))

        f.write('\n')
        f.write('\n')

        f.write('VPC count for the Required Destination Addresses with VPCs file')
        f.write('\n')
        f.write('\n')

        for x in range(len(vpcs)):
            f.write(vpcs[x])
            f.write(' : ')
            f.write(str(dst_vpcs[x]))
            f.write('\n')
        f.write('Total: ')
        f.write(str(len(dst.index)))

def run_nslookup():
    unknown = list(dict.fromkeys(unknown_address))
    print(unknown)
    #print("frnwfrirehghiurehgiuregreiugejvrevpokekregopkrejoigoijd;oivnpuehgew")

    headers = ['Address', 'dns']
    with open('unknown addresses.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for index in unknown:
            print("running")
            this = socket.getnameinfo((index, 0), 0)
            if this[0] == index:
                writer.writerow([index, "unkown"])
            else:
                writer.writerow([index,this[0]])


if __name__ == '__main__':
    print('in the main\n')
    run_req_dests('Required Destination Addresses (No Dupes).csv')
    #test_ip()
    run_req_src('Required Source Addresses (No Dupes).csv')
    count_VPCs()
    run_nslookup()
