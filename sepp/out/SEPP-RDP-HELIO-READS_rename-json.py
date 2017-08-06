import ast, re, string, sys
revnamemap = ast.literal_eval("{'LoGkyVuQN0000020_999': '0.999', 'LoGkyVuQN0000160_794': '0.794', 'LoGkyVuQN0000011_000': '1.000', 'LoGkyVuQN0000150_741': '0.741', 'LoGkyVuQN0000110_982': '0.982', 'LoGkyVuQN0000100_862': '0.862', 'LoGkyVuQN0000120_926': '0.926', 'LoGkyVuQN0000140_000': '0.000', 'LoGkyVuQN0000060_867': '0.867', 'LoGkyVuQN0000130_950': '0.950', 'LoGkyVuQN0000030_000': '0.000', 'LoGkyVuQN0000090_986': '0.986', 'LoGkyVuQN0000170_760': '0.760', 'LoGkyVuQN0000051_000': '1.000', 'LoGkyVuQN0000070_000': '0.000', 'LoGkyVuQN0000080_996': '0.996', 'LoGkyVuQN0000180_776': '0.776', 'LoGkyVuQN0000190_778': '0.778', 'LoGkyVuQN0000040_951': '0.951'}")
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