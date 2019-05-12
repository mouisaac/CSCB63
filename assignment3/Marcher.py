#################################################################
#                                                               #
#    Define any helper functions you need in this file only.    #
#    All classes/hepler functions should be subclass of         #
#    Marcher, do not include any code outside that scope.       #
#                                                               #
#    You cannot include any additional libraries                #
#    If you need something that Python doesn't                  #
#    have natively - implement it.                              #
#                                                               #
#    Make sure you take a look at Map.py to get familiar        #
#    with how the image is loaded in and stored, you will       #
#    need this to implement your solution properly.             #
#                                                               #
#    A few test cases are provided in Test.py. You can test     #
#    your code by running                                       #
#               python3 Test.py                                 #
#    in the directory where the files are located.              #
#                                                               #
#################################################################


class Marcher:

    @staticmethod
    def findPath(mp, weight):
        """
        Input:
            mp - This is a Map object representing the image you are working on. Look at the Map
                class to see details on how we are representing the data.

            weight - This is the weight **function**. You are supposed to use this to find the energy
                required for each step by the Pixel Marcher. This function should be called like this:

                      weight(mp, (x,y), (a, b))

                to find the energy needed to step from pixel (x,y) to pixel (a,b). Note that
                this function may return a value for *any* pair of pixels, and it is your job
                to only be consider valid steps (More on this below). In general this returns a float.

                The return value of this function will always be non-negative, and it is not necessarily
                the case that weight(mp, a, b) = weight(mp, b, a).

        Requirements:
            Your objective is to find the least-energy path from pixel (0,0) to pixel(sx-1, sy-1), along
            with the amount of energy required to traverse this path. Here, sx and sy are the x and y
            dimensions of the image. (These are stored in 'mp')

            From each pixel, it is possible to step to at most 4 other pixels, namely the ones on it's top,
            right, bottom and left. All of these steps may require different amounts of energy, and you have
            to use the given weight function to compute these.

            Note: When going through your neighbours, always go through them in the following order for the sake
                of this assignment: TOP, RIGHT, BOTTOM, LEFT (Start at the top and go clockwise).


                                                        (x, y-1)
                                                            ^
                                                            |
                                        (x-1, y) <------ (x, y) ------> (x+1, y)
                                                            |
                                                            v
                                                        (x, y+1)


            Always doing it in this order will ensure consistency if there are multiple least-energy paths.

            Once you find this path, you need to store all the nodes along it in mp.path[], ensuring that
            the (0,0) is the first element in the array, (sx-1, sy-1) is the last, and all the remaining
            elements are in order.

            Your function additionally needs to return the total energy required for the least-energy path
            you have found. You will be graded on this since the cost a least-energy path is unique and must
            match the expected answer.

        You are NOT allowed to import any additional libraries. All code must be your own.

        """
        goal = mp.sx * mp.sy
        # path finding using (modified) dijkstra's algorithm
        (dist, parent) = Marcher.dijkstra(mp, weight, 1, goal)
        # add the starting point (top left pixel)
        mp.path.append((0, 0))
        # get the path in between
        Marcher.get_path(mp, parent, goal)
        # add the ending point (bottom right pixel)
        mp.path.append((mp.sx - 1, mp.sy - 1))
        # returning distance to the last node (from upper left to bottom right)
        return dist[-1]

    @staticmethod
    def all_colour_weight(mp, a, b):
        """
        Input:
            mp : a Map object that represents the image
            a, b : There are both 2-tuples, containing the (x,y) coordinates for the two pixels between
                    which you want to find the energy for a step.


        Requirements:

            Define your own weight function here so that when "25colours.ppm" is run with this function,
            the least-energy path in the image satisfies the following constraints:

                (1) The least energy path must visit every one of the 25 colours in the graph. The order
                    in which the path visits these colours does *not* matter, as long as it visits them all.
                    Be careful - missing even one colour will result in 0 for this function.

                (2) The path can stay on one colour for as many steps as necessary, however once the path
                    leaves a colour, it can NEVER go through another pixel of the same colour again.
                    (Said in another way, it can only enter/exit each coloured box once)

                (3) For any two given pixels, the energy required to step between them *must* be non-negative.
                    If you have negative energies, this function may not work as intended.

            There is no restriction on path length, it can be as long or as short as needed - as long as it
            satisfies the conditions above. Also, the amount of energy to step from 'a' to 'b' does not have to be
            the same as the energy to step from 'b' to 'a'. This is up to you.

        Important Note: This weight function will NOT be tested with your solution to the first part of the
                        question. This will be passed into my code and should still produce the results as above,
                        so do not try to change your findPath() method to help with this.

                        This function will be tested ONLY on the specified image, so you do not have to worry
                        about generalizing it. Just make sure that it does not depend on anything else in your
                        code other than the arguments passed in.


        How to test:    Use the 'outputGradient' and 'outputPath' methods in Map to help you debug. Displaying
                        the path will be useful to start, as it will give you a general idea of what the least-
                        energy path looks like, but you will also want to display the gradient to make sure that
                        there are no colours repeated! (This should be obvious visually if it is the case)

        """
        # weight function designed for 25colours.ppm
        return Marcher.weight_function_25(a, b)


    '''
    a standard, boring implementation of a stack using list
    '''
    class Stack:
        def __init__(self):
            # faster than list()
            self.stack = []

        def push(self, value):
            # append to the end of the lsit
            self.stack.append(value)

        def peek(self):
            # item (last in) is at the end
            return self.stack[-1]

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
    def get_path(mp, parent, i):
        # get the "parent" of i (p will be the number representing the parent)
        p = parent[i]
        # a stack for "reverse traversal"
        stack = Marcher.Stack()
        # keep adding the path node until reaching the starting point
        while (p != -1):
            # push parent
            stack.push(p)
            # update p (traverse to the parent node)
            p = parent[p]

        # pop the first "parent" (c for current)
        c = stack.pop()
        # adding the coordinates of each node on the path in the right order
        while c:
            y = (c-1)//mp.sx
            x = (c-mp.sx*y)-1
            mp.path.append((x, y))
            # get the next node
            c = stack.pop()

    @staticmethod
    def dijkstra(mp, weight, start=1, end=None):
        '''
        Dijkstra's algorithm
        '''
        # number of nodes + 1
        n = mp.sx * mp.sy + 1
        # list to store the status of each node (visited or not)
        visited = [False]*n
        # list to store the shotest distance (from the starting point)
        distance = [float('inf')]*n
        # list to store the "parent" of each node (i.e. previous node on path)
        parent = [None]*n
        # list to store the pointer to each node
        heapNodes = [None]*n
        # priority queue using fibonacci heap
        pq = Marcher.FibonacciHeap()
        # insert the starting point with distance 0 (equiv: highest priority)
        heapNodes[1] = pq.insert(0, 1)

        '''
        # insert all the nodes at the beginning (will make extraction slow)
        for i in range(2, n):
            heapNodes[i] = pq.insert(float('inf'), i)
        '''
        # set the parent of the starting point to be a "non-existing point"
        parent[start] = -1
        # set the require distance to reach starting point to be 0
        distance[start] = 0

        # loop through the grid until end node (or all nodes) has been visited
        while pq.num:
            current = pq.extract_min().value
            visited[current] = True

            # stop as soon as we "reach" the ending point (when it is visited)
            if current == end:
                break
            # get the adjacent nodes (all four neighbors)
            adj = Marcher.get_adj(mp, weight, current)
            # check each neighbors
            for (neighbor, cost) in adj:
                # only consider unvisited ones
                if not visited[neighbor]:
                    # get the distance of reaching current node
                    d = distance[current]
                    # new distance
                    new = d + cost
                    # update parent and distance if new distance is shorter
                    if new < distance[neighbor]:
                        parent[neighbor] = current
                        distance[neighbor] = new
                        # insert the new neighbor if it has not been seen
                        if heapNodes[neighbor] is None:
                            # (put in priority queue for later visit)
                            heapNodes[neighbor] = pq.insert(new, neighbor)
                        # otherwise just update its priority to new distance
                        else:
                            pq.decrease_key(heapNodes[neighbor],
                                            distance[neighbor])

        return (distance, parent)

    @staticmethod
    def get_adj(mp, weight, i):
        # list to store adjacent nodes
        adj = []
        # number of row
        row = mp.sx
        # coordinates of current node
        y = (i-1)//row
        x = (i-row*y)-1
        # list to store neighbors
        neighbors = []
        # store neighbor coordinates and the index base on the current index i
        neighbors.append((x, y-1, i-row))  # up
        neighbors.append((x+1, y, i+1))  # right
        neighbors.append((x, y+1, i+row))  # bottom
        neighbors.append((x-1, y, i-1))  # left

        for neighbor in neighbors:
            # coordinates of the neighbor
            cur_x = neighbor[0]
            cur_y = neighbor[1]
            # check if the position is valid (inside the image)
            if (cur_x >= 0) and (cur_x <= (mp.sx - 1)):
                if (cur_y >= 0) and (cur_y <= (mp.sy - 1)):
                    cost = weight(mp, (x, y), (cur_x, cur_y))
                    # add valid node to the list
                    adj.append((neighbor[2], cost))
        return adj

    '''
    Implement Fibonacci Heap by linking roots of all trees as well as chidren
    with circular doubly linked lists. Only methods that are required for
    Dijkstra's Algorithm are implemented.
    '''
    class FibonacciHeap:

        '''
        (internal) node class that stores key (priority) and value (number)
        '''
        class Node:
            def __init__(self, key, value):
                self.key = key
                self.value = value
                self.parent = None
                self.child = None
                self.left = None
                self.right = None
                self.degree = 0
                self.mark = False

        # the list of roots (just point to one root in the linked list)
        root_list = None
        # the minimum node
        min_node = None
        # number of nodes
        num = 0

        def iterate(self, node=None):
            '''
            use to iterate through the node list
            '''
            # get the first node (min) in the heap if node is not given
            if node is None:
                node = self.root_list
            current = node
            # iterates through the node list whenever it is being called
            while True:
                # return the current node
                yield current
                # continue if current is a node
                if current is None:
                    break
                # shift to the next node
                current = current.right
                # continue only if next node is different from the current node
                if current == node:
                    break

        def insert(self, key, value):
            '''
            insert a key and a value associated with it
            '''
            # node store the key and the value
            node = self.Node(key, value)
            # "circular" (pointer)
            node.left = node.right = node
            # add the node to root list
            self.add_to_root_list(node)
            # update the min node
            if self.min_node is not None:
                if self.min_node.key > node.key:
                    self.min_node = node
            else:
                self.min_node = node
            # increment the "size"
            self.num += 1
            # return the node for future reference
            return node

        def get_min(self):
            '''
            get the minimum node without removing it (debug purpose)
            '''
            return self.min_node

        def extract_min(self):
            '''
            extract the min node (its children become roots) assuming it exists
            '''
            node = self.min_node
            if node.child is not None:
                # get its children
                children = [x for x in self.iterate(node.child)]
                # promote them to the root_list
                for child in children:
                    self.add_to_root_list(child)
                    child.parent = None

            # delete min node
            self.remove_from_root_list(node)
            # decrement the size
            self.num -= 1
            # consolidate so each root has unique rank
            self.consolidate()
            # update the min node
            if node == node.right:
                self.min_node = None
                self.root_list = None
            else:
                self.min_node = self.find_min()
            return node

        def find_min(self):
            '''
            find the minimum node by iterating through the node list
            '''
            # no min
            if self.root_list is None:
                return None
            else:
                min_node = self.root_list
                for node in self.iterate(self.root_list):
                    # update min node when we found a node with higher priority
                    if node.key < min_node.key:
                        min_node = node

                return min_node

        def decrease_key(self, node, key):
            '''
            increase the priority of node to v assuming v is relatively smaller
            '''
            # if v >= node.key
            # set new priority
            node.key = key
            parent = node.parent
            # check if node is in root list and if we need to cut its parent(s)
            if parent is not None and key < parent.key:
                self.cut(node, parent)
                self.cascading_cut(parent)
            # update min node if necessary
            if self.min_node is not None and key < self.min_node.key:
                self.min_node = node

        def cut(self, node, parent):
            '''
            cut the current node and put it on the root list
            '''
            # remove the node from the child list (of its parent)
            self.remove_from_child_list(parent, node)
            parent.degree -= 1
            # make it a root and add it to the root list
            self.add_to_root_list(node)
            node.parent = None
            node.mark = False
            # update min node if necessary
            if self.min_node is not None and node.key < self.min_node.key:
                self.min_node = node

        def remove_from_child_list(self, parent, node):
            '''
            remove the node from the child list
            '''
            # remove the whole child list if there is only one node
            if parent.child == parent.child.right:
                parent.child = None
            # shift the pointer
            elif parent.child == node:
                parent.child = node.right
                node.right.parent = parent
            # re-wire the pointers
            node.left.right = node.right
            node.right.left = node.left

        def add_to_root_list(self, node):
            '''
            add the node to root list
            '''
            # set the only node as the pointer to root list
            if self.root_list is None:
                self.root_list = node
            else:
                # re-wire the pointers
                node.right = self.root_list.right
                node.left = self.root_list
                self.root_list.right.left = node
                self.root_list.right = node

        def remove_from_root_list(self, node):
            '''
            remove the node from the root list
            '''
            # remove the whole list if there is only one node
            if self.root_list == node:
                if self.root_list == self.root_list.right:
                    self.root_list = None
                    return
                else:
                    # shift the pointer
                    self.root_list = node.right
            # re-wire the pointers
            node.left.right = node.right
            node.right.left = node.left

        def cascading_cut(self, node):
            '''
            recursively cut the node until reaching an unmark node or a root
            '''
            parent = node.parent
            # if node is not a root
            if parent is not None:
                # mark the parent (or if already marked, cut it as well)
                if parent.mark is False:
                    parent.mark = True
                else:
                    # cut the parent and start over (the cut process) on it
                    self.cut(node, parent)
                    self.cascading_cut(parent)

        def consolidate(self):
            '''
            consolidates the trees so each tree has a unique degree
            '''
            # check if the heap is empty
            if self.root_list is None:
                return
            # list to store unique degrees
            degrees = [None]*self.num
            # get all the roots
            nodes = [x for x in self.iterate(self.root_list)]
            # walk through the root list
            for node in nodes:
                d = node.degree
                # keep "eliminating" trees with same degree by "merge"
                while degrees[d] is not None:
                    # current tree (in the degree list) with degree d
                    current = degrees[d]
                    # let current tree to be the one with higher priority
                    if node.key > current.key:
                        node, current = current, node
                    # merge the two trees (essentailly merging two nodes)
                    self.merge(node, current)
                    # now we have a tree with degree d + 1
                    degrees[d] = None
                    d += 1
                # pointer to the first tree with degree d
                degrees[d] = node

        def merge(self, node1, node2):
            '''
            merge two nodes by setting the node with lower priority as child
            (assume node2 has lower priority)
            '''
            self.remove_from_root_list(node2)
            # circular list of one node
            node2.left = node2.right = node2
            # get the children list
            children = node1.child
            # set other node to be the pointer to its children if it had none
            if children is None:
                node1.child = node2
            else:
                # re-wiring the pointers
                node2.right = children.right
                node2.left = children
                children.right.left = node2
                children.right = node2

            # update info
            node2.parent = node1
            node1.degree += 1
            node2.mark = False

    @staticmethod
    def weight_function_25(a, b):
        '''
        A weight function designed specifically for 25colours.ppm.

        hard-coded a shortest path which goes through each color exactly once:
        (when going left or right, turn as soon as we hit the boundary;
        when going down, turn as soon as we step on a new color) right -> down
        -> left -> down -> right -> down -> left -> down -> right -> down
        '''
        if (( a ==(0, 0) and b ==(1, 0)) or
        ( a ==(1, 0) and b ==(2, 0)) or
        ( a ==(2, 0) and b ==(3, 0)) or
        ( a ==(3, 0) and b ==(4, 0)) or
        ( a ==(4, 0) and b ==(5, 0)) or
        ( a ==(5, 0) and b ==(6, 0)) or
        ( a ==(6, 0) and b ==(7, 0)) or
        ( a ==(7, 0) and b ==(8, 0)) or
        ( a ==(8, 0) and b ==(9, 0)) or
        ( a ==(9, 0) and b ==(10, 0)) or
        ( a ==(10, 0) and b ==(11, 0)) or
        ( a ==(11, 0) and b ==(12, 0)) or
        ( a ==(12, 0) and b ==(13, 0)) or
        ( a ==(13, 0) and b ==(14, 0)) or
        ( a ==(14, 0) and b ==(15, 0)) or
        ( a ==(15, 0) and b ==(16, 0)) or
        ( a ==(16, 0) and b ==(17, 0)) or
        ( a ==(17, 0) and b ==(18, 0)) or
        ( a ==(18, 0) and b ==(19, 0)) or
        ( a ==(19, 0) and b ==(20, 0)) or
        ( a ==(20, 0) and b ==(21, 0)) or
        ( a ==(21, 0) and b ==(22, 0)) or
        ( a ==(22, 0) and b ==(23, 0)) or
        ( a ==(23, 0) and b ==(24, 0)) or
        ( a ==(24, 0) and b ==(25, 0)) or
        ( a ==(25, 0) and b ==(26, 0)) or
        ( a ==(26, 0) and b ==(27, 0)) or
        ( a ==(27, 0) and b ==(28, 0)) or
        ( a ==(28, 0) and b ==(29, 0)) or
        ( a ==(29, 0) and b ==(30, 0)) or
        ( a ==(30, 0) and b ==(31, 0)) or
        ( a ==(31, 0) and b ==(32, 0)) or
        ( a ==(32, 0) and b ==(33, 0)) or
        ( a ==(33, 0) and b ==(34, 0)) or
        ( a ==(34, 0) and b ==(35, 0)) or
        ( a ==(35, 0) and b ==(36, 0)) or
        ( a ==(36, 0) and b ==(37, 0)) or
        ( a ==(37, 0) and b ==(38, 0)) or
        ( a ==(38, 0) and b ==(39, 0)) or
        ( a ==(39, 0) and b ==(40, 0)) or
        ( a ==(40, 0) and b ==(41, 0)) or
        ( a ==(41, 0) and b ==(42, 0)) or
        ( a ==(42, 0) and b ==(43, 0)) or
        ( a ==(43, 0) and b ==(44, 0)) or
        ( a ==(44, 0) and b ==(45, 0)) or
        ( a ==(45, 0) and b ==(46, 0)) or
        ( a ==(46, 0) and b ==(47, 0)) or
        ( a ==(47, 0) and b ==(48, 0)) or
        ( a ==(48, 0) and b ==(49, 0)) or
        ( a ==(49, 0) and b ==(50, 0)) or
        ( a ==(50, 0) and b ==(51, 0)) or
        ( a ==(51, 0) and b ==(52, 0)) or
        ( a ==(52, 0) and b ==(53, 0)) or
        ( a ==(53, 0) and b ==(54, 0)) or
        ( a ==(54, 0) and b ==(55, 0)) or
        ( a ==(55, 0) and b ==(56, 0)) or
        ( a ==(56, 0) and b ==(57, 0)) or
        ( a ==(57, 0) and b ==(58, 0)) or
        ( a ==(58, 0) and b ==(59, 0)) or
        ( a ==(59, 0) and b ==(60, 0)) or
        ( a ==(60, 0) and b ==(61, 0)) or
        ( a ==(61, 0) and b ==(62, 0)) or
        ( a ==(62, 0) and b ==(63, 0)) or
        ( a ==(63, 0) and b ==(64, 0)) or
        ( a ==(64, 0) and b ==(65, 0)) or
        ( a ==(65, 0) and b ==(66, 0)) or
        ( a ==(66, 0) and b ==(67, 0)) or
        ( a ==(67, 0) and b ==(68, 0)) or
        ( a ==(68, 0) and b ==(69, 0)) or
        ( a ==(69, 0) and b ==(70, 0)) or
        ( a ==(70, 0) and b ==(71, 0)) or
        ( a ==(71, 0) and b ==(72, 0)) or
        ( a ==(72, 0) and b ==(73, 0)) or
        ( a ==(73, 0) and b ==(74, 0)) or
        ( a ==(74, 0) and b ==(75, 0)) or
        ( a ==(75, 0) and b ==(76, 0)) or
        ( a ==(76, 0) and b ==(77, 0)) or
        ( a ==(77, 0) and b ==(78, 0)) or
        ( a ==(78, 0) and b ==(79, 0)) or
        ( a ==(79, 0) and b ==(80, 0)) or
        ( a ==(80, 0) and b ==(81, 0)) or
        ( a ==(81, 0) and b ==(82, 0)) or
        ( a ==(82, 0) and b ==(83, 0)) or
        ( a ==(83, 0) and b ==(84, 0)) or
        ( a ==(84, 0) and b ==(85, 0)) or
        ( a ==(85, 0) and b ==(86, 0)) or
        ( a ==(86, 0) and b ==(87, 0)) or
        ( a ==(87, 0) and b ==(88, 0)) or
        ( a ==(88, 0) and b ==(89, 0)) or
        ( a ==(89, 0) and b ==(90, 0)) or
        ( a ==(90, 0) and b ==(91, 0)) or
        ( a ==(91, 0) and b ==(92, 0)) or
        ( a ==(92, 0) and b ==(93, 0)) or
        ( a ==(93, 0) and b ==(94, 0)) or
        ( a ==(94, 0) and b ==(95, 0)) or
        ( a ==(95, 0) and b ==(96, 0)) or
        ( a ==(96, 0) and b ==(97, 0)) or
        ( a ==(97, 0) and b ==(98, 0)) or
        ( a ==(98, 0) and b ==(99, 0)) or
        ( a ==(99, 0) and b ==(100, 0)) or
        ( a ==(100, 0) and b ==(101, 0)) or
        ( a ==(101, 0) and b ==(102, 0)) or
        ( a ==(102, 0) and b ==(103, 0)) or
        ( a ==(103, 0) and b ==(104, 0)) or
        ( a ==(104, 0) and b ==(105, 0)) or
        ( a ==(105, 0) and b ==(106, 0)) or
        ( a ==(106, 0) and b ==(107, 0)) or
        ( a ==(107, 0) and b ==(108, 0)) or
        ( a ==(108, 0) and b ==(109, 0)) or
        ( a ==(109, 0) and b ==(110, 0)) or
        ( a ==(110, 0) and b ==(111, 0)) or
        ( a ==(111, 0) and b ==(112, 0)) or
        ( a ==(112, 0) and b ==(113, 0)) or
        ( a ==(113, 0) and b ==(114, 0)) or
        ( a ==(114, 0) and b ==(115, 0)) or
        ( a ==(115, 0) and b ==(116, 0)) or
        ( a ==(116, 0) and b ==(117, 0)) or
        ( a ==(117, 0) and b ==(118, 0)) or
        ( a ==(118, 0) and b ==(119, 0)) or
        ( a ==(119, 0) and b ==(120, 0)) or
        ( a ==(120, 0) and b ==(121, 0)) or
        ( a ==(121, 0) and b ==(122, 0)) or
        ( a ==(122, 0) and b ==(123, 0)) or
        ( a ==(123, 0) and b ==(124, 0)) or
        ( a ==(124, 0) and b ==(125, 0)) or
        ( a ==(125, 0) and b ==(126, 0)) or
        ( a ==(126, 0) and b ==(127, 0)) or
        ( a ==(127, 0) and b ==(128, 0)) or
        ( a ==(128, 0) and b ==(129, 0)) or
        ( a ==(129, 0) and b ==(130, 0)) or
        ( a ==(130, 0) and b ==(131, 0)) or
        ( a ==(131, 0) and b ==(132, 0)) or
        ( a ==(132, 0) and b ==(133, 0)) or
        ( a ==(133, 0) and b ==(134, 0)) or
        ( a ==(134, 0) and b ==(135, 0)) or
        ( a ==(135, 0) and b ==(136, 0)) or
        ( a ==(136, 0) and b ==(137, 0)) or
        ( a ==(137, 0) and b ==(138, 0)) or
        ( a ==(138, 0) and b ==(139, 0)) or
        ( a ==(139, 0) and b ==(140, 0)) or
        ( a ==(140, 0) and b ==(141, 0)) or
        ( a ==(141, 0) and b ==(142, 0)) or
        ( a ==(142, 0) and b ==(143, 0)) or
        ( a ==(143, 0) and b ==(144, 0)) or
        ( a ==(144, 0) and b ==(145, 0)) or
        ( a ==(145, 0) and b ==(146, 0)) or
        ( a ==(146, 0) and b ==(147, 0)) or
        ( a ==(147, 0) and b ==(148, 0)) or
        ( a ==(148, 0) and b ==(149, 0)) or
        ( a ==(149, 0) and b ==(150, 0)) or
        ( a ==(150, 0) and b ==(151, 0)) or
        ( a ==(151, 0) and b ==(152, 0)) or
        ( a ==(152, 0) and b ==(153, 0)) or
        ( a ==(153, 0) and b ==(154, 0)) or
        ( a ==(154, 0) and b ==(155, 0)) or
        ( a ==(155, 0) and b ==(156, 0)) or
        ( a ==(156, 0) and b ==(157, 0)) or
        ( a ==(157, 0) and b ==(158, 0)) or
        ( a ==(158, 0) and b ==(159, 0)) or
        ( a ==(159, 0) and b ==(160, 0)) or
        ( a ==(160, 0) and b ==(161, 0)) or
        ( a ==(161, 0) and b ==(162, 0)) or
        ( a ==(162, 0) and b ==(163, 0)) or
        ( a ==(163, 0) and b ==(164, 0)) or
        ( a ==(164, 0) and b ==(165, 0)) or
        ( a ==(165, 0) and b ==(166, 0)) or
        ( a ==(166, 0) and b ==(167, 0)) or
        ( a ==(167, 0) and b ==(168, 0)) or
        ( a ==(168, 0) and b ==(169, 0)) or
        ( a ==(169, 0) and b ==(170, 0)) or
        ( a ==(170, 0) and b ==(171, 0)) or
        ( a ==(171, 0) and b ==(172, 0)) or
        ( a ==(172, 0) and b ==(173, 0)) or
        ( a ==(173, 0) and b ==(174, 0)) or
        ( a ==(174, 0) and b ==(175, 0)) or
        ( a ==(175, 0) and b ==(176, 0)) or
        ( a ==(176, 0) and b ==(177, 0)) or
        ( a ==(177, 0) and b ==(178, 0)) or
        ( a ==(178, 0) and b ==(179, 0)) or
        ( a ==(179, 0) and b ==(180, 0)) or
        ( a ==(180, 0) and b ==(181, 0)) or
        ( a ==(181, 0) and b ==(182, 0)) or
        ( a ==(182, 0) and b ==(183, 0)) or
        ( a ==(183, 0) and b ==(184, 0)) or
        ( a ==(184, 0) and b ==(185, 0)) or
        ( a ==(185, 0) and b ==(186, 0)) or
        ( a ==(186, 0) and b ==(187, 0)) or
        ( a ==(187, 0) and b ==(188, 0)) or
        ( a ==(188, 0) and b ==(189, 0)) or
        ( a ==(189, 0) and b ==(190, 0)) or
        ( a ==(190, 0) and b ==(191, 0)) or
        ( a ==(191, 0) and b ==(192, 0)) or
        ( a ==(192, 0) and b ==(193, 0)) or
        ( a ==(193, 0) and b ==(194, 0)) or
        ( a ==(194, 0) and b ==(195, 0)) or
        ( a ==(195, 0) and b ==(196, 0)) or
        ( a ==(196, 0) and b ==(197, 0)) or
        ( a ==(197, 0) and b ==(198, 0)) or
        ( a ==(198, 0) and b ==(199, 0)) or
        ( a ==(199, 0) and b ==(200, 0))):
            return 1

        if (( a ==(199, 0) and b ==(199, 1)) or
        ( a ==(199, 1) and b ==(199, 2)) or
        ( a ==(199, 2) and b ==(199, 3)) or
        ( a ==(199, 3) and b ==(199, 4)) or
        ( a ==(199, 4) and b ==(199, 5)) or
        ( a ==(199, 5) and b ==(199, 6)) or
        ( a ==(199, 6) and b ==(199, 7)) or
        ( a ==(199, 7) and b ==(199, 8)) or
        ( a ==(199, 8) and b ==(199, 9)) or
        ( a ==(199, 9) and b ==(199, 10)) or
        ( a ==(199, 10) and b ==(199, 11)) or
        ( a ==(199, 11) and b ==(199, 12)) or
        ( a ==(199, 12) and b ==(199, 13)) or
        ( a ==(199, 13) and b ==(199, 14)) or
        ( a ==(199, 14) and b ==(199, 15)) or
        ( a ==(199, 15) and b ==(199, 16)) or
        ( a ==(199, 16) and b ==(199, 17)) or
        ( a ==(199, 17) and b ==(199, 18)) or
        ( a ==(199, 18) and b ==(199, 19)) or
        ( a ==(199, 19) and b ==(199, 20)) or
        ( a ==(199, 20) and b ==(199, 21)) or
        ( a ==(199, 21) and b ==(199, 22)) or
        ( a ==(199, 22) and b ==(199, 23)) or
        ( a ==(199, 23) and b ==(199, 24)) or
        ( a ==(199, 24) and b ==(199, 25)) or
        ( a ==(199, 25) and b ==(199, 26)) or
        ( a ==(199, 26) and b ==(199, 27)) or
        ( a ==(199, 27) and b ==(199, 28)) or
        ( a ==(199, 28) and b ==(199, 29)) or
        ( a ==(199, 29) and b ==(199, 30)) or
        ( a ==(199, 30) and b ==(199, 31)) or
        ( a ==(199, 31) and b ==(199, 32)) or
        ( a ==(199, 32) and b ==(199, 33)) or
        ( a ==(199, 33) and b ==(199, 34)) or
        ( a ==(199, 34) and b ==(199, 35)) or
        ( a ==(199, 35) and b ==(199, 36)) or
        ( a ==(199, 36) and b ==(199, 37)) or
        ( a ==(199, 37) and b ==(199, 38)) or
        ( a ==(199, 38) and b ==(199, 39)) or
        ( a ==(199, 39) and b ==(199, 40))):
            return 1

        if (( a ==(199, 40) and b ==(198, 40)) or
        ( a ==(198, 40) and b ==(197, 40)) or
        ( a ==(197, 40) and b ==(196, 40)) or
        ( a ==(196, 40) and b ==(195, 40)) or
        ( a ==(195, 40) and b ==(194, 40)) or
        ( a ==(194, 40) and b ==(193, 40)) or
        ( a ==(193, 40) and b ==(192, 40)) or
        ( a ==(192, 40) and b ==(191, 40)) or
        ( a ==(191, 40) and b ==(190, 40)) or
        ( a ==(190, 40) and b ==(189, 40)) or
        ( a ==(189, 40) and b ==(188, 40)) or
        ( a ==(188, 40) and b ==(187, 40)) or
        ( a ==(187, 40) and b ==(186, 40)) or
        ( a ==(186, 40) and b ==(185, 40)) or
        ( a ==(185, 40) and b ==(184, 40)) or
        ( a ==(184, 40) and b ==(183, 40)) or
        ( a ==(183, 40) and b ==(182, 40)) or
        ( a ==(182, 40) and b ==(181, 40)) or
        ( a ==(181, 40) and b ==(180, 40)) or
        ( a ==(180, 40) and b ==(179, 40)) or
        ( a ==(179, 40) and b ==(178, 40)) or
        ( a ==(178, 40) and b ==(177, 40)) or
        ( a ==(177, 40) and b ==(176, 40)) or
        ( a ==(176, 40) and b ==(175, 40)) or
        ( a ==(175, 40) and b ==(174, 40)) or
        ( a ==(174, 40) and b ==(173, 40)) or
        ( a ==(173, 40) and b ==(172, 40)) or
        ( a ==(172, 40) and b ==(171, 40)) or
        ( a ==(171, 40) and b ==(170, 40)) or
        ( a ==(170, 40) and b ==(169, 40)) or
        ( a ==(169, 40) and b ==(168, 40)) or
        ( a ==(168, 40) and b ==(167, 40)) or
        ( a ==(167, 40) and b ==(166, 40)) or
        ( a ==(166, 40) and b ==(165, 40)) or
        ( a ==(165, 40) and b ==(164, 40)) or
        ( a ==(164, 40) and b ==(163, 40)) or
        ( a ==(163, 40) and b ==(162, 40)) or
        ( a ==(162, 40) and b ==(161, 40)) or
        ( a ==(161, 40) and b ==(160, 40)) or
        ( a ==(160, 40) and b ==(159, 40)) or
        ( a ==(159, 40) and b ==(158, 40)) or
        ( a ==(158, 40) and b ==(157, 40)) or
        ( a ==(157, 40) and b ==(156, 40)) or
        ( a ==(156, 40) and b ==(155, 40)) or
        ( a ==(155, 40) and b ==(154, 40)) or
        ( a ==(154, 40) and b ==(153, 40)) or
        ( a ==(153, 40) and b ==(152, 40)) or
        ( a ==(152, 40) and b ==(151, 40)) or
        ( a ==(151, 40) and b ==(150, 40)) or
        ( a ==(150, 40) and b ==(149, 40)) or
        ( a ==(149, 40) and b ==(148, 40)) or
        ( a ==(148, 40) and b ==(147, 40)) or
        ( a ==(147, 40) and b ==(146, 40)) or
        ( a ==(146, 40) and b ==(145, 40)) or
        ( a ==(145, 40) and b ==(144, 40)) or
        ( a ==(144, 40) and b ==(143, 40)) or
        ( a ==(143, 40) and b ==(142, 40)) or
        ( a ==(142, 40) and b ==(141, 40)) or
        ( a ==(141, 40) and b ==(140, 40)) or
        ( a ==(140, 40) and b ==(139, 40)) or
        ( a ==(139, 40) and b ==(138, 40)) or
        ( a ==(138, 40) and b ==(137, 40)) or
        ( a ==(137, 40) and b ==(136, 40)) or
        ( a ==(136, 40) and b ==(135, 40)) or
        ( a ==(135, 40) and b ==(134, 40)) or
        ( a ==(134, 40) and b ==(133, 40)) or
        ( a ==(133, 40) and b ==(132, 40)) or
        ( a ==(132, 40) and b ==(131, 40)) or
        ( a ==(131, 40) and b ==(130, 40)) or
        ( a ==(130, 40) and b ==(129, 40)) or
        ( a ==(129, 40) and b ==(128, 40)) or
        ( a ==(128, 40) and b ==(127, 40)) or
        ( a ==(127, 40) and b ==(126, 40)) or
        ( a ==(126, 40) and b ==(125, 40)) or
        ( a ==(125, 40) and b ==(124, 40)) or
        ( a ==(124, 40) and b ==(123, 40)) or
        ( a ==(123, 40) and b ==(122, 40)) or
        ( a ==(122, 40) and b ==(121, 40)) or
        ( a ==(121, 40) and b ==(120, 40)) or
        ( a ==(120, 40) and b ==(119, 40)) or
        ( a ==(119, 40) and b ==(118, 40)) or
        ( a ==(118, 40) and b ==(117, 40)) or
        ( a ==(117, 40) and b ==(116, 40)) or
        ( a ==(116, 40) and b ==(115, 40)) or
        ( a ==(115, 40) and b ==(114, 40)) or
        ( a ==(114, 40) and b ==(113, 40)) or
        ( a ==(113, 40) and b ==(112, 40)) or
        ( a ==(112, 40) and b ==(111, 40)) or
        ( a ==(111, 40) and b ==(110, 40)) or
        ( a ==(110, 40) and b ==(109, 40)) or
        ( a ==(109, 40) and b ==(108, 40)) or
        ( a ==(108, 40) and b ==(107, 40)) or
        ( a ==(107, 40) and b ==(106, 40)) or
        ( a ==(106, 40) and b ==(105, 40)) or
        ( a ==(105, 40) and b ==(104, 40)) or
        ( a ==(104, 40) and b ==(103, 40)) or
        ( a ==(103, 40) and b ==(102, 40)) or
        ( a ==(102, 40) and b ==(101, 40)) or
        ( a ==(101, 40) and b ==(100, 40)) or
        ( a ==(100, 40) and b ==(99, 40)) or
        ( a ==(99, 40) and b ==(98, 40)) or
        ( a ==(98, 40) and b ==(97, 40)) or
        ( a ==(97, 40) and b ==(96, 40)) or
        ( a ==(96, 40) and b ==(95, 40)) or
        ( a ==(95, 40) and b ==(94, 40)) or
        ( a ==(94, 40) and b ==(93, 40)) or
        ( a ==(93, 40) and b ==(92, 40)) or
        ( a ==(92, 40) and b ==(91, 40)) or
        ( a ==(91, 40) and b ==(90, 40)) or
        ( a ==(90, 40) and b ==(89, 40)) or
        ( a ==(89, 40) and b ==(88, 40)) or
        ( a ==(88, 40) and b ==(87, 40)) or
        ( a ==(87, 40) and b ==(86, 40)) or
        ( a ==(86, 40) and b ==(85, 40)) or
        ( a ==(85, 40) and b ==(84, 40)) or
        ( a ==(84, 40) and b ==(83, 40)) or
        ( a ==(83, 40) and b ==(82, 40)) or
        ( a ==(82, 40) and b ==(81, 40)) or
        ( a ==(81, 40) and b ==(80, 40)) or
        ( a ==(80, 40) and b ==(79, 40)) or
        ( a ==(79, 40) and b ==(78, 40)) or
        ( a ==(78, 40) and b ==(77, 40)) or
        ( a ==(77, 40) and b ==(76, 40)) or
        ( a ==(76, 40) and b ==(75, 40)) or
        ( a ==(75, 40) and b ==(74, 40)) or
        ( a ==(74, 40) and b ==(73, 40)) or
        ( a ==(73, 40) and b ==(72, 40)) or
        ( a ==(72, 40) and b ==(71, 40)) or
        ( a ==(71, 40) and b ==(70, 40)) or
        ( a ==(70, 40) and b ==(69, 40)) or
        ( a ==(69, 40) and b ==(68, 40)) or
        ( a ==(68, 40) and b ==(67, 40)) or
        ( a ==(67, 40) and b ==(66, 40)) or
        ( a ==(66, 40) and b ==(65, 40)) or
        ( a ==(65, 40) and b ==(64, 40)) or
        ( a ==(64, 40) and b ==(63, 40)) or
        ( a ==(63, 40) and b ==(62, 40)) or
        ( a ==(62, 40) and b ==(61, 40)) or
        ( a ==(61, 40) and b ==(60, 40)) or
        ( a ==(60, 40) and b ==(59, 40)) or
        ( a ==(59, 40) and b ==(58, 40)) or
        ( a ==(58, 40) and b ==(57, 40)) or
        ( a ==(57, 40) and b ==(56, 40)) or
        ( a ==(56, 40) and b ==(55, 40)) or
        ( a ==(55, 40) and b ==(54, 40)) or
        ( a ==(54, 40) and b ==(53, 40)) or
        ( a ==(53, 40) and b ==(52, 40)) or
        ( a ==(52, 40) and b ==(51, 40)) or
        ( a ==(51, 40) and b ==(50, 40)) or
        ( a ==(50, 40) and b ==(49, 40)) or
        ( a ==(49, 40) and b ==(48, 40)) or
        ( a ==(48, 40) and b ==(47, 40)) or
        ( a ==(47, 40) and b ==(46, 40)) or
        ( a ==(46, 40) and b ==(45, 40)) or
        ( a ==(45, 40) and b ==(44, 40)) or
        ( a ==(44, 40) and b ==(43, 40)) or
        ( a ==(43, 40) and b ==(42, 40)) or
        ( a ==(42, 40) and b ==(41, 40)) or
        ( a ==(41, 40) and b ==(40, 40)) or
        ( a ==(40, 40) and b ==(39, 40)) or
        ( a ==(39, 40) and b ==(38, 40)) or
        ( a ==(38, 40) and b ==(37, 40)) or
        ( a ==(37, 40) and b ==(36, 40)) or
        ( a ==(36, 40) and b ==(35, 40)) or
        ( a ==(35, 40) and b ==(34, 40)) or
        ( a ==(34, 40) and b ==(33, 40)) or
        ( a ==(33, 40) and b ==(32, 40)) or
        ( a ==(32, 40) and b ==(31, 40)) or
        ( a ==(31, 40) and b ==(30, 40)) or
        ( a ==(30, 40) and b ==(29, 40)) or
        ( a ==(29, 40) and b ==(28, 40)) or
        ( a ==(28, 40) and b ==(27, 40)) or
        ( a ==(27, 40) and b ==(26, 40)) or
        ( a ==(26, 40) and b ==(25, 40)) or
        ( a ==(25, 40) and b ==(24, 40)) or
        ( a ==(24, 40) and b ==(23, 40)) or
        ( a ==(23, 40) and b ==(22, 40)) or
        ( a ==(22, 40) and b ==(21, 40)) or
        ( a ==(21, 40) and b ==(20, 40)) or
        ( a ==(20, 40) and b ==(19, 40)) or
        ( a ==(19, 40) and b ==(18, 40)) or
        ( a ==(18, 40) and b ==(17, 40)) or
        ( a ==(17, 40) and b ==(16, 40)) or
        ( a ==(16, 40) and b ==(15, 40)) or
        ( a ==(15, 40) and b ==(14, 40)) or
        ( a ==(14, 40) and b ==(13, 40)) or
        ( a ==(13, 40) and b ==(12, 40)) or
        ( a ==(12, 40) and b ==(11, 40)) or
        ( a ==(11, 40) and b ==(10, 40)) or
        ( a ==(10, 40) and b ==(9, 40)) or
        ( a ==(9, 40) and b ==(8, 40)) or
        ( a ==(8, 40) and b ==(7, 40)) or
        ( a ==(7, 40) and b ==(6, 40)) or
        ( a ==(6, 40) and b ==(5, 40)) or
        ( a ==(5, 40) and b ==(4, 40)) or
        ( a ==(4, 40) and b ==(3, 40)) or
        ( a ==(3, 40) and b ==(2, 40)) or
        ( a ==(2, 40) and b ==(1, 40)) or
        ( a ==(1, 40) and b ==(0, 40)) or
        ( a ==(0, 40) and b ==(-1, 40))):
            return 1

        if (( a ==(199, 80) and b ==(199, 81)) or
        ( a ==(199, 81) and b ==(199, 82)) or
        ( a ==(199, 82) and b ==(199, 83)) or
        ( a ==(199, 83) and b ==(199, 84)) or
        ( a ==(199, 84) and b ==(199, 85)) or
        ( a ==(199, 85) and b ==(199, 86)) or
        ( a ==(199, 86) and b ==(199, 87)) or
        ( a ==(199, 87) and b ==(199, 88)) or
        ( a ==(199, 88) and b ==(199, 89)) or
        ( a ==(199, 89) and b ==(199, 90)) or
        ( a ==(199, 90) and b ==(199, 91)) or
        ( a ==(199, 91) and b ==(199, 92)) or
        ( a ==(199, 92) and b ==(199, 93)) or
        ( a ==(199, 93) and b ==(199, 94)) or
        ( a ==(199, 94) and b ==(199, 95)) or
        ( a ==(199, 95) and b ==(199, 96)) or
        ( a ==(199, 96) and b ==(199, 97)) or
        ( a ==(199, 97) and b ==(199, 98)) or
        ( a ==(199, 98) and b ==(199, 99)) or
        ( a ==(199, 99) and b ==(199, 100)) or
        ( a ==(199, 100) and b ==(199, 101)) or
        ( a ==(199, 101) and b ==(199, 102)) or
        ( a ==(199, 102) and b ==(199, 103)) or
        ( a ==(199, 103) and b ==(199, 104)) or
        ( a ==(199, 104) and b ==(199, 105)) or
        ( a ==(199, 105) and b ==(199, 106)) or
        ( a ==(199, 106) and b ==(199, 107)) or
        ( a ==(199, 107) and b ==(199, 108)) or
        ( a ==(199, 108) and b ==(199, 109)) or
        ( a ==(199, 109) and b ==(199, 110)) or
        ( a ==(199, 110) and b ==(199, 111)) or
        ( a ==(199, 111) and b ==(199, 112)) or
        ( a ==(199, 112) and b ==(199, 113)) or
        ( a ==(199, 113) and b ==(199, 114)) or
        ( a ==(199, 114) and b ==(199, 115)) or
        ( a ==(199, 115) and b ==(199, 116)) or
        ( a ==(199, 116) and b ==(199, 117)) or
        ( a ==(199, 117) and b ==(199, 118)) or
        ( a ==(199, 118) and b ==(199, 119)) or
        ( a ==(199, 119) and b ==(199, 120))):
            return 1

        if (( a ==(199, 160) and b ==(199, 161)) or
        ( a ==(199, 161) and b ==(199, 162)) or
        ( a ==(199, 162) and b ==(199, 163)) or
        ( a ==(199, 163) and b ==(199, 164)) or
        ( a ==(199, 164) and b ==(199, 165)) or
        ( a ==(199, 165) and b ==(199, 166)) or
        ( a ==(199, 166) and b ==(199, 167)) or
        ( a ==(199, 167) and b ==(199, 168)) or
        ( a ==(199, 168) and b ==(199, 169)) or
        ( a ==(199, 169) and b ==(199, 170)) or
        ( a ==(199, 170) and b ==(199, 171)) or
        ( a ==(199, 171) and b ==(199, 172)) or
        ( a ==(199, 172) and b ==(199, 173)) or
        ( a ==(199, 173) and b ==(199, 174)) or
        ( a ==(199, 174) and b ==(199, 175)) or
        ( a ==(199, 175) and b ==(199, 176)) or
        ( a ==(199, 176) and b ==(199, 177)) or
        ( a ==(199, 177) and b ==(199, 178)) or
        ( a ==(199, 178) and b ==(199, 179)) or
        ( a ==(199, 179) and b ==(199, 180)) or
        ( a ==(199, 180) and b ==(199, 181)) or
        ( a ==(199, 181) and b ==(199, 182)) or
        ( a ==(199, 182) and b ==(199, 183)) or
        ( a ==(199, 183) and b ==(199, 184)) or
        ( a ==(199, 184) and b ==(199, 185)) or
        ( a ==(199, 185) and b ==(199, 186)) or
        ( a ==(199, 186) and b ==(199, 187)) or
        ( a ==(199, 187) and b ==(199, 188)) or
        ( a ==(199, 188) and b ==(199, 189)) or
        ( a ==(199, 189) and b ==(199, 190)) or
        ( a ==(199, 190) and b ==(199, 191)) or
        ( a ==(199, 191) and b ==(199, 192)) or
        ( a ==(199, 192) and b ==(199, 193)) or
        ( a ==(199, 193) and b ==(199, 194)) or
        ( a ==(199, 194) and b ==(199, 195)) or
        ( a ==(199, 195) and b ==(199, 196)) or
        ( a ==(199, 196) and b ==(199, 197)) or
        ( a ==(199, 197) and b ==(199, 198)) or
        ( a ==(199, 198) and b ==(199, 199))):
            return 1

        if (( a ==(0, 40) and b ==(0, 41)) or
        ( a ==(0, 41) and b ==(0, 42)) or
        ( a ==(0, 42) and b ==(0, 43)) or
        ( a ==(0, 43) and b ==(0, 44)) or
        ( a ==(0, 44) and b ==(0, 45)) or
        ( a ==(0, 45) and b ==(0, 46)) or
        ( a ==(0, 46) and b ==(0, 47)) or
        ( a ==(0, 47) and b ==(0, 48)) or
        ( a ==(0, 48) and b ==(0, 49)) or
        ( a ==(0, 49) and b ==(0, 50)) or
        ( a ==(0, 50) and b ==(0, 51)) or
        ( a ==(0, 51) and b ==(0, 52)) or
        ( a ==(0, 52) and b ==(0, 53)) or
        ( a ==(0, 53) and b ==(0, 54)) or
        ( a ==(0, 54) and b ==(0, 55)) or
        ( a ==(0, 55) and b ==(0, 56)) or
        ( a ==(0, 56) and b ==(0, 57)) or
        ( a ==(0, 57) and b ==(0, 58)) or
        ( a ==(0, 58) and b ==(0, 59)) or
        ( a ==(0, 59) and b ==(0, 60)) or
        ( a ==(0, 60) and b ==(0, 61)) or
        ( a ==(0, 61) and b ==(0, 62)) or
        ( a ==(0, 62) and b ==(0, 63)) or
        ( a ==(0, 63) and b ==(0, 64)) or
        ( a ==(0, 64) and b ==(0, 65)) or
        ( a ==(0, 65) and b ==(0, 66)) or
        ( a ==(0, 66) and b ==(0, 67)) or
        ( a ==(0, 67) and b ==(0, 68)) or
        ( a ==(0, 68) and b ==(0, 69)) or
        ( a ==(0, 69) and b ==(0, 70)) or
        ( a ==(0, 70) and b ==(0, 71)) or
        ( a ==(0, 71) and b ==(0, 72)) or
        ( a ==(0, 72) and b ==(0, 73)) or
        ( a ==(0, 73) and b ==(0, 74)) or
        ( a ==(0, 74) and b ==(0, 75)) or
        ( a ==(0, 75) and b ==(0, 76)) or
        ( a ==(0, 76) and b ==(0, 77)) or
        ( a ==(0, 77) and b ==(0, 78)) or
        ( a ==(0, 78) and b ==(0, 79)) or
        ( a ==(0, 79) and b ==(0, 80))):
            return 1

        if (( a ==(0, 120) and b ==(0, 121)) or
        ( a ==(0, 121) and b ==(0, 122)) or
        ( a ==(0, 122) and b ==(0, 123)) or
        ( a ==(0, 123) and b ==(0, 124)) or
        ( a ==(0, 124) and b ==(0, 125)) or
        ( a ==(0, 125) and b ==(0, 126)) or
        ( a ==(0, 126) and b ==(0, 127)) or
        ( a ==(0, 127) and b ==(0, 128)) or
        ( a ==(0, 128) and b ==(0, 129)) or
        ( a ==(0, 129) and b ==(0, 130)) or
        ( a ==(0, 130) and b ==(0, 131)) or
        ( a ==(0, 131) and b ==(0, 132)) or
        ( a ==(0, 132) and b ==(0, 133)) or
        ( a ==(0, 133) and b ==(0, 134)) or
        ( a ==(0, 134) and b ==(0, 135)) or
        ( a ==(0, 135) and b ==(0, 136)) or
        ( a ==(0, 136) and b ==(0, 137)) or
        ( a ==(0, 137) and b ==(0, 138)) or
        ( a ==(0, 138) and b ==(0, 139)) or
        ( a ==(0, 139) and b ==(0, 140)) or
        ( a ==(0, 140) and b ==(0, 141)) or
        ( a ==(0, 141) and b ==(0, 142)) or
        ( a ==(0, 142) and b ==(0, 143)) or
        ( a ==(0, 143) and b ==(0, 144)) or
        ( a ==(0, 144) and b ==(0, 145)) or
        ( a ==(0, 145) and b ==(0, 146)) or
        ( a ==(0, 146) and b ==(0, 147)) or
        ( a ==(0, 147) and b ==(0, 148)) or
        ( a ==(0, 148) and b ==(0, 149)) or
        ( a ==(0, 149) and b ==(0, 150)) or
        ( a ==(0, 150) and b ==(0, 151)) or
        ( a ==(0, 151) and b ==(0, 152)) or
        ( a ==(0, 152) and b ==(0, 153)) or
        ( a ==(0, 153) and b ==(0, 154)) or
        ( a ==(0, 154) and b ==(0, 155)) or
        ( a ==(0, 155) and b ==(0, 156)) or
        ( a ==(0, 156) and b ==(0, 157)) or
        ( a ==(0, 157) and b ==(0, 158)) or
        ( a ==(0, 158) and b ==(0, 159)) or
        ( a ==(0, 159) and b ==(0, 160))):
            return 1

        if (( a ==(199, 120) and b ==(198, 120)) or
        ( a ==(198, 120) and b ==(197, 120)) or
        ( a ==(197, 120) and b ==(196, 120)) or
        ( a ==(196, 120) and b ==(195, 120)) or
        ( a ==(195, 120) and b ==(194, 120)) or
        ( a ==(194, 120) and b ==(193, 120)) or
        ( a ==(193, 120) and b ==(192, 120)) or
        ( a ==(192, 120) and b ==(191, 120)) or
        ( a ==(191, 120) and b ==(190, 120)) or
        ( a ==(190, 120) and b ==(189, 120)) or
        ( a ==(189, 120) and b ==(188, 120)) or
        ( a ==(188, 120) and b ==(187, 120)) or
        ( a ==(187, 120) and b ==(186, 120)) or
        ( a ==(186, 120) and b ==(185, 120)) or
        ( a ==(185, 120) and b ==(184, 120)) or
        ( a ==(184, 120) and b ==(183, 120)) or
        ( a ==(183, 120) and b ==(182, 120)) or
        ( a ==(182, 120) and b ==(181, 120)) or
        ( a ==(181, 120) and b ==(180, 120)) or
        ( a ==(180, 120) and b ==(179, 120)) or
        ( a ==(179, 120) and b ==(178, 120)) or
        ( a ==(178, 120) and b ==(177, 120)) or
        ( a ==(177, 120) and b ==(176, 120)) or
        ( a ==(176, 120) and b ==(175, 120)) or
        ( a ==(175, 120) and b ==(174, 120)) or
        ( a ==(174, 120) and b ==(173, 120)) or
        ( a ==(173, 120) and b ==(172, 120)) or
        ( a ==(172, 120) and b ==(171, 120)) or
        ( a ==(171, 120) and b ==(170, 120)) or
        ( a ==(170, 120) and b ==(169, 120)) or
        ( a ==(169, 120) and b ==(168, 120)) or
        ( a ==(168, 120) and b ==(167, 120)) or
        ( a ==(167, 120) and b ==(166, 120)) or
        ( a ==(166, 120) and b ==(165, 120)) or
        ( a ==(165, 120) and b ==(164, 120)) or
        ( a ==(164, 120) and b ==(163, 120)) or
        ( a ==(163, 120) and b ==(162, 120)) or
        ( a ==(162, 120) and b ==(161, 120)) or
        ( a ==(161, 120) and b ==(160, 120)) or
        ( a ==(160, 120) and b ==(159, 120)) or
        ( a ==(159, 120) and b ==(158, 120)) or
        ( a ==(158, 120) and b ==(157, 120)) or
        ( a ==(157, 120) and b ==(156, 120)) or
        ( a ==(156, 120) and b ==(155, 120)) or
        ( a ==(155, 120) and b ==(154, 120)) or
        ( a ==(154, 120) and b ==(153, 120)) or
        ( a ==(153, 120) and b ==(152, 120)) or
        ( a ==(152, 120) and b ==(151, 120)) or
        ( a ==(151, 120) and b ==(150, 120)) or
        ( a ==(150, 120) and b ==(149, 120)) or
        ( a ==(149, 120) and b ==(148, 120)) or
        ( a ==(148, 120) and b ==(147, 120)) or
        ( a ==(147, 120) and b ==(146, 120)) or
        ( a ==(146, 120) and b ==(145, 120)) or
        ( a ==(145, 120) and b ==(144, 120)) or
        ( a ==(144, 120) and b ==(143, 120)) or
        ( a ==(143, 120) and b ==(142, 120)) or
        ( a ==(142, 120) and b ==(141, 120)) or
        ( a ==(141, 120) and b ==(140, 120)) or
        ( a ==(140, 120) and b ==(139, 120)) or
        ( a ==(139, 120) and b ==(138, 120)) or
        ( a ==(138, 120) and b ==(137, 120)) or
        ( a ==(137, 120) and b ==(136, 120)) or
        ( a ==(136, 120) and b ==(135, 120)) or
        ( a ==(135, 120) and b ==(134, 120)) or
        ( a ==(134, 120) and b ==(133, 120)) or
        ( a ==(133, 120) and b ==(132, 120)) or
        ( a ==(132, 120) and b ==(131, 120)) or
        ( a ==(131, 120) and b ==(130, 120)) or
        ( a ==(130, 120) and b ==(129, 120)) or
        ( a ==(129, 120) and b ==(128, 120)) or
        ( a ==(128, 120) and b ==(127, 120)) or
        ( a ==(127, 120) and b ==(126, 120)) or
        ( a ==(126, 120) and b ==(125, 120)) or
        ( a ==(125, 120) and b ==(124, 120)) or
        ( a ==(124, 120) and b ==(123, 120)) or
        ( a ==(123, 120) and b ==(122, 120)) or
        ( a ==(122, 120) and b ==(121, 120)) or
        ( a ==(121, 120) and b ==(120, 120)) or
        ( a ==(120, 120) and b ==(119, 120)) or
        ( a ==(119, 120) and b ==(118, 120)) or
        ( a ==(118, 120) and b ==(117, 120)) or
        ( a ==(117, 120) and b ==(116, 120)) or
        ( a ==(116, 120) and b ==(115, 120)) or
        ( a ==(115, 120) and b ==(114, 120)) or
        ( a ==(114, 120) and b ==(113, 120)) or
        ( a ==(113, 120) and b ==(112, 120)) or
        ( a ==(112, 120) and b ==(111, 120)) or
        ( a ==(111, 120) and b ==(110, 120)) or
        ( a ==(110, 120) and b ==(109, 120)) or
        ( a ==(109, 120) and b ==(108, 120)) or
        ( a ==(108, 120) and b ==(107, 120)) or
        ( a ==(107, 120) and b ==(106, 120)) or
        ( a ==(106, 120) and b ==(105, 120)) or
        ( a ==(105, 120) and b ==(104, 120)) or
        ( a ==(104, 120) and b ==(103, 120)) or
        ( a ==(103, 120) and b ==(102, 120)) or
        ( a ==(102, 120) and b ==(101, 120)) or
        ( a ==(101, 120) and b ==(100, 120)) or
        ( a ==(100, 120) and b ==(99, 120)) or
        ( a ==(99, 120) and b ==(98, 120)) or
        ( a ==(98, 120) and b ==(97, 120)) or
        ( a ==(97, 120) and b ==(96, 120)) or
        ( a ==(96, 120) and b ==(95, 120)) or
        ( a ==(95, 120) and b ==(94, 120)) or
        ( a ==(94, 120) and b ==(93, 120)) or
        ( a ==(93, 120) and b ==(92, 120)) or
        ( a ==(92, 120) and b ==(91, 120)) or
        ( a ==(91, 120) and b ==(90, 120)) or
        ( a ==(90, 120) and b ==(89, 120)) or
        ( a ==(89, 120) and b ==(88, 120)) or
        ( a ==(88, 120) and b ==(87, 120)) or
        ( a ==(87, 120) and b ==(86, 120)) or
        ( a ==(86, 120) and b ==(85, 120)) or
        ( a ==(85, 120) and b ==(84, 120)) or
        ( a ==(84, 120) and b ==(83, 120)) or
        ( a ==(83, 120) and b ==(82, 120)) or
        ( a ==(82, 120) and b ==(81, 120)) or
        ( a ==(81, 120) and b ==(80, 120)) or
        ( a ==(80, 120) and b ==(79, 120)) or
        ( a ==(79, 120) and b ==(78, 120)) or
        ( a ==(78, 120) and b ==(77, 120)) or
        ( a ==(77, 120) and b ==(76, 120)) or
        ( a ==(76, 120) and b ==(75, 120)) or
        ( a ==(75, 120) and b ==(74, 120)) or
        ( a ==(74, 120) and b ==(73, 120)) or
        ( a ==(73, 120) and b ==(72, 120)) or
        ( a ==(72, 120) and b ==(71, 120)) or
        ( a ==(71, 120) and b ==(70, 120)) or
        ( a ==(70, 120) and b ==(69, 120)) or
        ( a ==(69, 120) and b ==(68, 120)) or
        ( a ==(68, 120) and b ==(67, 120)) or
        ( a ==(67, 120) and b ==(66, 120)) or
        ( a ==(66, 120) and b ==(65, 120)) or
        ( a ==(65, 120) and b ==(64, 120)) or
        ( a ==(64, 120) and b ==(63, 120)) or
        ( a ==(63, 120) and b ==(62, 120)) or
        ( a ==(62, 120) and b ==(61, 120)) or
        ( a ==(61, 120) and b ==(60, 120)) or
        ( a ==(60, 120) and b ==(59, 120)) or
        ( a ==(59, 120) and b ==(58, 120)) or
        ( a ==(58, 120) and b ==(57, 120)) or
        ( a ==(57, 120) and b ==(56, 120)) or
        ( a ==(56, 120) and b ==(55, 120)) or
        ( a ==(55, 120) and b ==(54, 120)) or
        ( a ==(54, 120) and b ==(53, 120)) or
        ( a ==(53, 120) and b ==(52, 120)) or
        ( a ==(52, 120) and b ==(51, 120)) or
        ( a ==(51, 120) and b ==(50, 120)) or
        ( a ==(50, 120) and b ==(49, 120)) or
        ( a ==(49, 120) and b ==(48, 120)) or
        ( a ==(48, 120) and b ==(47, 120)) or
        ( a ==(47, 120) and b ==(46, 120)) or
        ( a ==(46, 120) and b ==(45, 120)) or
        ( a ==(45, 120) and b ==(44, 120)) or
        ( a ==(44, 120) and b ==(43, 120)) or
        ( a ==(43, 120) and b ==(42, 120)) or
        ( a ==(42, 120) and b ==(41, 120)) or
        ( a ==(41, 120) and b ==(40, 120)) or
        ( a ==(40, 120) and b ==(39, 120)) or
        ( a ==(39, 120) and b ==(38, 120)) or
        ( a ==(38, 120) and b ==(37, 120)) or
        ( a ==(37, 120) and b ==(36, 120)) or
        ( a ==(36, 120) and b ==(35, 120)) or
        ( a ==(35, 120) and b ==(34, 120)) or
        ( a ==(34, 120) and b ==(33, 120)) or
        ( a ==(33, 120) and b ==(32, 120)) or
        ( a ==(32, 120) and b ==(31, 120)) or
        ( a ==(31, 120) and b ==(30, 120)) or
        ( a ==(30, 120) and b ==(29, 120)) or
        ( a ==(29, 120) and b ==(28, 120)) or
        ( a ==(28, 120) and b ==(27, 120)) or
        ( a ==(27, 120) and b ==(26, 120)) or
        ( a ==(26, 120) and b ==(25, 120)) or
        ( a ==(25, 120) and b ==(24, 120)) or
        ( a ==(24, 120) and b ==(23, 120)) or
        ( a ==(23, 120) and b ==(22, 120)) or
        ( a ==(22, 120) and b ==(21, 120)) or
        ( a ==(21, 120) and b ==(20, 120)) or
        ( a ==(20, 120) and b ==(19, 120)) or
        ( a ==(19, 120) and b ==(18, 120)) or
        ( a ==(18, 120) and b ==(17, 120)) or
        ( a ==(17, 120) and b ==(16, 120)) or
        ( a ==(16, 120) and b ==(15, 120)) or
        ( a ==(15, 120) and b ==(14, 120)) or
        ( a ==(14, 120) and b ==(13, 120)) or
        ( a ==(13, 120) and b ==(12, 120)) or
        ( a ==(12, 120) and b ==(11, 120)) or
        ( a ==(11, 120) and b ==(10, 120)) or
        ( a ==(10, 120) and b ==(9, 120)) or
        ( a ==(9, 120) and b ==(8, 120)) or
        ( a ==(8, 120) and b ==(7, 120)) or
        ( a ==(7, 120) and b ==(6, 120)) or
        ( a ==(6, 120) and b ==(5, 120)) or
        ( a ==(5, 120) and b ==(4, 120)) or
        ( a ==(4, 120) and b ==(3, 120)) or
        ( a ==(3, 120) and b ==(2, 120)) or
        ( a ==(2, 120) and b ==(1, 120)) or
        ( a ==(1, 120) and b ==(0, 120)) or
        ( a ==(0, 120) and b ==(-1, 120))):
            return 1

        if (( a ==(0, 80) and b ==(1, 80)) or
        ( a ==(1, 80) and b ==(2, 80)) or
        ( a ==(2, 80) and b ==(3, 80)) or
        ( a ==(3, 80) and b ==(4, 80)) or
        ( a ==(4, 80) and b ==(5, 80)) or
        ( a ==(5, 80) and b ==(6, 80)) or
        ( a ==(6, 80) and b ==(7, 80)) or
        ( a ==(7, 80) and b ==(8, 80)) or
        ( a ==(8, 80) and b ==(9, 80)) or
        ( a ==(9, 80) and b ==(10, 80)) or
        ( a ==(10, 80) and b ==(11, 80)) or
        ( a ==(11, 80) and b ==(12, 80)) or
        ( a ==(12, 80) and b ==(13, 80)) or
        ( a ==(13, 80) and b ==(14, 80)) or
        ( a ==(14, 80) and b ==(15, 80)) or
        ( a ==(15, 80) and b ==(16, 80)) or
        ( a ==(16, 80) and b ==(17, 80)) or
        ( a ==(17, 80) and b ==(18, 80)) or
        ( a ==(18, 80) and b ==(19, 80)) or
        ( a ==(19, 80) and b ==(20, 80)) or
        ( a ==(20, 80) and b ==(21, 80)) or
        ( a ==(21, 80) and b ==(22, 80)) or
        ( a ==(22, 80) and b ==(23, 80)) or
        ( a ==(23, 80) and b ==(24, 80)) or
        ( a ==(24, 80) and b ==(25, 80)) or
        ( a ==(25, 80) and b ==(26, 80)) or
        ( a ==(26, 80) and b ==(27, 80)) or
        ( a ==(27, 80) and b ==(28, 80)) or
        ( a ==(28, 80) and b ==(29, 80)) or
        ( a ==(29, 80) and b ==(30, 80)) or
        ( a ==(30, 80) and b ==(31, 80)) or
        ( a ==(31, 80) and b ==(32, 80)) or
        ( a ==(32, 80) and b ==(33, 80)) or
        ( a ==(33, 80) and b ==(34, 80)) or
        ( a ==(34, 80) and b ==(35, 80)) or
        ( a ==(35, 80) and b ==(36, 80)) or
        ( a ==(36, 80) and b ==(37, 80)) or
        ( a ==(37, 80) and b ==(38, 80)) or
        ( a ==(38, 80) and b ==(39, 80)) or
        ( a ==(39, 80) and b ==(40, 80)) or
        ( a ==(40, 80) and b ==(41, 80)) or
        ( a ==(41, 80) and b ==(42, 80)) or
        ( a ==(42, 80) and b ==(43, 80)) or
        ( a ==(43, 80) and b ==(44, 80)) or
        ( a ==(44, 80) and b ==(45, 80)) or
        ( a ==(45, 80) and b ==(46, 80)) or
        ( a ==(46, 80) and b ==(47, 80)) or
        ( a ==(47, 80) and b ==(48, 80)) or
        ( a ==(48, 80) and b ==(49, 80)) or
        ( a ==(49, 80) and b ==(50, 80)) or
        ( a ==(50, 80) and b ==(51, 80)) or
        ( a ==(51, 80) and b ==(52, 80)) or
        ( a ==(52, 80) and b ==(53, 80)) or
        ( a ==(53, 80) and b ==(54, 80)) or
        ( a ==(54, 80) and b ==(55, 80)) or
        ( a ==(55, 80) and b ==(56, 80)) or
        ( a ==(56, 80) and b ==(57, 80)) or
        ( a ==(57, 80) and b ==(58, 80)) or
        ( a ==(58, 80) and b ==(59, 80)) or
        ( a ==(59, 80) and b ==(60, 80)) or
        ( a ==(60, 80) and b ==(61, 80)) or
        ( a ==(61, 80) and b ==(62, 80)) or
        ( a ==(62, 80) and b ==(63, 80)) or
        ( a ==(63, 80) and b ==(64, 80)) or
        ( a ==(64, 80) and b ==(65, 80)) or
        ( a ==(65, 80) and b ==(66, 80)) or
        ( a ==(66, 80) and b ==(67, 80)) or
        ( a ==(67, 80) and b ==(68, 80)) or
        ( a ==(68, 80) and b ==(69, 80)) or
        ( a ==(69, 80) and b ==(70, 80)) or
        ( a ==(70, 80) and b ==(71, 80)) or
        ( a ==(71, 80) and b ==(72, 80)) or
        ( a ==(72, 80) and b ==(73, 80)) or
        ( a ==(73, 80) and b ==(74, 80)) or
        ( a ==(74, 80) and b ==(75, 80)) or
        ( a ==(75, 80) and b ==(76, 80)) or
        ( a ==(76, 80) and b ==(77, 80)) or
        ( a ==(77, 80) and b ==(78, 80)) or
        ( a ==(78, 80) and b ==(79, 80)) or
        ( a ==(79, 80) and b ==(80, 80)) or
        ( a ==(80, 80) and b ==(81, 80)) or
        ( a ==(81, 80) and b ==(82, 80)) or
        ( a ==(82, 80) and b ==(83, 80)) or
        ( a ==(83, 80) and b ==(84, 80)) or
        ( a ==(84, 80) and b ==(85, 80)) or
        ( a ==(85, 80) and b ==(86, 80)) or
        ( a ==(86, 80) and b ==(87, 80)) or
        ( a ==(87, 80) and b ==(88, 80)) or
        ( a ==(88, 80) and b ==(89, 80)) or
        ( a ==(89, 80) and b ==(90, 80)) or
        ( a ==(90, 80) and b ==(91, 80)) or
        ( a ==(91, 80) and b ==(92, 80)) or
        ( a ==(92, 80) and b ==(93, 80)) or
        ( a ==(93, 80) and b ==(94, 80)) or
        ( a ==(94, 80) and b ==(95, 80)) or
        ( a ==(95, 80) and b ==(96, 80)) or
        ( a ==(96, 80) and b ==(97, 80)) or
        ( a ==(97, 80) and b ==(98, 80)) or
        ( a ==(98, 80) and b ==(99, 80)) or
        ( a ==(99, 80) and b ==(100, 80)) or
        ( a ==(100, 80) and b ==(101, 80)) or
        ( a ==(101, 80) and b ==(102, 80)) or
        ( a ==(102, 80) and b ==(103, 80)) or
        ( a ==(103, 80) and b ==(104, 80)) or
        ( a ==(104, 80) and b ==(105, 80)) or
        ( a ==(105, 80) and b ==(106, 80)) or
        ( a ==(106, 80) and b ==(107, 80)) or
        ( a ==(107, 80) and b ==(108, 80)) or
        ( a ==(108, 80) and b ==(109, 80)) or
        ( a ==(109, 80) and b ==(110, 80)) or
        ( a ==(110, 80) and b ==(111, 80)) or
        ( a ==(111, 80) and b ==(112, 80)) or
        ( a ==(112, 80) and b ==(113, 80)) or
        ( a ==(113, 80) and b ==(114, 80)) or
        ( a ==(114, 80) and b ==(115, 80)) or
        ( a ==(115, 80) and b ==(116, 80)) or
        ( a ==(116, 80) and b ==(117, 80)) or
        ( a ==(117, 80) and b ==(118, 80)) or
        ( a ==(118, 80) and b ==(119, 80)) or
        ( a ==(119, 80) and b ==(120, 80)) or
        ( a ==(120, 80) and b ==(121, 80)) or
        ( a ==(121, 80) and b ==(122, 80)) or
        ( a ==(122, 80) and b ==(123, 80)) or
        ( a ==(123, 80) and b ==(124, 80)) or
        ( a ==(124, 80) and b ==(125, 80)) or
        ( a ==(125, 80) and b ==(126, 80)) or
        ( a ==(126, 80) and b ==(127, 80)) or
        ( a ==(127, 80) and b ==(128, 80)) or
        ( a ==(128, 80) and b ==(129, 80)) or
        ( a ==(129, 80) and b ==(130, 80)) or
        ( a ==(130, 80) and b ==(131, 80)) or
        ( a ==(131, 80) and b ==(132, 80)) or
        ( a ==(132, 80) and b ==(133, 80)) or
        ( a ==(133, 80) and b ==(134, 80)) or
        ( a ==(134, 80) and b ==(135, 80)) or
        ( a ==(135, 80) and b ==(136, 80)) or
        ( a ==(136, 80) and b ==(137, 80)) or
        ( a ==(137, 80) and b ==(138, 80)) or
        ( a ==(138, 80) and b ==(139, 80)) or
        ( a ==(139, 80) and b ==(140, 80)) or
        ( a ==(140, 80) and b ==(141, 80)) or
        ( a ==(141, 80) and b ==(142, 80)) or
        ( a ==(142, 80) and b ==(143, 80)) or
        ( a ==(143, 80) and b ==(144, 80)) or
        ( a ==(144, 80) and b ==(145, 80)) or
        ( a ==(145, 80) and b ==(146, 80)) or
        ( a ==(146, 80) and b ==(147, 80)) or
        ( a ==(147, 80) and b ==(148, 80)) or
        ( a ==(148, 80) and b ==(149, 80)) or
        ( a ==(149, 80) and b ==(150, 80)) or
        ( a ==(150, 80) and b ==(151, 80)) or
        ( a ==(151, 80) and b ==(152, 80)) or
        ( a ==(152, 80) and b ==(153, 80)) or
        ( a ==(153, 80) and b ==(154, 80)) or
        ( a ==(154, 80) and b ==(155, 80)) or
        ( a ==(155, 80) and b ==(156, 80)) or
        ( a ==(156, 80) and b ==(157, 80)) or
        ( a ==(157, 80) and b ==(158, 80)) or
        ( a ==(158, 80) and b ==(159, 80)) or
        ( a ==(159, 80) and b ==(160, 80)) or
        ( a ==(160, 80) and b ==(161, 80)) or
        ( a ==(161, 80) and b ==(162, 80)) or
        ( a ==(162, 80) and b ==(163, 80)) or
        ( a ==(163, 80) and b ==(164, 80)) or
        ( a ==(164, 80) and b ==(165, 80)) or
        ( a ==(165, 80) and b ==(166, 80)) or
        ( a ==(166, 80) and b ==(167, 80)) or
        ( a ==(167, 80) and b ==(168, 80)) or
        ( a ==(168, 80) and b ==(169, 80)) or
        ( a ==(169, 80) and b ==(170, 80)) or
        ( a ==(170, 80) and b ==(171, 80)) or
        ( a ==(171, 80) and b ==(172, 80)) or
        ( a ==(172, 80) and b ==(173, 80)) or
        ( a ==(173, 80) and b ==(174, 80)) or
        ( a ==(174, 80) and b ==(175, 80)) or
        ( a ==(175, 80) and b ==(176, 80)) or
        ( a ==(176, 80) and b ==(177, 80)) or
        ( a ==(177, 80) and b ==(178, 80)) or
        ( a ==(178, 80) and b ==(179, 80)) or
        ( a ==(179, 80) and b ==(180, 80)) or
        ( a ==(180, 80) and b ==(181, 80)) or
        ( a ==(181, 80) and b ==(182, 80)) or
        ( a ==(182, 80) and b ==(183, 80)) or
        ( a ==(183, 80) and b ==(184, 80)) or
        ( a ==(184, 80) and b ==(185, 80)) or
        ( a ==(185, 80) and b ==(186, 80)) or
        ( a ==(186, 80) and b ==(187, 80)) or
        ( a ==(187, 80) and b ==(188, 80)) or
        ( a ==(188, 80) and b ==(189, 80)) or
        ( a ==(189, 80) and b ==(190, 80)) or
        ( a ==(190, 80) and b ==(191, 80)) or
        ( a ==(191, 80) and b ==(192, 80)) or
        ( a ==(192, 80) and b ==(193, 80)) or
        ( a ==(193, 80) and b ==(194, 80)) or
        ( a ==(194, 80) and b ==(195, 80)) or
        ( a ==(195, 80) and b ==(196, 80)) or
        ( a ==(196, 80) and b ==(197, 80)) or
        ( a ==(197, 80) and b ==(198, 80)) or
        ( a ==(198, 80) and b ==(199, 80)) or
        ( a ==(199, 80) and b ==(200, 80))):
            return 1

        if (( a ==(0, 160) and b ==(1, 160)) or
        ( a ==(1, 160) and b ==(2, 160)) or
        ( a ==(2, 160) and b ==(3, 160)) or
        ( a ==(3, 160) and b ==(4, 160)) or
        ( a ==(4, 160) and b ==(5, 160)) or
        ( a ==(5, 160) and b ==(6, 160)) or
        ( a ==(6, 160) and b ==(7, 160)) or
        ( a ==(7, 160) and b ==(8, 160)) or
        ( a ==(8, 160) and b ==(9, 160)) or
        ( a ==(9, 160) and b ==(10, 160)) or
        ( a ==(10, 160) and b ==(11, 160)) or
        ( a ==(11, 160) and b ==(12, 160)) or
        ( a ==(12, 160) and b ==(13, 160)) or
        ( a ==(13, 160) and b ==(14, 160)) or
        ( a ==(14, 160) and b ==(15, 160)) or
        ( a ==(15, 160) and b ==(16, 160)) or
        ( a ==(16, 160) and b ==(17, 160)) or
        ( a ==(17, 160) and b ==(18, 160)) or
        ( a ==(18, 160) and b ==(19, 160)) or
        ( a ==(19, 160) and b ==(20, 160)) or
        ( a ==(20, 160) and b ==(21, 160)) or
        ( a ==(21, 160) and b ==(22, 160)) or
        ( a ==(22, 160) and b ==(23, 160)) or
        ( a ==(23, 160) and b ==(24, 160)) or
        ( a ==(24, 160) and b ==(25, 160)) or
        ( a ==(25, 160) and b ==(26, 160)) or
        ( a ==(26, 160) and b ==(27, 160)) or
        ( a ==(27, 160) and b ==(28, 160)) or
        ( a ==(28, 160) and b ==(29, 160)) or
        ( a ==(29, 160) and b ==(30, 160)) or
        ( a ==(30, 160) and b ==(31, 160)) or
        ( a ==(31, 160) and b ==(32, 160)) or
        ( a ==(32, 160) and b ==(33, 160)) or
        ( a ==(33, 160) and b ==(34, 160)) or
        ( a ==(34, 160) and b ==(35, 160)) or
        ( a ==(35, 160) and b ==(36, 160)) or
        ( a ==(36, 160) and b ==(37, 160)) or
        ( a ==(37, 160) and b ==(38, 160)) or
        ( a ==(38, 160) and b ==(39, 160)) or
        ( a ==(39, 160) and b ==(40, 160)) or
        ( a ==(40, 160) and b ==(41, 160)) or
        ( a ==(41, 160) and b ==(42, 160)) or
        ( a ==(42, 160) and b ==(43, 160)) or
        ( a ==(43, 160) and b ==(44, 160)) or
        ( a ==(44, 160) and b ==(45, 160)) or
        ( a ==(45, 160) and b ==(46, 160)) or
        ( a ==(46, 160) and b ==(47, 160)) or
        ( a ==(47, 160) and b ==(48, 160)) or
        ( a ==(48, 160) and b ==(49, 160)) or
        ( a ==(49, 160) and b ==(50, 160)) or
        ( a ==(50, 160) and b ==(51, 160)) or
        ( a ==(51, 160) and b ==(52, 160)) or
        ( a ==(52, 160) and b ==(53, 160)) or
        ( a ==(53, 160) and b ==(54, 160)) or
        ( a ==(54, 160) and b ==(55, 160)) or
        ( a ==(55, 160) and b ==(56, 160)) or
        ( a ==(56, 160) and b ==(57, 160)) or
        ( a ==(57, 160) and b ==(58, 160)) or
        ( a ==(58, 160) and b ==(59, 160)) or
        ( a ==(59, 160) and b ==(60, 160)) or
        ( a ==(60, 160) and b ==(61, 160)) or
        ( a ==(61, 160) and b ==(62, 160)) or
        ( a ==(62, 160) and b ==(63, 160)) or
        ( a ==(63, 160) and b ==(64, 160)) or
        ( a ==(64, 160) and b ==(65, 160)) or
        ( a ==(65, 160) and b ==(66, 160)) or
        ( a ==(66, 160) and b ==(67, 160)) or
        ( a ==(67, 160) and b ==(68, 160)) or
        ( a ==(68, 160) and b ==(69, 160)) or
        ( a ==(69, 160) and b ==(70, 160)) or
        ( a ==(70, 160) and b ==(71, 160)) or
        ( a ==(71, 160) and b ==(72, 160)) or
        ( a ==(72, 160) and b ==(73, 160)) or
        ( a ==(73, 160) and b ==(74, 160)) or
        ( a ==(74, 160) and b ==(75, 160)) or
        ( a ==(75, 160) and b ==(76, 160)) or
        ( a ==(76, 160) and b ==(77, 160)) or
        ( a ==(77, 160) and b ==(78, 160)) or
        ( a ==(78, 160) and b ==(79, 160)) or
        ( a ==(79, 160) and b ==(80, 160)) or
        ( a ==(80, 160) and b ==(81, 160)) or
        ( a ==(81, 160) and b ==(82, 160)) or
        ( a ==(82, 160) and b ==(83, 160)) or
        ( a ==(83, 160) and b ==(84, 160)) or
        ( a ==(84, 160) and b ==(85, 160)) or
        ( a ==(85, 160) and b ==(86, 160)) or
        ( a ==(86, 160) and b ==(87, 160)) or
        ( a ==(87, 160) and b ==(88, 160)) or
        ( a ==(88, 160) and b ==(89, 160)) or
        ( a ==(89, 160) and b ==(90, 160)) or
        ( a ==(90, 160) and b ==(91, 160)) or
        ( a ==(91, 160) and b ==(92, 160)) or
        ( a ==(92, 160) and b ==(93, 160)) or
        ( a ==(93, 160) and b ==(94, 160)) or
        ( a ==(94, 160) and b ==(95, 160)) or
        ( a ==(95, 160) and b ==(96, 160)) or
        ( a ==(96, 160) and b ==(97, 160)) or
        ( a ==(97, 160) and b ==(98, 160)) or
        ( a ==(98, 160) and b ==(99, 160)) or
        ( a ==(99, 160) and b ==(100, 160)) or
        ( a ==(100, 160) and b ==(101, 160)) or
        ( a ==(101, 160) and b ==(102, 160)) or
        ( a ==(102, 160) and b ==(103, 160)) or
        ( a ==(103, 160) and b ==(104, 160)) or
        ( a ==(104, 160) and b ==(105, 160)) or
        ( a ==(105, 160) and b ==(106, 160)) or
        ( a ==(106, 160) and b ==(107, 160)) or
        ( a ==(107, 160) and b ==(108, 160)) or
        ( a ==(108, 160) and b ==(109, 160)) or
        ( a ==(109, 160) and b ==(110, 160)) or
        ( a ==(110, 160) and b ==(111, 160)) or
        ( a ==(111, 160) and b ==(112, 160)) or
        ( a ==(112, 160) and b ==(113, 160)) or
        ( a ==(113, 160) and b ==(114, 160)) or
        ( a ==(114, 160) and b ==(115, 160)) or
        ( a ==(115, 160) and b ==(116, 160)) or
        ( a ==(116, 160) and b ==(117, 160)) or
        ( a ==(117, 160) and b ==(118, 160)) or
        ( a ==(118, 160) and b ==(119, 160)) or
        ( a ==(119, 160) and b ==(120, 160)) or
        ( a ==(120, 160) and b ==(121, 160)) or
        ( a ==(121, 160) and b ==(122, 160)) or
        ( a ==(122, 160) and b ==(123, 160)) or
        ( a ==(123, 160) and b ==(124, 160)) or
        ( a ==(124, 160) and b ==(125, 160)) or
        ( a ==(125, 160) and b ==(126, 160)) or
        ( a ==(126, 160) and b ==(127, 160)) or
        ( a ==(127, 160) and b ==(128, 160)) or
        ( a ==(128, 160) and b ==(129, 160)) or
        ( a ==(129, 160) and b ==(130, 160)) or
        ( a ==(130, 160) and b ==(131, 160)) or
        ( a ==(131, 160) and b ==(132, 160)) or
        ( a ==(132, 160) and b ==(133, 160)) or
        ( a ==(133, 160) and b ==(134, 160)) or
        ( a ==(134, 160) and b ==(135, 160)) or
        ( a ==(135, 160) and b ==(136, 160)) or
        ( a ==(136, 160) and b ==(137, 160)) or
        ( a ==(137, 160) and b ==(138, 160)) or
        ( a ==(138, 160) and b ==(139, 160)) or
        ( a ==(139, 160) and b ==(140, 160)) or
        ( a ==(140, 160) and b ==(141, 160)) or
        ( a ==(141, 160) and b ==(142, 160)) or
        ( a ==(142, 160) and b ==(143, 160)) or
        ( a ==(143, 160) and b ==(144, 160)) or
        ( a ==(144, 160) and b ==(145, 160)) or
        ( a ==(145, 160) and b ==(146, 160)) or
        ( a ==(146, 160) and b ==(147, 160)) or
        ( a ==(147, 160) and b ==(148, 160)) or
        ( a ==(148, 160) and b ==(149, 160)) or
        ( a ==(149, 160) and b ==(150, 160)) or
        ( a ==(150, 160) and b ==(151, 160)) or
        ( a ==(151, 160) and b ==(152, 160)) or
        ( a ==(152, 160) and b ==(153, 160)) or
        ( a ==(153, 160) and b ==(154, 160)) or
        ( a ==(154, 160) and b ==(155, 160)) or
        ( a ==(155, 160) and b ==(156, 160)) or
        ( a ==(156, 160) and b ==(157, 160)) or
        ( a ==(157, 160) and b ==(158, 160)) or
        ( a ==(158, 160) and b ==(159, 160)) or
        ( a ==(159, 160) and b ==(160, 160)) or
        ( a ==(160, 160) and b ==(161, 160)) or
        ( a ==(161, 160) and b ==(162, 160)) or
        ( a ==(162, 160) and b ==(163, 160)) or
        ( a ==(163, 160) and b ==(164, 160)) or
        ( a ==(164, 160) and b ==(165, 160)) or
        ( a ==(165, 160) and b ==(166, 160)) or
        ( a ==(166, 160) and b ==(167, 160)) or
        ( a ==(167, 160) and b ==(168, 160)) or
        ( a ==(168, 160) and b ==(169, 160)) or
        ( a ==(169, 160) and b ==(170, 160)) or
        ( a ==(170, 160) and b ==(171, 160)) or
        ( a ==(171, 160) and b ==(172, 160)) or
        ( a ==(172, 160) and b ==(173, 160)) or
        ( a ==(173, 160) and b ==(174, 160)) or
        ( a ==(174, 160) and b ==(175, 160)) or
        ( a ==(175, 160) and b ==(176, 160)) or
        ( a ==(176, 160) and b ==(177, 160)) or
        ( a ==(177, 160) and b ==(178, 160)) or
        ( a ==(178, 160) and b ==(179, 160)) or
        ( a ==(179, 160) and b ==(180, 160)) or
        ( a ==(180, 160) and b ==(181, 160)) or
        ( a ==(181, 160) and b ==(182, 160)) or
        ( a ==(182, 160) and b ==(183, 160)) or
        ( a ==(183, 160) and b ==(184, 160)) or
        ( a ==(184, 160) and b ==(185, 160)) or
        ( a ==(185, 160) and b ==(186, 160)) or
        ( a ==(186, 160) and b ==(187, 160)) or
        ( a ==(187, 160) and b ==(188, 160)) or
        ( a ==(188, 160) and b ==(189, 160)) or
        ( a ==(189, 160) and b ==(190, 160)) or
        ( a ==(190, 160) and b ==(191, 160)) or
        ( a ==(191, 160) and b ==(192, 160)) or
        ( a ==(192, 160) and b ==(193, 160)) or
        ( a ==(193, 160) and b ==(194, 160)) or
        ( a ==(194, 160) and b ==(195, 160)) or
        ( a ==(195, 160) and b ==(196, 160)) or
        ( a ==(196, 160) and b ==(197, 160)) or
        ( a ==(197, 160) and b ==(198, 160)) or
        ( a ==(198, 160) and b ==(199, 160)) or
        ( a ==(199, 160) and b ==(200, 160))):
            return 1

        # otherwise output max distance (impossible to reach)
        return float('inf')


    """
    my codes that nearly generates the above conditional statements
    (change the values of intial a and b will give all the desire conditions)
    a = [0, 160]
    b = [1, 160]
    print("if (( a ==" + str(tuple(a)) + " and b ==" + str(tuple(b)) + ") or")
    for i in range(199):
        a[0] += 1
        b[0] += 1
        print("( a ==" + str(tuple(a)) + " and b ==" + str(tuple(b)) + ") or")
    print("return 1")

    a = [0, 120]
    b = [0, 121]
    print("if (( a ==" + str(tuple(a)) + " and b ==" + str(tuple(b)) + ") or")
    for i in range(39):
        a[1] += 1
        b[1] += 1
        print("( a ==" + str(tuple(a)) + " and b ==" + str(tuple(b)) + ") or")
    print("return 1")
    """