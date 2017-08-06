import argparse
import numpy
import pandas


def restructure_tipp_classification(infile, ranks, revcom=False):
    df = pandas.read_csv(infile, header=None)
    df.rename(columns={0: "query", 
                       1: "tax_id",
                       2: "tax_name",
                       3: "rank",
                       4: "confidence"},
                       inplace=True)
    df = df[["query", "tax_name", "rank"]]

    cols = ["sequence", "revcom"] + ranks
    rows = []
    for q in numpy.unique(df["query"]):
        row = {}
        row["sequence"] = q

        tq = df[df["query"] == q]
        rk = tq["rank"].values.tolist()
        tx = tq["tax_name"].values.tolist()

        for r in ranks:
            try:
                row[r] = tx[rk.index(r)].replace(' ', '_')
            except ValueError:
                row[r] = "Unclassified"

        row["revcom"] = revcom
        rows.append(row)

    df = pandas.DataFrame(rows, columns=cols)
    return df


def main(infile, revcom, outfile):
    ranks = ["phylum", "class", "order",
             "family", "genus", "species"]

    idf = restructure_tipp_classification(infile, ranks)
    if revcom is not None:
        rdf = restructure_tipp_classification(revcom, ranks, revcom=True)

        iset = set(idf.sequence.values)
        rset = set(rdf.sequence.values)

        # Merge classification results
        # between sequences and their reverse complement!
        for seq in list(iset.union(rset)):
            iclass = idf[idf["sequence"] == seq]
            rclass = rdf[rdf["sequence"] == seq]

            if rclass.shape[0] == 0:
                # Do nothing
                pass
            elif iclass.shape[0] == 0:
                # Add reverse complement classification
                idf = idf.append(rclass)
            else:
                # Use lowest rank classification
                for r1 in ranks:
                    # TO DO: improve indexing into dataframe...
                    if (iclass[r1].values[0] != "Unclassified") and \
                       (rclass[r1].values[0] == "Unclassified"):
                        break
                    elif (iclass[r1].values[0] == "Unclassified") and \
                         (rclass[r1].values[0] != "Unclassified"):
                        idf.loc[idf["sequence"] == seq, "revcom"] = True
                        for r2 in ranks:
                            idf.loc[idf["sequence"] == seq, r2] = rclass[r2].values[0]
                        break

    # Write restructured (and merged) classification data
    idf.to_csv(outfile + ".csv",
               sep=',', na_rep="NA",header=False, index=False)

    # Extract and write read counts
    for r in ranks:
        cols = ["taxonomy", "count"]
        rows = [] 
        for n in set(idf[r].values):
            row = {}
            row["taxonomy"] = n
            row["count"] = idf[idf[r] == n].shape[0]
            rows.append(row)
        xdf = pandas.DataFrame(rows, columns=cols)
        xdf.to_csv(outfile + "_" + r + ".csv",
                   sep=',', na_rep="NA",header=False, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", type=str,
                        required=True, help="TIPP classification file")
    parser.add_argument("-r", "--revcom", type=str, default=None,
                        help="TIPP classification for reverse complement")
    parser.add_argument("-o", "--output", type=str,
                        required=True, help="Prefix of output CSV file")

    args = parser.parse_args()

    main(args.input, args.revcom, args.output)
