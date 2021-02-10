# Description 

Input
The program will take as input a specification of a puzzle and a starting state and will
generate as output a set of clauses to be satisfied.
The format of the input contains the following elements:
1. First line: The number of holes and the hole that is empty at time 1.
2. Remaining lines: The encoding of the puzzle as a set of triples. Each line is a triple of
three numbers, for holes that lie in a row.
Note: The puzzle does not have to be geometrically feasible. The only requirement is
that jumps are symmetric; if the input contains a line I,J,K then it is possible, both to jump
from I to K over J and from K to I over J.


## How to excute?


```bash
python Puzzle.py
```

## Usage

```python
	To read data from input.txt
	write data to output.txt, propositions.txt
```

