# -*- coding: utf-8 -*-
from collections import deque
from search_problem_solver.exceptions.engine_exceptions import *
from search_problem_solver.node import Node
from calcudoku.utilities.priorityqueue import *
from calcudoku.search_strategies.astar import a_star
from calcudoku.search_strategies.greedy import greedy
from calcudoku.search_strategies.dfs import dfs
from calcudoku.search_strategies.bfs import bfs


ROOT_COST = 0


class SearchProblemSolver():
    def __init__(self, problem, search_strategy):
        self._problem = problem
        self._search_strategy = None  # initialized in the method below
        self.set_search_strategy(search_strategy)
        self._frontier_hash = {}
        self._explored = []
        self._explored_hash = {}
        self._explosionCounter = 0

        if search_strategy == 'A-star' or search_strategy == 'Greedy':
            self._frontier = PriorityQueue()
            self._pop_function = pqpop
        else:
            self._frontier = deque()
            self._pop_function = pop

    def solve(self):
        root = Node(self._problem.get_initial_state(), ROOT_COST)
        append_node(root, self._frontier, self._frontier_hash)

        failed, finished = self.start_exploration()

        if finished:
            print("Solution Found!")
        elif failed:
            print("Exploded: %d" % self._explosionCounter)
            print("FAILED! solution not found!")
        return {
            'expanded_node': self._explosionCounter,
            'frontier_size': len(self._frontier),
            'explored_size': len(self._explored)
        }

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
        append_node(current_node, self._explored, self._explored_hash)
        if self.is_goal(current_node):
            finished = True
            print 'Solution: '
            solution = current_node.get_solution()
            for i in range(len(solution)):
                print solution[i]
            print("Expanded nodes: %d" % self._explosionCounter)
        else:
            self.explode(current_node)
            self._explosionCounter += 1
            if self._explosionCounter % 5000 == 0:
                print("Exploded %d nodes..." % self._explosionCounter)
        return finished

    def is_goal(self, node):
        state = node.state
        if state is not None:
            return self._problem.is_goal_state(state)
        return False

    def explode(self, node):
        if self._problem.get_rules() is None:
            raise NoRulesException()

        for rule in self._problem.get_rules():
            try:
                new_state = rule.apply_rule(node.state)
            except NotApplicableException:
                continue

            node_is_valid = self.validate_node(node, new_state)
            if node_is_valid:
                self.add_to_frontier(node, new_state, rule)

    def validate_node(self, node, new_state):
        state_is_replicated = self.replicated_state_in_ancestor(node.parent, new_state)
        better_option_found = self.better_node_in_frontier_or_explored(node.cost, new_state)
        return not state_is_replicated and not better_option_found

    def replicated_state_in_ancestor(self, parent, state):
        """
        Checks if the state of any of the ancestors is the same as the
        state of the current node.
        If it is the same, then you're in a loop a cycle.
        """
        if parent is None:
            return False

        same_state_as_an_ancestor = self.replicated_state_in_ancestor(parent.parent, parent.state)
        same_state_as_parent = state is not None and state.compare(parent.state)
        return same_state_as_an_ancestor or same_state_as_parent

    def better_node_in_frontier_or_explored(self, cost, state):
        """
        Checks that the current node doesn't have the same state as an
        explored or unexplored node that has a lower cost.
        """
        if state in self._frontier_hash and self._frontier_hash[state].cost <= cost:
            return True
        if state in self._explored_hash and self._explored_hash[state].cost <= cost:
            return True
        return False

    def add_node(self, node):
        self._search_strategy(node, self._frontier)

    def add_to_frontier(self, node, new_state, rule):
        # TODO: Ver si conviene calcular el costo en una función
        new_node = Node(new_state, node.cost + rule.cost)
        new_node.parent = node
        self.add_node(new_node)
        self._frontier_hash[new_node] = new_node

    def pop_node(self, arr, hash_table):
        node = self._pop_function(arr)
        del hash_table[node]
        return node

    def set_search_strategy(self, search_strategy):
        strategies = {
            'BFS': bfs,
            'DFS': dfs,
            'A-star': a_star,
            'Greedy': greedy
        }
        self._search_strategy = strategies.get(search_strategy)


def pop(arr):
    return arr.popleft()


def pqpop(arr):
    return arr.pqpop()


def append_node(node, arr, hash_table):
    arr.append(node)
    hash_table[node] = node
