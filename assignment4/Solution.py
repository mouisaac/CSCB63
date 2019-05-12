#################################################################
#                                                               #
#    Define any helper functions you need in this file only.    #
#    All classes/hepler functions should be inside the class    #
#    Solution, do not include any code outside that scope.      #
#                                                               #
#    You cannot include any additional libraries                #
#    If you need something that Python doesn't                  #
#    have natively - implement it.                              #
#                                                               #
#    Make sure you take a look at BayesNet.py to get familiar   #
#    with how the network is loaded in and stored, you will     #
#    need this to implement your solution properly.             #
#                                                               #
#    A few test cases are provided in Test.py. You can test     #
#    your code by running                                       #
#               python3 Test.py                                 #
#    in the directory where the files are located.              #
#                                                               #
#################################################################


class Solution:

    @staticmethod
    def getProbability(net, state):
        # num of variables
        n = len(state)
        # all variables in state
        var = []
        # value correspond to variables
        val = []
        # move var and value to lists
        for key, value in state.items():
            var.append(key)
            val.append(value)
        # instantiate a stack to store all possible nodes (possibly duplicates)
        S = Solution.Stack()
        # loop through all the nodes given in state
        for v in var:
            # get the dependency list of each node
            deps = net.deps[v]
            # add every node to the stack
            for d in deps:
                S.push(d)
        # copy all the nodes in state
        varall = var.copy()
        # store the nodes that are missing from the state
        miss = []
        # while stack is not empty
        while S.size():
            # get the node
            node = S.pop()
            # only add the ones that are not already in varall (no duplicate)
            if node not in varall:
                miss.append(node)
                varall.append(node)
        # store the sum of all the probabilities (from all the partitions)
        prob = 0
        # number of missing nodes (use to determine the binary table size)
        missnum = len(miss)
        # if not all the nodes present in the state
        if missnum:
            # loop through the size of the binary table (number of rows)
            for i in range(2**missnum):
                # new state copy from state
                new = state.copy()
                # get the binary representation (count from 0)
                binary = bin(i)[2:]
                # fill the missing 0s (extend them to the full length)
                s = ('0' * (missnum-len(binary)))+binary
                # add each missing node to the new state
                for j in range(missnum):
                    # we must get the binary representation from the left
                    new[miss[j]] = int(s[missnum-j-1])
                # add the particular probability (one of the partition)
                prob += Solution.getProbabilityAll(net, new)
            # return the sum
            return prob
        # all the nodes present in the state, calculate base on dependencies
        else:
            return Solution.getProbabilityAll(net, state)

    class Stack:
        '''
        a standard implementation of a stack using list
        implemented in Marcher (assignment3)
        '''
        def __init__(self):
            # faster than list()
            self.stack = []

        def push(self, value):
            # append to the end of the lsit
            self.stack.append(value)

        def pop(self):
            # pop the last item if not empty
            if self.stack:
                return self.stack.pop()
            else:
                return False

        def size(self):
            # actually don't need but whatever
            return len(self.stack)

    @staticmethod
    def getProbabilityAll(net, state):
        '''
        Assume state contain all the nodes in the "dependent" graph
        '''
        # num of variables
        n = len(state)
        # all variables in state
        var = []
        # value correspond to each variable
        val = []
        # probablity of each variable (with condition)
        prob = [1]*n
        # move variables and values to lists
        for key, value in state.items():
            var.append(key)
            val.append(value)

        # attempt to calculate probability one by one
        for i in range(n):
            # get variable
            v = var[i]
            # get dependent list
            deps = net.deps[v]
            # get the status from state
            status = val[i]
            # no dependency
            if not deps:
                # directly get from probs if 1
                if status:
                    prob[i] = net.probs[v][0]
                # complement = 1 - original
                else:
                    prob[i] = 1-net.probs[v][0]
            else:
                # store dependencies
                dep = []
                # power of 2 used to calculate the index where in probs
                power = -1
                # add all dependencies that are in state
                for x in deps:
                    if x in state:
                        dep.append(x)
                        # increment power for every node
                        power += 1
                # index in probs
                index = 0
                # dep not empty (directly dependent; should always be the case)
                if dep:
                    # go through from left to right (power from highest to 0)
                    for j in range(power+1):
                        if state[dep[j]]:
                            index += 2**(power-j)
                    # set the probability of this node
                    if status:
                        prob[i] = net.probs[v][int(index)]
                    else:
                        prob[i] = 1-net.probs[v][int(index)]

        # probability for the final result
        probability = 1
        # multiply all the probabilities
        for p in prob:
            probability *= p
        return probability
