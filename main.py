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
        days = int(days)
        print('Books: {}, Libraries: {}, Days: {}'.format(books_count, libraries, days))
        book_scores = lines[1].split()
        book_scores_dict = {}
        for idx, book_score in enumerate(book_scores):
            book_scores_dict[idx] = int(book_score)

        # print('Book score dict: {}'.format(book_scores_dict))

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
                books_index_set = set(map(int, line.split()))
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
    sorted_libraries = sorted(libraries, key=lambda x: x.signup_days, reverse=False)
    print(sorted_libraries)
    for library in sorted_libraries:
        print(library.books_index_set)
        library.scanned_books_list = library.books_index_set
    return sorted_libraries


def run_generic_algorithm(books_count, days, book_scores_dict, libraries):
    days_remaining = days
    already_scanned_books_set = set()
    output_libraries = list()
    total_score = 0
    while True:
        print("Remaining days: {}".format(days_remaining))
        for library in libraries:
            max_value, scanned_books_list = find_library_value_and_books(library, days_remaining, already_scanned_books_set, book_scores_dict)
            library.max_value = max_value
            library.scanned_books_list = scanned_books_list
            library.magic_ratio = max_value / library.signup_days

        sorted_libraries = sorted(libraries, key=lambda x: x.magic_ratio, reverse=True)

        # we have chosen a winner, update the values
        winner_library = sorted_libraries.pop(0)
        if winner_library.max_value == 0:
            print('Got max_value 0')
            # we can't scan anything anymore, bail
            break
        total_score += winner_library.max_value
        days_remaining -= winner_library.signup_days
        winner_library_books_set = set(winner_library.scanned_books_list)
        already_scanned_books_set = already_scanned_books_set.union(winner_library_books_set)
        output_libraries.append(winner_library)
        libraries = sorted_libraries
        if not libraries:
            print('Run out of libraries')
            break

    print("Total libraries: {}".format(len(output_libraries)))
    print("Total score: {}".format(total_score))

    return output_libraries


def find_library_value_and_books(library, days_remaining, already_scanned_books_set, book_scores_dict):
    days_available = days_remaining - library.signup_days
    if days_available <= 0:
        return 0, []
    books_not_scanned = library.books_index_set - already_scanned_books_set
    max_books_we_can_scan = days_available * library.ship_books_per_day

    my_books_dict = dict()
    for book_index in books_not_scanned:
        my_books_dict[book_index] = book_scores_dict[book_index]

    books_added = 0
    library_value = 0
    scanned_books_list = list()
    for k, v in sorted(my_books_dict.items(), key=lambda item: item[1]):
        library_value += v
        scanned_books_list.append(k)
        books_added += 1
        if books_added == max_books_we_can_scan:
            break

    return library_value, scanned_books_list


def main():
    myargs = parse_args()
    books_count, days, book_scores_dict, libraries = read_input(myargs)
    print('Books: {}, Days: {}'.format(books_count, days))
    # print('Book score dict: {}'.format(book_scores_dict))
    for library in libraries:
        pass
        # print('Book library: {}'.format(library.__dict__))

    # Task
    if myargs.input.find('b_read_on.txt') != -1:
        print("Sample b hack")
        libraries_solved = solve_case_b(books_count, days, book_scores_dict, libraries)
    elif myargs.input.find('d_tough_choices.txt') != -1:
        print("Sample d hack")
        libraries_solved = solve_case_b(books_count, days, book_scores_dict, libraries)
    else:
        print("Generic solution")
        libraries_solved = run_generic_algorithm(books_count, days, book_scores_dict, libraries)
        # run_fake_algorithm(libraries)

    print_output('output.txt', libraries_solved)


if __name__ == "__main__":
    main()
