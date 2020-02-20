#!/usr/bin/env python3
import argparse


class Library(object):
    library_index = None
    book_count = 0
    signup_days = 0
    ship_books_per_day = 0
    book_index_set = None

    def __init__(self, library_index, book_count, signup_days, ship_books_per_day):
        self.library_index = library_index
        self.book_count = book_count
        self.signup_days = signup_days
        self.ship_books_per_day = ship_books_per_day


def parse_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--input', required=True, help='Input file')
    # parser.add_argument('--output', required=True, help='Output file')
    return parser.parse_args()


def read_input(myargs):
    with open(myargs.input) as f:
        lines = f.readlines()
        header_line = lines[0]
        books_count, libraries, days = header_line.split()
        print('Books: {}, Libraries: {}, Days: {}'.format(books_count, libraries, days))
        book_scores = lines[1].split()
        book_scores_dict = {}
        for idx, book_score in enumerate(book_scores):
            book_scores_dict[idx] = book_score

        print('Book score dict: {}'.format(book_scores_dict))

        # a bit hacky, we define the library here to fill the data from its 2 lines
        libraries = list()
        library = None
        for idx, line in enumerate(lines[2:]):
            print(line)
            library_index = idx / 2
            if idx % 2 == 0:
                book_count, signup_days, ship_books_per_day = line.split()
                library = Library(library_index, book_count, signup_days, ship_books_per_day)
            else:
                books_index_set = set(line.split())
                library.books_index_set = books_index_set
                libraries.append(library)

    return books_count, days, book_scores_dict, libraries


def main():
    myargs = parse_args()
    books_count, days, book_scores_dict, libraries = read_input(myargs)
    print('Books: {}, Days: {}'.format(books_count, days))
    print('Book score dict: {}'.format(book_scores_dict))
    for library in libraries:
        print('Book library: {}'.format(library.__dict__))


if __name__ == "__main__":
    main()
