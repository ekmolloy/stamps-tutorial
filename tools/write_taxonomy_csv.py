import numpy
import pandas

if __name__ == "__main__":
    ranks = ["superkingdom", "phylum", "class",
             "order", "family", "genus", "species"]

    # Read taxonomy file
    df = pandas.read_csv("rdp_bacteria_2016.refpkg/taxonomy.table")

    # Read species name map files
    nmp = pandas.read_csv("rdp_bacteria_2016.refpkg/species.mapping")

    # Get rank information for each species
    cols = ["sequence", "tax_id"] + ranks
    rows = []
    for s, x in zip(nmp.seqname.values, nmp.tax_id.values):
        data = df[df["tax_id"] == x]

        dic = {}
        dic["sequence"] = s
        dic["tax_id"] = x

        for r in ranks:
            xid = data[r].values[0]
            x = df[df["tax_id"] == xid].tax_name.values
            if x.size == 0:
                x = "NA"
            else:
                x = x[0].replace(' ', '_').replace('[', '').replace(']', '')
            dic[r] = x

        rows.append(dic)
    df = pandas.DataFrame(rows, columns=cols)
    df.to_csv("rdp_bacteria_2016.refpkg/taxonomy.csv",
              sep=',', na_rep="NA",head=False, index=False)
