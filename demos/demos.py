import csv
import html
import jinja2
import os
import sys

from collections import defaultdict
from pylatexenc.latexencode import utf8tolatex


def _s(s):
    return utf8tolatex(html.unescape(s))


def get_authors(author_names):
    authors = defaultdict(str)
    with open(author_names, 'r') as author_file:
        a_reader = csv.reader(author_file)
        for row in a_reader:
            key = row[0]
            row = row[5:]
            author_parts = []
            while len(row) > 3:
                if row[0] == '' or row[2] == '':
                    break
                if row[1] == '':
                    author_parts.append(_s('%s %s' % (row[0], row[2])))
                else:
                    author_parts.append(_s('%s %s %s' % (row[0], row[1], row[2])))
                row = row[4:]
            authors[key] = ', '.join(author_parts)

    return authors


def demos_from_files(abstracts, authors):
    sessions = defaultdict(list)
    with open(abstracts, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            key = row[1]
            session_key = row[0]
            if session_key == '':
                continue
            sessions[session_key].append({
                'title': _s(row[2]),
                'authors': authors[key],
            })

    return sessions


# Formatting borrowed from http://eosrei.net/articles/2015/11/latex-templates-python-and-jinja2-generate-pdfs
def generate_tex(demos):
    latex_jinja_env = jinja2.Environment(
        block_start_string = '\\BLOCK{',
        block_end_string = '}',
        variable_start_string = '\\val{',
        variable_end_string = '}',
        comment_start_string = '\\#{',
        comment_end_string = '}',
        line_statement_prefix = '\tag',
        line_comment_prefix = '%#',
        trim_blocks = True,
        autoescape = False,
        loader = jinja2.FileSystemLoader(os.path.abspath('.'))
    )
    template = latex_jinja_env.get_template('demos.tex.tmpl')
    with open('demos.tex', 'w') as f:
        f.write(template.render(demos=demos))


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('You must include the demo and author data CSVs as the arguments to this function.')
        sys.exit(1)

    authors = get_authors(sys.argv[2])
    generate_tex(demos_from_files(sys.argv[1], authors))
