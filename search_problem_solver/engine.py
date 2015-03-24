# -*- coding: utf-8 -*-
from collections import deque
from search_problem_solver.exceptions.engine_exceptions import *
from search_problem_solver.node import Node
from calcudoku.utilities.priorityqueue import *


ROOT_COST = 0


class SearchProblemSolver():

    def __init__(self, problem, search_strategy):
        self._problem = problem
        self._search_strategy = None  # initialized in the method below
        self.set_search_strategy(self, search_strategy)
        self._explored = []
        self._explosionCounter = 0
        if search_strategy == 'Astar' or search_strategy == 'Greedy':
            self._frontier = PriorityQueue()
            self._popfunction = pqpop
        else:
            self._frontier = deque()
            self._popfunction = pop

    def solve(self):
        root = Node(self._problem.getInitialState(), ROOT_COST)
        self._frontier.append(root)

        failed, finished = self.start_exploration()

        if finished:
            print("Solution Found!")
        elif failed:
            print("FAILED! solution not found!")

    def start_exploration(self):
        failed = finished = False

        while not failed and not finished:
            if len(self._frontier) <= 0:
                failed = True
            else:
                finished = self.explore_frontier()

        return failed, finished

    def explore_frontier(self):
        finished = False
        current_node = self._popfunction()
        self._explored.append(current_node)
        if self.is_goal(current_node):
            finished = True
            print(current_node.get_solution())
            print("Expanded nodes: %d" % self._explosionCounter)
        else:
            self.explode(current_node)
            self._explosionCounter += 1
        return finished

    def is_goal(self, node):
        state = node.getState()
        if state is not None:
            return self._problem.isGoalState(state)
        return False

    def explode(self, node):
        if self._problem.getRules() is None:
            raise NoRulesException()

        for rule in self._problem.getRules():
            try:
                new_state = rule.applyRule(node.getState())
            except NotApplicableException:
                continue

            node_is_valid = self.validate_node(node, new_state)
            if node_is_valid:
                self.add_to_frontier(node, new_state, rule)

    def validate_node(self, node, new_state):
        state_is_not_replicated = self.check_branch(node.getParent(), new_state)
        no_better_option_found = self.check_frontier_and_explored(node.getCost(), new_state)
        return state_is_not_replicated and no_better_option_found

    def add_to_frontier(self, node, new_state, rule):
        # TODO: Ver si conviene calcular el costo en una función
        new_node = Node(new_state, node.getCost() + rule.getCost())
        new_node.parent = node
        self.add_node(new_node)

    def check_branch(self, parent, state):
        """
        Checks if the state of any of the ancestors is the same as the
        state of the current node.
        If it is the same, then you're in a loop a cycle.
        """
        if parent is None:
            return False

        same_state_as_an_ancestor = self.check_branch(parent, state)
        same_state_as_parent = state is not None and state.compare(
            parent.getState())
        return same_state_as_an_ancestor or same_state_as_parent

    def check_frontier_and_explored(self, cost, state):
        """
        Checks that the current node doesn't have the same state as an
        explored or unexplored node that has a lower cost.
        """
        # TODO: Ver si combiene pasar esto a un hash
        for frontier_node in self._frontier:
            node_state = frontier_node.getState()
            if node_state.compare(state) and frontier_node.getCost() < cost:
                return True

        for explored_node in self._explored:
            node_state = explored_node.getState()
            if node_state.compare(state) and explored_node.getCost() < cost:
                return True

    def bsf(self, node):
        self._frontier.append(node)

    def dfs(self, node):
        self._frontier.appendleft(node)

    def a_star(self, node):
        self._frontier.pqpush(evaluation(node), node)

    def greedy(self, node):
        self._frontier.pqpush(heuristic(node), node)

    def add_node(self, node):
        self._search_strategy(node)

    def set_search_strategy(self, search_strategy):
        strategies = {
            'BFS': self.bsf,
            'DFS': self.dfs,
            'A-star': self.a_star,
            'Greedy': self.greedy
        }
        self._search_strategy = strategies.get(search_strategy)


def h1(node):
    raise NotImplementedError


def h2(node):
    raise NotImplementedError


# TODO asignarle la que se pase por parametro al programa, no cablearla!
heuristic = h1


def evaluation(node):
    return node.cost + heuristic(node)


def pop(self):
    return self._frontier.popleft()


def pqpop(self):
    return self._frontier.pqpop()
