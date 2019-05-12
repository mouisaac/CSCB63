class BayesNet:
    """
    This stores the representation of the Bayes Net. It includes
    the following fields:

    - adj : A dictionary that contains the adjacency list for the network.

            For example, if adj['A'] = ['B', 'C'], there is a directed edge
            from A to B, and also one from A to C.


    - deps : A dictionary that stores the other variables that each variable
            is dependent on.

            For example, if deps['B'] = ['A', 'C'], then B is conditionally
            dependent on A and C. In other words, the table at this node 
            contains the conditional probability P(B | A, C).

            If deps['A'] = [], then A is not conditionally dependent on anything
            (It is independent of anything else).


    - probs : This is a dictionary that contains a list of the conditional 
            probabilities for every variable. This is the tricky one - make sure
            you really understand how this is being stored, otherwise your code may
            not be correct. Here's how it works

            If a variable A is independent (deps['A'] = []), then probs['A'] will be
            a list with one element, that contains the probability that A = 1.
            Remember that A is an indicator variable, so the probability of A = 0 can 
            be inferred by P(A=0) = 1 - P(A=1).

            Now, if B is dependent on some other variables A and C, and we have 
            deps['B'] = ['A', 'C'] (The order in this array is important), and we have
            probs['B'] = [0.1, 0.2, 0.7, 0.4], then this means that:


                P(B=1 | A=0, C=0) = 0.1          Note how we are 'binary counting' with 
                P(B=1 | A=0, C=1) = 0.2          A and C - this is the same order you
                P(B=1 | A=1, C=0) = 0.7          used in CSCB36 to write the truth tables.   
                P(B=1 | A=1, C=1) = 0.4          The first entry is where all dependencies
                                                 are 0, and the last is where they are all 1.

            Note that once again, P(B=0 | ... ) can be inferred once again by taking the
            complement of the corresponding probability above, since we are only dealing
            with indicator random variables here.

    Make sure you read the above a few times to make sure you've understood how we're storing
    the network.

    """

    def __init__(self, fname):
        """
        Reads the net from the input file, sets everything up.
        Stores the adjacency matrix, the parents of each node,
        the conditional probability tables, as well as an array
        storing the nodes in topologically sorted order.
        """
        inF = open(fname)
        lines = inF.readlines()
        inF.close()
        adj, deps, probs = {}, {}, {}
        curProb = None
        mode = 0
        for line in lines:
            # Ignore comments
            if "#" in line:
                continue

            # Read in adjacency list
            if mode == 0:
                # Done with adjacency matrix
                if "---" in line:
                    mode += 1
                    continue

                w = [i.rstrip().lstrip() for i in line.split('->')]
                node = w[0]
                edgs = w[1].split(' ')
                for i in edgs:
                    if i not in adj:
                        adj[i] = []
                adj[node] = edgs

            # Read in the probabilities
            if mode == 1:
                # Done with the current variable, reset for next
                if "---" in line:
                    curProb = None

                # Add the parents in order
                elif curProb is None:
                    curProb = [i.rstrip().lstrip() for i in line.split(" ")]
                    if (len(curProb) == 1):
                        deps[curProb[0]] = []
                    else:
                        deps[curProb[0]] = curProb[1:]
                    curProb = curProb[0]
                    probs[curProb] = []
                # Read the probability
                else:
                    probs[curProb] += [float(line)]

        # Set the vars for the instance
        self.adj = adj
        self.deps = deps
        self.probs = probs
