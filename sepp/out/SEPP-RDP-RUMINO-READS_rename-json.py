import ast, re, string, sys
revnamemap = ast.literal_eval("{'LoGkyVuQN0000440_967': '0.967', 'LoGkyVuQN0000180_999': '0.999', 'LoGkyVuQN0000421_000': '1.000', 'LoGkyVuQN0000160_000': '0.000', 'LoGkyVuQN0000501_000': '1.000', 'LoGkyVuQN0000140_845': '0.845', 'LoGkyVuQN0000260_936': '0.936', 'LoGkyVuQN0000280_801': '0.801', 'LoGkyVuQN0000080_930': '0.930', 'LoGkyVuQN0000361_000': '1.000', 'LoGkyVuQN0000370_000': '0.000', 'LoGkyVuQN0000390_698': '0.698', 'LoGkyVuQN0000470_336': '0.336', 'LoGkyVuQN0000320_000': '0.000', 'LoGkyVuQN0000310_969': '0.969', 'LoGkyVuQN0000520_995': '0.995', 'LoGkyVuQN0000031_000': '1.000', 'LoGkyVuQN0000450_940': '0.940', 'LoGkyVuQN0000060_000': '0.000', 'LoGkyVuQN0000410_746': '0.746', 'LoGkyVuQN0000510_993': '0.993', 'LoGkyVuQN0000200_581': '0.581', 'LoGkyVuQN0000210_174': '0.174', 'LoGkyVuQN0000460_885': '0.885', 'LoGkyVuQN0000231_000': '1.000', 'LoGkyVuQN0000340_851': '0.851', 'LoGkyVuQN0000090_866': '0.866', 'LoGkyVuQN0000170_989': '0.989', 'LoGkyVuQN0000040_998': '0.998', 'LoGkyVuQN0000380_916': '0.916', 'LoGkyVuQN0000150_938': '0.938', 'LoGkyVuQN0000400_999': '0.999', 'LoGkyVuQN0000251_000': '1.000', 'LoGkyVuQN0000481_000': '1.000', 'LoGkyVuQN0000010_000': '0.000', 'LoGkyVuQN0000020_902': '0.902', 'LoGkyVuQN0000490_999': '0.999', 'LoGkyVuQN0000330_976': '0.976', 'LoGkyVuQN0000050_925': '0.925', 'LoGkyVuQN0000300_988': '0.988', 'LoGkyVuQN0000110_855': '0.855', 'LoGkyVuQN0000221_000': '1.000', 'LoGkyVuQN0000120_993': '0.993', 'LoGkyVuQN0000130_000': '0.000', 'LoGkyVuQN0000270_695': '0.695', 'LoGkyVuQN0000350_979': '0.979', 'LoGkyVuQN0000430_957': '0.957', 'LoGkyVuQN0000190_997': '0.997', 'LoGkyVuQN0000290_957': '0.957', 'LoGkyVuQN0000070_149': '0.149', 'LoGkyVuQN0000100_485': '0.485', 'LoGkyVuQN0000241_000': '1.000'}")
def relabel_newick(newick_string):
    pattern = re.compile("(LoGkyVuQN[^(,:)<>]+)")
    invalidChars = set(string.punctuation).union(set(string.whitespace))
    def replace_func(m):
        repl = m.group(1)
        if m.group(1) in revnamemap:
            repl = revnamemap[m.group(1)]
            if any(char in invalidChars for char in repl):
                repl = "'%s'" %repl
        else:
            repl = m.group(1)
        
        return repl 
    t = pattern.sub(replace_func,newick_string)
    return t
for l in sys.stdin.readlines():
        sys.stdout.write(relabel_newick(l))