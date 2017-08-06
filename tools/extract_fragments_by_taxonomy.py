import argparse
import pandas


def read_fasta(ifil, istext=False):
    """
    Reads a fasta file into a python dictionary.
    Parameters
    ----------
    ifil: string
          file name
    Returns
    -------
    seqs : python dictionary
    """
    seqs = {}

    if istext:
        text = ifil
    else:
        with open(ifil, 'r') as f:
            text = f.read()

    lines = text.split('>')

    for x in text.split('>')[1:]:
        [n, d] = x.split('\n', 1)
        d = d.replace('\n', '').replace(' ', '')

        if n in seqs:
            print("Sequence %s already exists in alignment!" % n)

        seqs[n] = d
    return seqs


def main(args):
    df = pandas.read_csv(args.classification)
    keep = df[df[args.rank] == args.name]

    frgmts = read_fasta(args.fragments)
    if args.reverse_complement is not None:
        revcom = read_fasta(args.reverse_complement)

    with open(args.output, 'w') as f:
        for n in keep[keep["revcom"] == False].sequence.values:
            f.write('>' + n + '\n' + frgmts[n] + '\n')
        if args.reverse_complement is not None:
            for n in keep[keep["revcom"] == True].sequence.values:
                f.write('>' + n + '\n' + revcom[n] + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--classification", type=str, required=True, 
                        help="Restructured classification file")
    
    parser.add_argument("-f", "--fragments", type=str, required=True,
                        help="Reads/fragments")
    parser.add_argument("-r", "--reverse_complement", type=str, required=False,
                        help="Reverse complement of reads/fragments")
    
    parser.add_argument("-x", "--rank", type=str, required=True,
    	                help="Taxonomic rank (e.g., class) for extracting reads")
    parser.add_argument("-n", "--name", type=str, required=True,
    	                help="Name (e.g., Clostridia) of taxonomic rank for extracting reads")
    
    parser.add_argument("-o", "--output", type=str, required=True,
                        help="Fasta file with reads selected by taxonomy")

    args = parser.parse_args()

    main(args)
