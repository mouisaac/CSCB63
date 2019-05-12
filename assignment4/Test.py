import unittest
from BayesNet import BayesNet
from Solution import Solution

#####################################################################
#                                                                   #
#   There will be other test cases when your code is graded.        #
#   Feel free to add your own test cases here, this file will       #
#   not be submitted. These are just for reference. You should      #
#   be testing your code with your own test cases to ensure         #
#   correctness.                                                    #
#                                                                   #
#   Individial tests can be run as follows:                         #
#      python3 Test.py TestNet.test_One      (etc)                  #
#                                                                   #
#####################################################################


class TestNet(unittest.TestCase):

    # The following two test cases are exactly what you've
    # done for the written portion of this assignment.
    def test_One(self):
        net = BayesNet("net1.txt")
        state = {'A': 1, 'B': 0, 'C': 1, 'D': 0}
        p = Solution.getProbability(net, state)
        self.assertAlmostEqual(p, 0.1215)

    def test_Two(self):
        net = BayesNet("net1.txt")
        state = {'A': 1, 'C': 0, 'D': 1}
        p = Solution.getProbability(net, state)
        self.assertAlmostEqual(p, 0.3024)

    # Another Bayes Net, this one has a variable that's conditionally
    # dependent on 2 others. Your implementation should be able to handle
    # any number of dependencies, as long as the Bayes Net is valid.
    def test_Three(self):
        net = BayesNet("net2.txt")
        state = {'C': 1, 'S': 0, 'R': 1, 'W': 1}
        p = Solution.getProbability(net, state)
        self.assertAlmostEqual(p, 0.324)

    def test_Four(self):
        net = BayesNet("net2.txt")
        state = {'C': 0, 'W': 1}
        p = Solution.getProbability(net, state)
        self.assertAlmostEqual(p, 0.2765)

    # Now... write your own test cases! Make sure your code is doing what
    #       it's supposed to be doing!


if __name__ == "__main__":
    unittest.main()
