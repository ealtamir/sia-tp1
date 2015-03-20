from collections import deque
from search_problem_solver.exceptions.engine_exceptions import *
from search_problem_solver.node import Node

class SearchProblemSolver():


    def __init__(self, problem, search_strategy):
        self._problem = problem
        self._search_strategy = search_strategy
        self._frontier = deque()
        self._explored = []
        self._explosionCounter = 0

    def solve(self):
        root = Node(self._problem.getInitialState(), 0)
        self._frontier.append(root)

        failed, finished = self.startExploration()

        if finished:
            print("Solution Found!")
        elif failed:
            print("FAILED! solution not found!")

    def startExploration(self):
        failed = finished = False

        while not failed and not finished:
            if len(self._frontier) <= 0:
                failed = True
            else:
                finished = self.exploreFrontier()

        return failed, finished

    def exploreFrontier(self):
        finished = False
        currentNode = self._frontier.popleft()
        self._explored.append(currentNode)
        if self.isGoal(currentNode):
            finished = True
            print(currentNode.getSolution())
            print("Expanded nodes: %d" % self._explosionCounter)
        else:
            self.explode(currentNode)
            self._explosionCounter += 1
        return finished

    def isGoal(self, node):
        state = node.getState()
        if state is not None:
            return state.compare(self._problem.getGoalState())
        return False

    def explode(self, node):
        if self._problem.getRules() is None:
            raise NoRulesException()

        for rule in self._problem.getRules():
            try:
                state = rule.applyRule(node.getState())
            except NotApplicableException:
                pass

            stateIsNotReplicated = self.checkBranch(node.getParent(), state)
            noBetterOptionFound = self.checkFrontierAndExplored(node.getCost(), state)
            if stateIsNotReplicated and noBetterOptionFound:
                newNode = Node(state, node.getCost() + rule.getCost())
                newNode.setParent(node)
                self.addNode(newNode)

    def checkBranch(self, parent, state):
        """
        Checks if the state of any of the ancestors is the same as the
         state of the current node.
        :return True
        """
        if parent is None:
            return False

        sameStateAsAnAncestor = self.checkBranch(parent , state)
        sameStateAsParent = state is not None and state.compare(parent.getState())
        return  sameStateAsAnAncestor or sameStateAsParent

    def checkFrontierAndExplored(self, cost, state):
        """
        Checks that the current node doesn't have the same state as an
        explored or unexplored node that has a lower cost.
        """
        nodeState = None
        for frontierNode in self._frontier:
            nodeState = frontierNode.getState()
            if nodeState.compare(state) and frontierNode.getCost() < cost:
                return True

        for exploredNode in self._explored:
            nodeState = exploredNode.getState()
            if nodeState.compare(state) and exploredNode.getCost() < cost:
                return True

    def addNode(self, node):
        raise NotImplementedError("This method depends on the search strat.")
