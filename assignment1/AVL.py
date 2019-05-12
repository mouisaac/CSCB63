from Node import *

#################################################################
#                                                               #
#    Define any helper functions you need in this file only.    #
#    Make sure you take a look at Node.py to get familiar       #
#    with how we are storing the AVL tree, and the functions    #
#    provided. A few test cases are provided in Test.py.        #
#    You can test your code by running                          #
#               python Test.py                                  #
#    in the directory where the files are located.              #
#                                                               #
#    Please use Python 2.7.x. Python 3-specific features        #
#    may not work when being autograded.                        #
#                                                               #
#################################################################


class AVL():
    @staticmethod
    def disjoint(T, V):
        """ (Node, Node) -> Bool
        Return True if T and V are disjoint (have no elements in common),
        and False otherwise.
        """
        # empty lists to store the keys of each tree in order
        list_T = []
        list_V = []
        # get the sorted lists
        AVL.in_order_list(T, list_T)
        AVL.in_order_list(V, list_V)

        # keep "intersecting" whenever the lists are not empty
        while list_T and list_V:
            # get the min of each tree
            min_T = list_T[0]
            min_V = list_V[0]
            # when two keys are the same (two trees are not disjoint)
            if min_T == min_V:
                return False
            # when the min key from V is greater than min key from T
            elif min_T < min_V:
                # delete the smaller key in T
                list_T.pop(0)
            # when the min key from T is greater than min key from V
            else:
                # delete the smaller key in V
                list_V.pop(0)

        # if either tree is empty, the intersection is necessarily empty;
        # if the loop has finished, then no keys present in both trees,
        # i.e. the intersection is again empty. Hence True is returned.
        return True

    @staticmethod
    def in_order_list(T, L):
        """ (Node) -> list
        convert an AVL tree to an sorted list by doing in order traversal
        """
        # proceed only if the root is not None
        if T:
            # recursively traverse the tree in order (left -> root -> right)
            # traverse the left subtree
            if (T.left != None):
                AVL.in_order_list(T.left, L)
            # add the key of the current node when left subtree is empty
            L.append(T.key)
            # traverse the right subtree
            if (T.right != None):
                AVL.in_order_list(T.right, L)
