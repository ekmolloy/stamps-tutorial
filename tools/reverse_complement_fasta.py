import argparse
from Bio.Alphabet import generic_dna
from Bio.Seq import Seq

def reverse_complement_fasta(ifas, ofas):
    with open(ifas, 'r') as f:
        lines = [l.rstrip('\n') for l in f]
        nlines = len(lines)

    with open(ofas, 'w') as f:
        i = 0
        while i < nlines:
            if lines[i][0] == '>':
                f.write(lines[i] + '\n')
                i = i + 1
            else:
                j = i
                x = ''
                while j < nlines and lines[j][0] != '>':
                    x = x + lines[j]
                    j = j + 1
                seq = Seq(x, generic_dna)
                f.write(str(seq.reverse_complement()) + '\n')
                i = j

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", type=str,
                        required=True, help='Input fasta file')
    parser.add_argument("-o", "--output", type=str,
                        required=True, help="Output fasta file")

    args = parser.parse_args()
    reverse_complement_fasta(args.input, args.output)
