#!/usr/bin/env python3

from itertools import groupby, chain
from operator import attrgetter
from collections import defaultdict
from typing import List
import re

START_END_PATTERN = re.compile('.*[\s|#](?P<start>\d+)-(?P<end>\d+)[\s]?.*')
START_ONLY_PATTERN = re.compile('[^\d]*(?P<start>\d+).*')


class BookNote:
    def __init__(self, book_name='', text='', start=0, end=0):
        self.book_name = book_name
        self.text = text
        self.start = start
        self.end = end

    def __hash__(self):
        return hash(self.book_name + str(self.start) + ' ' + str(self.end))

    def __eq__(self, other: 'BookNote'):
        return self.book_name == other.book_name and \
               self.start == other.start \
               and self.end == other.end \
               and self.text == other.text

    def __str__(self):
        book_name = '<' + self.book_name[0:10]
        book_name += '...>:' if len(self.book_name) > 10 else '>:'
        text = self.text[0:10]
        text += '...' if len(self.text) > 10 else ''
        return book_name + ' ' + text

    def __repr__(self):
        return str(self)

    def __bool__(self):
        return len(self.text) > 0


def book_notes_generator(file):
    BOM = '\ufeff'
    line_separator = '=========='
    SKIP_NUM_INI = 4
    skip_num = SKIP_NUM_INI
    book_name = ''
    text = ''
    start = 0
    end = 0

    def reset_context():
        nonlocal skip_num
        nonlocal book_name
        nonlocal text
        skip_num = SKIP_NUM_INI
        book_name = ''
        text = ''

    for line in file.readlines():
        line = line.strip()
        line = line.replace(BOM, '')

        if line == line_separator:
            yield BookNote(book_name, text, start, end)
            reset_context()
        else:
            skip_num -= 1
            if book_name is '':
                book_name = line
            else:
                if skip_num == 2:
                    line = line.split('|')[0]
                    try:
                        match = START_END_PATTERN.search(line)
                        if match:
                            start = match.group('start')
                            end = match.group('end')
                        else:
                            match = START_ONLY_PATTERN.search(line)
                            if match:
                                start = end = match.group('start')
                        start, end = int(start), int(end)
                    except Exception as e:
                        print(type(e))
                        print("Invalid pos", line)
                        start = end = 0
                if skip_num == 0:
                    text += line


def remove_duplicated_book_notes(book_notes) -> List[BookNote]:
    book_note_lst = list(book_notes)
    book_note_lst.sort(key=lambda __: __.book_name)
    book_note_dct = defaultdict(list)
    for group_key, values in groupby(book_note_lst, key=attrgetter('book_name')):
        book_name = group_key
        book_note_lst_under_book = list(values)
        book_note_lst_under_book.sort(key=lambda x: len(x.text))
        for idx, book_note in enumerate(book_note_lst_under_book):
            if idx < len(book_note_lst_under_book) - 1 and any(map(lambda rest: book_note.text in rest.text,
                                                                   book_note_lst_under_book[idx + 1:])):
                continue
            else:
                book_note_dct[book_name].append(book_note)

    return list(chain.from_iterable(book_note_dct.values()))


def generate_output(book_notes):
    HEADING_1 = '# '
    HEADING_2 = '## '
    LISTING = '- '
    NEWLINE = '\n'
    output = HEADING_1 + 'Kindle Notes' + NEWLINE
    for group_key, values in groupby(book_notes, key=attrgetter('book_name')):
        book_name = group_key
        book_note_lst_under_book = list(sorted(values, key=lambda x: x.start))
        output += f"{NEWLINE}{HEADING_2} {book_name}{NEWLINE}{NEWLINE}"
        for book_note in book_note_lst_under_book:
            output += f"{LISTING} {book_note.text}{NEWLINE}"
        output += NEWLINE
    return output


if __name__ == '__main__':
    file_path = './My Clippings.txt'
    book_notes_lst = list(book_notes_generator(open(file_path, 'r')))
    book_note_set = set(book_notes_lst)
    book_notes = list(filter(lambda __: bool(__), book_note_set))
    book_notes = remove_duplicated_book_notes(book_notes)
    markdown_output = generate_output(book_notes)
    print(markdown_output)
