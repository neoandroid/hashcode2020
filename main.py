#!/usr/bin/env python3
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--input', required=True, help='Input file')
    # parser.add_argument('--output', required=True, help='Output file')
    return parser.parse_args()


def read_input(myargs):
    photos = []
    with open(myargs.input) as f:
        lines = f.readlines()
        num_photos = int(lines[0])
        for idx, line in enumerate(lines[1:]):
            orientation, num, cats = line.strip().split(' ', 2)
            cats_list = cats.split()
            photos.append((idx, orientation, int(num), set(cats_list)))
    return num_photos, photos


def main():
    myargs = parse_args()
    num_photos, photos = read_input(myargs)
    print('Number of photos: {}'.format(num_photos))
    for i in photos:
        print(i)





if __name__ == "__main__":
    main()
