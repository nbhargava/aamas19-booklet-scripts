import csv
import html
import jinja2
import os
import sys

from collections import defaultdict
from pylatexenc.latexencode import utf8tolatex


def _s(s):
    return utf8tolatex(html.unescape(s))


def keynotes_from_file(filename):
    keynotes = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            keynotes.append({
                'title': _s(row[1]),
                'presenter': _s('%s %s' % (row[2], row[4])),
            })

    return keynotes


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


def sessions_from_files(program_sessions, authors):
    sessions = defaultdict(list)
    with open(program_sessions, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            key = row[1]
            session_key = row[3][:2]
            sessions[session_key].append({
                'title': _s(row[2]),
                'authors': authors[key]
            })

    return sessions


# Formatting borrowed from http://eosrei.net/articles/2015/11/latex-templates-python-and-jinja2-generate-pdfs
def generate_tex(keynotes, sessions):
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
    template = latex_jinja_env.get_template('program-sessions.tex.tmpl')
    session_metadata = {
        '1A': {
            'title': 'Reinforcement Leaning 1',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '1B': {
            'title': 'Socially Intelligent Agents 1',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '1C': {
            'title': 'Multi-Robot Systems',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '1D': {
            'title': 'Verification and Validation',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '1E': {
            'title': 'Economic Paradigms: Learning and Adaptation',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '1F': {
            'title': 'Agent Societies and Societal Issues 1',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '2A': {
            'title': 'Reinforcement Leaning 2',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '2B': {
            'title': 'Practical Applications of Game Theory',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '2C': {
            'title': 'Knowledge Representation and Reasoning',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '2D': {
            'title': 'Social Choice Theory 1',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '2E': {
            'title': 'Game Theory 1',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '2F': {
            'title': 'Agent Societies and Societal Issues 2',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '3A': {
            'title': 'Learning and Adaptation',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '3B': {
            'title': 'Socially Intelligent Agents 2',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '3C': {
            'title': 'Engineering Multiagent Systems 1',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '3D': {
            'title': 'Social Choice Theory 2',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '3E': {
            'title': 'Game Theory 2',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '3F': {
            'title': 'Logics for Agents',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '4A': {
            'title': 'Learning Agent Capabilities',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '4B': {
            'title': 'Multimodal Interaction',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '4C': {
            'title': 'Deep Learning',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '4D': {
            'title': 'Robotics',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '4E': {
            'title': 'Game Theory 3',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '4F': {
            'title': 'Communication and Argumentation 1',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '5A': {
            'title': 'Learning Agents',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '5B': {
            'title': 'Human-Robot interaction',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '5C': {
            'title': 'Industrial Applications Track',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '5D': {
            'title': 'Social Choice Theory 3',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '5E': {
            'title': 'Auctions and Mechanism Design',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '5F': {
            'title': 'Agent Cooperation 1',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '5G': {
            'title': 'Networks',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '6A': {
            'title': 'Agent-Based Simulation',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '6B': {
            'title': 'Auctions and Mechanism Design',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '6C': {
            'title': 'Engineering Multiagent Systems 2',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '6D': {
            'title': 'Blue Sky',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '6E': {
            'title': 'Agent Cooperation 2',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '6F': {
            'title': 'Communication and Argumentation 2',
            'room': 'TBD',
            'chair': 'TBD',
        },
        '6G': {
            'title': _s('Planning & Learning'),
            'room': 'TBD',
            'chair': 'TBD',
        },
    }
    with open('program-sessions.tex', 'w') as f:
        f.write(template.render(keynotes=keynotes, sessions=sessions, metadata=session_metadata))


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('You must include the keynote, session, and author data CSVs as the arguments to this function.')
        sys.exit(1)

    authors = get_authors(sys.argv[3])
    generate_tex(keynotes_from_file(sys.argv[1]),
                 sessions_from_files(sys.argv[2], authors))
