Each folder should have the necessary documents and scripts to generate the corresponding .tex file for that section. After generating the file, you should commit your code (and .tex file) and upload the .tex file manually to the shared Overleaf document.

Unless stated otherwise, these scripts use python 3. Install all dependencies with `pip install -r requirements.txt`.

# program-committee

Usage: `python program-committee.py program-committee.csv`

Outputs: `program-committee.tex`

# program-session

Usage: `python program-sessions.py keynotes.csv sessions.csv author-names.csv`

Output: `program-sessions.tex`


# extended-abstracts

Usage: `python extended-abstracts.py abstracts.csv author-names.csv`

Output: `extended-abstracts.tex`
