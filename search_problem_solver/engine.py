# -*- coding: utf-8 -*-
from collections import deque
from calcudoku.search_strategies.DFS import DFS
from calcudoku.search_strategies.BFS import BSF
from search_problem_solver.exceptions.engine_exceptions import *
from search_problem_solver.node import Node


ROOT_COST = 0

STRATEGIES = {'BFS': BSF, 'DFS': DFS}

class SearchProblemSolver():

    def __init__(self, problem, search_strategy):
        self._problem = problem
        self._search_strategy = search_strategy
        self._frontier = deque()
        self._frontier_hash = {}
        self._explored = []
        self._explored_hash = {}
        self._explosionCounter = 0

    def solve(self):
        root = Node(self._problem.getInitialState(), ROOT_COST)
        self.append_node(root, self._frontier, self._frontier_hash)

        failed, finished = self.start_exploration()

        if finished:
            print("Solution Found!")
        elif failed:
            print("Exploded: %d" % self._explosionCounter)
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
        current_node = self.pop_node(self._frontier, self._frontier_hash)
        self.append_node(current_node, self._explored, self._explored_hash)
        if self.is_goal(current_node):
            finished = True
            print(current_node.get_solution())
            print("Expanded nodes: %d" % self._explosionCounter)
        else:
            self.explode(current_node)
            self._explosionCounter += 1
            if self._explosionCounter % 1000 == 0:
                print("Explosion counter reached %d..." % self._explosionCounter)
                print(current_node)
        return finished

    def is_goal(self, node):
        state = node.state
        if state is not None:
            return self._problem.isGoalState(state)
        return False

    def explode(self, node):
        if self._problem.getRules() is None:
            raise NoRulesException()

        for rule in self._problem.getRules():
            try:
                new_state = rule.applyRule(node.state)
            except NotApplicableException:
                continue

            node_is_valid = self.validate_node(node, new_state)
            if node_is_valid:
                self.add_to_frontier(node, new_state, rule)

    def validate_node(self, node, new_state):
        state_is_replicated = self.replicated_state_in_ancestor(node.parent,
                                                    new_state)
        better_option_found = self.better_node_in_frontier_or_explored(
            node.cost, new_state)
        return not state_is_replicated and not better_option_found

    def replicated_state_in_ancestor(self, parent, state):
        """
        Checks if the state of any of the ancestors is the same as the
        state of the current node.
        If it is the same, then you're in a loop a cycle.
        """
        if parent is None:
            return False

        same_state_as_an_ancestor = self.replicated_state_in_ancestor(
            parent.parent, parent.state)
        same_state_as_parent = state is not None and state.compare(
            parent.state)
        return same_state_as_an_ancestor or same_state_as_parent

    def better_node_in_frontier_or_explored(self, cost, state):
        """
        Checks that the current node doesn't have the same state as an
        explored or unexplored node that has a lower cost.
        """
        # TODO: Ver si combiene pasar esto a un hash
        if state in self._frontier_hash and self._frontier_hash[state].cost < cost:
            return True
        if state in self._explored_hash and self._explored_hash[state].cost < cost:
            return True
        return False

    def add_to_frontier(self, node, new_state, rule):
        # TODO: Ver si conviene calcular el costo en una función
        new_node = Node(new_state, node.cost + rule.cost)
        new_node.parent = node
        self.add_node(new_node)
        self._frontier_hash[new_node] = new_node

    def add_node(self, node):
        strategy_add = STRATEGIES[self._search_strategy]
        strategy_add(node, self._frontier)

    def append_node(self, node, arr, hash):
        arr.append(node)
        hash[node] = node

    def pop_node(self, arr, hash):
        node = arr.popleft()
        del hash[node]
        return node
