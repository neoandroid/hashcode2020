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
        return "<Library: index:%s signup_delay:%s num_books:%s>" % (self.library_index, self.signup_days, len(self.books_index_set))


def parse_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--input', required=True, help='Input file')
    parser.add_argument('--no-generic', dest='avoid_generic_alg', required=False, action='store_true', help='Do not run generic algorithm')
    # parser.add_argument('--output', required=True, help='Output file')
    parser.set_defaults(avoid_generic_alg=False)
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


def print_output(output_file_name, scanned_libraries_list, book_scores_dict):
    with open(output_file_name, 'w') as f:
        scanned_books_set = set()
        total_points = 0
        f.write("{}\n".format(len(scanned_libraries_list)))
        for library in scanned_libraries_list:
            for book in library.scanned_books_list:
                assert(book not in scanned_books_set)
                scanned_books_set.add(book)
                total_points += book_scores_dict[book]
            f.write("{} {}\n".format(library.library_index, len(library.scanned_books_list)))
            f.write(" ".join(map(str, library.scanned_books_list)))
            f.write('\n')

    print("Total points: {}, Scanned books: {}".format(
        total_points, len(scanned_books_set)
    ))


def run_fake_algorithm(libraries):
    libraries[0].scanned_books_list = [0, 1, 2, 3, 4]
    libraries[1].scanned_books_list = [0, 2]


def solve_case_b(books_count, days, book_scores_dict, libraries):
    # 100000 books, all socre 100
    # 100 librares, all ship 1 book, distinct delay time
    # 1000 days
    print("Start")
    sorted_libraries = sorted(libraries, key=lambda x: x.signup_days, reverse=False)
    print(sorted_libraries)
    for library in sorted_libraries:
        print(library.books_index_set)
        library.scanned_books_list = library.books_index_set
    return sorted_libraries


def solve_case_c(books_count, days, book_scores_dict, libraries):
    # 100000 books, distinct scores
    # 10000 librares, can ship lots of books, but they have very few
    # 100000 days
    print("Start")
    sorted_libraries = sorted(libraries, key=lambda x: x.signup_days, reverse=False)
    print(sorted_libraries)
    selected_libraries = []
    scanned_books = []
    first = True
    for library in sorted_libraries:
        if first:
            library.scanned_books_list = library.books_index_set
            scanned_books.extend(order_libray_books_by_points(library.books_index_set, book_scores_dict))
            selected_libraries.append(library)
        else:
            new_books = set(order_libray_books_by_points(library.books_index_set, book_scores_dict)) - set(scanned_books)
            library.scanned_books_list = new_books
            scanned_books.extend(list(new_books))
            if len(new_books) > 0 :
                selected_libraries.append(library)
        first = False
    return selected_libraries


def solve_case_d(books_count, days, book_scores_dict, libraries):
    # 78600 books, all socre 65
    # 30000 librares, all ship 1 book, all delay 2
    # 30001 days
    print("Start")
    sorted_libraries = sorted(libraries, key=lambda x: x.book_count, reverse=True)
    print(sorted_libraries)
    selected_libraries = []
    scanned_books = []
    first = True
    for library in sorted_libraries:
        if first:
            library.scanned_books_list = library.books_index_set
            scanned_books.extend(list(library.books_index_set))
            selected_libraries.append(library)
        else:
            new_books = set(library.books_index_set) - set(scanned_books)
            library.scanned_books_list = new_books
            scanned_books.extend(list(new_books))
            if len(new_books) > 0 :
                selected_libraries.append(library)
        first = False
    return selected_libraries


def solve_case_d_alg2(books_count, days, book_scores_dict, libraries):
    # 78600 books, all socre 65
    # 30000 librares, all ship 1 book, all delay 2
    # 30001 days
    print("Start")
    sorted_libraries = sorted(libraries, key=lambda x: x.book_count, reverse=True)
    print(sorted_libraries)
    selected_libraries = []
    scanned_books = []
    sorted_libraries[0].scanned_books_list = list(sorted_libraries[0].books_index_set)
    scanned_books.extend(list(sorted_libraries[0].books_index_set))
    selected_libraries.append(sorted_libraries[0])
    sorted_libraries.pop(0)
    remaining_libraries = sorted_libraries
    while len(selected_libraries) < 15001:
        # Remove_scanned_books
        remaining_libraries = remove_scanned_books(remaining_libraries, scanned_books)
        # Sort remaining libraries with the ones that have more books to scan
        sorted_remaining_libraries = sorted(remaining_libraries, key=lambda x: x.book_count, reverse=True)
        sorted_remaining_libraries[0].scanned_books_list = list(sorted_remaining_libraries[0].books_index_set)
        scanned_books.extend(sorted_remaining_libraries[0].scanned_books_list)
        selected_libraries.append(sorted_remaining_libraries[0])
        sorted_remaining_libraries.pop(0)
        remaining_libraries = sorted_remaining_libraries
        print(len(selected_libraries))

    return selected_libraries


