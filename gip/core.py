#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description='Pip style script for Gitlab')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')
