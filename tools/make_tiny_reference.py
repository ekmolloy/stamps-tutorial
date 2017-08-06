import dendropy
import numpy
import os
import pandas
from shutil import copyfile


def keep_seqs(seqs, nams):
    """
    Removes all other sequences besides names from an alignment object.
    Parameters
    ----------
    seqs : python dictionary
    nams : list of strings
           subset of sequences to keep
    """
    assert(type(nams) is list), "Input names must be in a list!"

    nams = list(set(seqs.keys()) - set(nams))
    for n in nams:
        try:
            del seqs[n]
        except KeyError:
            warn("Sequence %s does not exist!" % n)


def mask_gaps(seqs, thresh=1.0):
    """
    Removes columns in an alignment when a certain fraction
    of sites are gaps. Default is 100% gaps or 1.
    Parameters
    ----------
    seqs : python dictionary
    Returns
    -------
    algn : python dictionary
    """
    import numpy
    from numpy.core.defchararray import startswith

    nams = seqs.keys()
    nseq = len(nams)

    data = []
    for n in nams:
        data.append(list(seqs[n]))
    data = numpy.array(data)

    perc = numpy.sum(startswith(data, '-'), axis=0) / float(nseq)
    cols = numpy.where(perc < thresh)[0]
    data = data[:, cols]

    algn = {}
    for i, n in enumerate(nams):
        algn[n] = ''.join(list(data[i, :]))

    return algn


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


def write_fasta(seqs, ofil):
    """
    Writes sequence data to file with format fasta.
    Parameters
    ----------
    seqs : python dictonary
    ofil : string
           file name
    """
    with open(ofil, 'w') as f:
        for n in seqs.keys():
            f.write('>' + n + '\n' + seqs[n] + '\n')
    return


def main(rank, name):
    indir = "../refpkgs/RDP_2016_Bacteria.refpkg/"
    outdir = "../refpkgs/RDP_2016_" + name + ".refpkg/"

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    # Find sequences to keep
    df = pandas.read_csv(indir + "taxonomy.csv")
    xdf = df[df[rank] == name]

    # Handle duplicate species names!
    seen = {}
    for row in xdf.iterrows():
        n = row[1].species
        try:
            x = seen[n] + 1         
        except KeyError:
            x = 1
        seen[row[1].species] = x

        xdf.set_value(row[0], 'species', n + "_" + str(x))

    keep = list(xdf.sequence.values)

    nmap = {}
    for s, x in zip(keep, xdf.species.values):
        nmap[s] = x

    # Extract sequences from alignment
    if not os.path.exists(outdir + "pasta.fasta"):
        algn = read_fasta(indir + "pasta.fasta")
        keep_seqs(algn, keep)
        algn = mask_gaps(algn)
        write_fasta(algn, outdir + "pasta.fasta")

    # Rename sequences
    if not os.path.exists(outdir + "pasta_labeled.fasta"):
        newa = {}
        for n in algn.keys():
            newa[nmap[n]] = algn[n]
        write_fasta(newa, outdir + "pasta_labeled.fasta")

    # Extract sequences from the tree
    if not os.path.exists(outdir + "RAxML_info.tree"):
        copyfile(indir + "RAxML_info.tree",
                 outdir + "RAxML_info.tree")

    if not os.path.exists(outdir + "pasta.tree"):
        tree = dendropy.Tree.get(path=indir + "pasta.tree",
                                 schema='newick')
        tree.retain_taxa_with_labels(keep)
        with open(outdir + "pasta.tree", 'w') as f:
            f.write(tree.as_string(schema="newick"))

        for n in tree.leaf_nodes():
            s = n.taxon.label 
            n.taxon.label = nmap[s]

        with open(outdir + "pasta_labeled.tree", 'w') as f:
            f.write(tree.as_string(schema="newick"))

    # Extract sequences from the refined taxonomy
    if not os.path.exists(outdir + "RAxML_info.taxonomy"):
        copyfile(indir + "RAxML_info.taxonomy",
                 outdir + "RAxML_info.taxonomy")
    
    if not os.path.exists(outdir + "pasta.taxonomy"):
        tree = dendropy.Tree.get(path=indir + "pasta.taxonomy",
                                 schema='newick')
        tree.retain_taxa_with_labels(keep)
        with open(outdir + "pasta.taxonomy", 'w') as f:
            f.write(tree.as_string(schema="newick"))

        for n in tree.leaf_nodes():
            s = n.taxon.label 
            n.taxon.label = nmap[s]

        with open(outdir + "pasta_labeled.taxonomy", 'w') as f:
            f.write(tree.as_string(schema="newick"))

    # Extract sequences from the species.mapping
    if not os.path.exists(outdir + "species.mapping"):
        cols = ["sequence", "tax_id"]
        rows = []
        for k in keep:
            row = {}
            row["sequence"] = k
            row["tax_id"] = df[df["sequence"] == k].tax_id.values[0]
            rows.append(row)
        xdf = pandas.DataFrame(rows, columns=cols)
        xdf.to_csv(outdir + "species.mapping",
                   sep=',', na_rep="NA",head=False, index=False)

    # Extract sequences from the taxonomy.table
    if not os.path.exists(outdir + "taxonomy.table"):
        copyfile(indir + "taxonomy.table",
                 outdir + "taxonomy.table")


if __name__ == "__main__":
    # Make tiny datasets to classify and visualize Fastidiosipila sanguinis
    main("class", "Clostridia")         # 707 sequences
    main("family", "Ruminococcaceae")   #  55 sequences -- visualize
    main("family", "Heliobacteriaceae") #  21 sequences -- visualize

    # Make tiny datasets to classify and visualize Campylobacter hominis
    main("class", "Epsilonproteobacteria")  # 117 sequences
    main("family", "Campylobacteraceae")    #  56 sequences -- visualize