def remove_scanned_books(libraries, scanned_books):
    good_libraries = []
    scanned_books_set = set(scanned_books)
    for library in libraries:
        books_not_scanned = library.books_index_set - scanned_books_set
        library.books_index_set = books_not_scanned
        library.book_count = len(library.books_index_set)
        if len(library.books_index_set) > 0:
            good_libraries.append(library)
    return good_libraries


def order_libray_books_by_points(books_set, books_scores_dict):
    my_books_dict = dict()
    for book_index in books_set:
        my_books_dict[book_index] = books_scores_dict[book_index]

    scanned_books_list = list()
    for k, v in sorted(my_books_dict.items(), key=lambda item: item[1], reverse=True):
        scanned_books_list.append(k)

    return scanned_books_list


def run_generic_algorithm(books_count, days, book_scores_dict, libraries):
    days_remaining = days
    already_scanned_books_set = set()
    output_libraries = list()
    total_score = 0
    while True:
        print("Remaining days: {}, Libraries used: {}, Libraries left: {}, Used books: {}/{}".format(
            days_remaining, len(output_libraries), len(libraries), len(already_scanned_books_set), books_count
        ))
        for library in libraries:
            max_value, scanned_books_list, can_wait = find_library_value_and_books(library, days_remaining, already_scanned_books_set, book_scores_dict)
            library.max_value = max_value
            library.scanned_books_list = scanned_books_list
            can_wait_bonus = 0 if can_wait else 2000
            library.magic_ratio = (max_value / library.signup_days) + can_wait_bonus
            # library.magic_ratio = (max_value / library.signup_days) * library.ship_books_per_day
            # library.magic_ratio = (1 / library.signup_days) * library.ship_books_per_day

        # sort the libraries by magic ratio
        sorted_libraries = sorted(libraries, key=lambda x: x.magic_ratio, reverse=True)

        # we have chosen a winner, update the values
        winner_library = sorted_libraries.pop(0)
        if winner_library.max_value == 0:
            print('Got max_value 0')
            # we can't scan anything anymore, bail
            break
        print("Chose library with: max_value: {}, total_books: {}, signup_days: {}, best book: {}, worst book {}, books per day: {}".format(
            winner_library.max_value, len(winner_library.scanned_books_list), winner_library.signup_days,
            book_scores_dict[winner_library.scanned_books_list[0]],
            book_scores_dict[winner_library.scanned_books_list[-1]],
            winner_library.ship_books_per_day
        ))
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
        return 0, [], False
    books_not_scanned = library.books_index_set - already_scanned_books_set
    max_books_we_can_scan = days_available * library.ship_books_per_day
    can_wait = False
    if max_books_we_can_scan > len(books_not_scanned) + library.ship_books_per_day:
        can_wait = True

    my_books_dict = dict()
    for book_index in books_not_scanned:
        my_books_dict[book_index] = book_scores_dict[book_index]

    books_added = 0
    library_value = 0
    scanned_books_list = list()
    for k, v in sorted(my_books_dict.items(), key=lambda item: item[1], reverse=True):
        library_value += v
        scanned_books_list.append(k)
        books_added += 1
        if books_added == max_books_we_can_scan:
            break

    return library_value, scanned_books_list, can_wait


def main():
    myargs = parse_args()
    books_count, days, book_scores_dict, libraries = read_input(myargs)
    print('Books: {}, Days: {}'.format(books_count, days))
    # print('Book score dict: {}'.format(book_scores_dict))

    # Task
    if myargs.input.find('b_read_on.txt') != -1 and myargs.avoid_generic_alg == True:
        print("Sample b hack")
        libraries_solved = solve_case_b(books_count, days, book_scores_dict, libraries)
    elif myargs.input.find('c_incunabula.txt') != -1 and myargs.avoid_generic_alg == True:
        print("Sample c hack")
        libraries_solved = solve_case_c(books_count, days, book_scores_dict, libraries)
    elif myargs.input.find('d_tough_choices.txt') != -1 and myargs.avoid_generic_alg == True:
        print("Sample d hack")
        libraries_solved = solve_case_d_alg2(books_count, days, book_scores_dict, libraries)
    elif myargs.input.find('e_so_many_books.txt') != -1 and myargs.avoid_generic_alg == True:
        print("Sample e hack")
        libraries_solved = solve_case_c(books_count, days, book_scores_dict, libraries)
    else:
        print("Generic solution")
        libraries_solved = run_generic_algorithm(books_count, days, book_scores_dict, libraries)
        # run_fake_algorithm(libraries)

    print_output('output.txt', libraries_solved, book_scores_dict)


if __name__ == "__main__":
    main()
