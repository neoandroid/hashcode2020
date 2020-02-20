#!/usr/bin/env python3
import argparse


class Library(object):
    library_index = None
    book_count = 0
    signup_days = 0
    ship_books_per_day = 0
    books_index_set = None

    def __init__(self, library_index, book_count, signup_days, ship_books_per_day):
        self.library_index = int(library_index)
        self.book_count = int(book_count)
        self.signup_days = int(signup_days)
        self.ship_books_per_day = int(ship_books_per_day)

    def __repr__(self):
        return "<Library: index:%s signup_delay:%s>" % (self.library_index, self.signup_days)


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
            # print("Line: {}".format(line))
            if line == '\n':
                continue
            library_index = int(idx / 2)
            if idx % 2 == 0:
                book_count, signup_days, ship_books_per_day = line.split()
                library = Library(library_index, book_count, signup_days, ship_books_per_day)
            else:
                books_index_set = set(line.split())
                library.books_index_set = books_index_set
                libraries.append(library)

    return books_count, days, book_scores_dict, libraries


def print_output(output_file_name, scanned_libraries_list):
    with open(output_file_name, 'w') as f:
        f.write("{}\n".format(len(scanned_libraries_list)))
        for library in scanned_libraries_list:
            f.write("{} {}\n".format(library.library_index, len(library.scanned_books_list)))
            f.write(" ".join(map(str, library.scanned_books_list)))
            f.write('\n')


def run_fake_algorithm(libraries):
    libraries[0].scanned_books_list = [0, 1, 2, 3, 4]
    libraries[1].scanned_books_list = [0, 2]


def solve_case_b(books_count, days, book_scores_dict, libraries):
    # 100000 books, all socre 100
    # 100 librares, all ship 1 book
    # 1000 days
    print("Start")
    how_many_singups = 100
    sorted_libraries = sorted(libraries, key=lambda x: x.signup_days, reverse=False)
    print(sorted_libraries)
    for library in sorted_libraries:
        print(library.books_index_set)
        library.scanned_books_list = library.books_index_set
    for librari in sorted_libraries:
        print(library.scanned_books_list)
    return sorted_libraries


def main():
    myargs = parse_args()
    books_count, days, book_scores_dict, libraries = read_input(myargs)
    print('Books: {}, Days: {}'.format(books_count, days))
    print('Book score dict: {}'.format(book_scores_dict))
    for library in libraries:
        print('Book library: {}'.format(library.__dict__))

    run_fake_algorithm(libraries)

    # Task
    if myargs.input.find('b_read_on.txt') != -1:
        libraries_solved = solve_case_b(books_count, days, book_scores_dict, libraries)
    elif myargs.input.find('d_tough_choices.txt'):
        libraries_solved = solve_case_b(books_count, days, book_scores_dict, libraries)

    print_output('output.txt', libraries_solved)


if __name__ == "__main__":
    main()
