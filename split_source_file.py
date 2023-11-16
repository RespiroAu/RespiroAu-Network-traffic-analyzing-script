# This script is used to split the log file for each source VPC we are interested in.


# Imports

import pandas as pd
import ipaddress
import csv

# Globals
cidr = ipaddress.IPv4Network("10.72.0.0/21")
# Functions

def read_csv(filename):
    print('in read_csv\n')
    df = pd.read_csv(filename)

    src_match = df[df['Src Address'].apply(lambda x: ipaddress.ip_address(x) in cidr)]
    dst_match = df[df['Dst Address'].apply(lambda x: ipaddress.ip_address(x) in cidr)]
    src_match = src_match.drop_duplicates(subset='Dst Address')
    dst_match = dst_match.drop_duplicates(subset='Src Address')
    combine = pd.concat([src_match, dst_match])

    write_dst_add(src_match, 'Required Destination Addresses (No Dupes).csv')

    write_src_add(dst_match,'Required Source Addresses (No Dupes).csv')
    write_all_add(combine,'all_matched_dts_src.csv')


def write_dst_add(src_match, output_filename):
    src_match['VPC Name'] = ''
    src_match[['Src Address', 'Src Port', 'Dst Address', 'Dst Port', 'VPC Name']].to_csv(output_filename, index=False)
def write_src_add(dst_match, output_filename):
    dst_match['VPC Name'] = ''
    dst_match[['Src Address', 'Src Port', 'Dst Address', 'Dst Port', 'VPC Name']].to_csv(output_filename, index=False)
    #dst_match["Dst Address"].to_csv(output_filename, index=False)

def write_all_add(combine, output_filename):
    combine.to_csv(output_filename, index=False)

           



if __name__ == '__main__':
    print('in the main\n')
    read_csv('CG_NetworkTraffic_6f7e2266-8c79-4336-9de9-0a1ba781b2a0_2023-11-09_11_13_04.csv')
