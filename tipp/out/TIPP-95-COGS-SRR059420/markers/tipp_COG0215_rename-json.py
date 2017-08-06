import ast, re, string, sys
revnamemap = ast.literal_eval("{}")
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