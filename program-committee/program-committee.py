import csv
import sys


def generate_tex(filename):
    output_text = '{\\bf\\large Committees}\\par\n'

    with open(filename, 'r') as f:
        reader = csv.reader(f)
        chair_type = None
        chairs = []

        for row in reader:
            if len(row) != 2:
                print('Error: Expected exactly two values per row.')
                exit(1)
            paren_pos = row[1].find('(')
            person = row[1]
            if paren_pos != -1:
                person = row[1][:paren_pos].strip()
            if not row[0]:
                chairs.append(person)
            else:
                if chair_type is not None:
                    output_text += '\\committeeBlock{%s}{%s}\n' % (chair_type, ' \\\\ '.join(chairs))
                chair_type = row[0].strip().rstrip(':')
                chairs = [person]
        if chair_type is not None:
            output_text += '\\committeeBlock{%s}{%s}\n' % (chair_type, ' \\\\ '.join(chairs))

    with open('program-committee.tex', 'w') as w:
        w.write(output_text)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('You must include the CSV to parse as the second argument.')
        sys.exit(1)

    generate_tex(sys.argv[1])
