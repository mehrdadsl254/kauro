import copy
import time
from collections import defaultdict
from itertools import permutations
import boards

class Game:
    def __init__(self,Filtering = None,Ordering = None,valueordering = None):

        self.board = boards.hard1



        self.domains = defaultdict(list)
        self.neighbors = defaultdict(set)
        self.row_neighbors = defaultdict(set)
        self.column_neighbors = defaultdict(set)
        self.number_current_assigned = 0
        self.variables = []
        self.constraints = defaultdict(set)  # {(var1, var2): {(val1, val2), ...}, ...}
        self.vertical_constraints = defaultdict(set) # {variable: vertical_constraints}
        self.horizontal_constraints = defaultdict(set)  # {variable: horizontal_constraints}
        self.assigned_variables = {}  # {variable: value}
        self.unassigned_variables = []
        self.current_assignement = {}
        self.vertical_constrainPo_variable = {}
        self.horizontal_constrainPo_variable = {}
        self.vertical_constraint_current_sum = {}
        self.horizontal_constraint_current_sum = {}
        self.numbers_current_verconstraints_assigned = {}
        self.numbers_current_hoconstraints_assigned = {}
        self.vertical_current_assigneds = defaultdict(set) #{vertical_constraint:{1,2,3}}
        self.horizontal_current_assigneds = defaultdict(set)
        self.counter = 0
        self.Filtering = Filtering
        self.valueordering = valueordering
        self.Ordering = Ordering
        self.get_info()
        self.init_unassigned_varables()
    def init_unassigned_varables(self):
        self.unassigned_variables = [v for v in self.variables]


    def assigne(self, variable, value):
        self.counter += 1
        self.number_current_assigned += 1
        self.current_assignement[variable] = value
        self.unassigned_variables.remove(variable)
        self.board[variable[0]][variable[1]] = value
        self.vertical_current_assigneds[self.vertical_constrainPo_variable[variable]].add(value)
        self.horizontal_current_assigneds[self.horizontal_constrainPo_variable[variable]].add(value)
        self.vertical_constraint_current_sum[self.vertical_constrainPo_variable[variable]] += value
        self.horizontal_constraint_current_sum[self.horizontal_constrainPo_variable[variable]] += value
        self.numbers_current_verconstraints_assigned[self.vertical_constrainPo_variable[variable]] += 1
        self.numbers_current_hoconstraints_assigned[self.horizontal_constrainPo_variable[variable]] += 1

    def unassigne(self, variable, value):
        self.number_current_assigned -= 1
        self.current_assignement[variable] = None
        self.unassigned_variables.append(variable)
        self.board[variable[0]][variable[1]] = ''
        self.vertical_current_assigneds[self.vertical_constrainPo_variable[variable]].remove(value)
        self.horizontal_current_assigneds[self.horizontal_constrainPo_variable[variable]].remove(value)
        self.vertical_constraint_current_sum[self.vertical_constrainPo_variable[variable]] -= value
        self.horizontal_constraint_current_sum[self.horizontal_constrainPo_variable[variable]] -= value
        self.numbers_current_verconstraints_assigned[self.vertical_constrainPo_variable[variable]] -= 1
        self.numbers_current_hoconstraints_assigned[self.horizontal_constrainPo_variable[variable]] -= 1

    def select_variables(self):

        if self.Ordering is None:
            return self.unassigned_variables[0]
        elif self.Ordering == 'MCV':

            min_row_var, min_col_var, max_row_var, max_col_var = self.unassigned_variables[0], self.unassigned_variables[0], \
                                                                 self.unassigned_variables[0], self.unassigned_variables[0]

            for var in self.unassigned_variables:
                if self.horizontal_constraints[var] < self.horizontal_constraints[min_col_var]:
                    min_col_var = var
                if self.vertical_constraints[var] < self.vertical_constraints[min_row_var]:
                    min_row_var = var
                if self.horizontal_constraints[var] > self.horizontal_constraints[max_col_var]:
                    max_col_var = var
                if self.vertical_constraints[var] > self.vertical_constraints[max_row_var]:
                    max_row_var = var

            selected_vars = []

            if self.vertical_constraints[min_row_var] <= self.horizontal_constraints[min_col_var]:
                selected_vars.append(min_row_var)
                for n in self.row_neighbors[min_row_var]:
                    if n in self.unassigned_variables:
                        selected_vars.append(n)
            else:
                selected_vars.append(min_col_var)
                for n in self.column_neighbors[min_col_var]:
                    if n in self.unassigned_variables:
                        selected_vars.append(n)

            mcv = selected_vars[0]
            for var in selected_vars:
                if len(self.domains[var]) < len(self.domains[mcv]):
                    mcv = var

            return mcv




    def ordered_value(self, variable):
        if self.valueordering == 'LCV':
            return sorted(self.domains[variable], key=lambda val: self.lcv(variable, val))
        elif self.valueordering is None:
            return self.domains[variable]
    def lcv(self, variable, value):
        return sum([1 for neighbor in self.neighbors[variable] if value in self.domains[neighbor]])




    def get_board(self):
        return self.board

    def get_info(self):
        variables = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                cell = self.board[i][j]
                if cell != 'X' and '\\' not in cell:
                    variables.append((i, j))
                    if cell != '':
                        self.assigned_variables[(i, j)] = int(cell)
                if '\\' in cell:
                    index = cell.find('\\')  # Find the index of '\\'
                    parts = cell.split('\\')
                    if index > 0:  # n\
                        numberh = int(parts[0])
                        relevant_vars = []
                        k = i + 1
                        while k < len(self.board) and self.board[k][j] != 'X' and '\\' not in self.board[k][j]:
                            relevant_vars.append((k, j))
                            k += 1
                        self.get_info_helper(numberh, relevant_vars,(i,j), is_vertical=False)

                    if index < len(cell) - 1:  # \n
                        number_after = int(parts[1])
                        relevant_vars = []
                        k = j + 1
                        while k < len(self.board[i]) and self.board[i][k] != 'X' and '\\' not in self.board[i][k]:
                            relevant_vars.append((i, k))
                            k += 1
                        self.get_info_helper(number_after, relevant_vars,(i,j), is_vertical=True)

        self.variables = variables



    def is_consistence(self, variable, value):

        for neighbor in self.neighbors[variable]:
            if neighbor in self.current_assignement and self.current_assignement[neighbor] is not None:
                if (self.current_assignement[neighbor], value) not in self.constraints[(neighbor, variable)]:
                    return False


        if (value in self.vertical_current_assigneds[self.vertical_constrainPo_variable[variable]]) or (value in self.horizontal_current_assigneds[self.horizontal_constrainPo_variable[variable]]):
            return False

        if len(self.row_neighbors[variable])  == self.numbers_current_verconstraints_assigned[self.vertical_constrainPo_variable[variable]]:
            if self.vertical_constraint_current_sum[self.vertical_constrainPo_variable[variable]] + value == self.vertical_constraints[variable]:
                return True
            else:
                return False
        if len(self.column_neighbors[variable])  == self.numbers_current_hoconstraints_assigned[self.horizontal_constrainPo_variable[variable]]:
            if self.horizontal_constraint_current_sum[self.horizontal_constrainPo_variable[variable]] + value == self.horizontal_constraints[variable]:
                return True
            else:
                return False



        # print(self.constraint_current_sum[self.vertical_constrainPo_variable[variable]] + value ,'  ')
        # print(self.vertical_constraints[variable], '  ')
        # print(self.constraint_current_sum[self.horizontal_constrainPo_variable[variable]] + value, '  ')
        # print(self.horizontal_constraints[variable], '  ')

        if (self.vertical_constraint_current_sum[self.vertical_constrainPo_variable[variable]] + value < self.vertical_constraints[variable]) and \
                (self.horizontal_constraint_current_sum[self.horizontal_constrainPo_variable[variable]] + value < self.horizontal_constraints[variable]):
            return True
        else:
            return False



    def print_matrix(self):
        for row in self.board:
            for i, element in enumerate(row):
                if isinstance(element, int):
                    print(f"\033[31m{element:<7}\033[0m", end="")
                else:
                    print(f"{element:<7}", end="")
                if i < len(row) - 1:
                    print("| ", end="")
            print()
        print("\n\n\n")


    def filtering(self, variable, value):
        if self.Filtering is None:
            return True
        if self.Filtering == 'FC':
            return self.forward_checking(variable, value)
        elif self.Filtering == 'AC3':
            return self.AC3(variable, value)


    def forward_checking(self, variable, value):
        self.domains[variable] = [value]
        for neighbor in self.neighbors[variable]:
            if neighbor in self.unassigned_variables:
                for value in self.domains[neighbor]:
                    if not self.is_consistence(neighbor,value):
                        self.domains[neighbor].remove(value)
                        if len(self.domains[neighbor]) == 0:
                            return False
        return True


    def AC3(self, variable, value):
        queue = []
        self.domains[variable] = [value]
        for neighbor in self.neighbors[variable]:
            queue.append((neighbor, variable))
        while len(queue) != 0:
            (xi, xj) = queue.pop(0)
            if self.revise(xi, xj):
                if len(self.domains[xi]) == 0:
                    return False
                for neighbor in self.neighbors[xi]:
                    if neighbor != xj:
                        queue.append((neighbor, xi))
        return True

    def revise(self, xi, xj):
        revised = False
        for value in self.domains[xi]:
            if all(not self.has_values(xi,value,xj, val) for val in self.domains[xj]):
                self.domains[xi].remove(value)

                revised = True
        return revised
    def has_values(self, var1, val1,var2,val2):
        for key, value in self.constraints.items():
            if key == (var1,var2):
                if (val1 , val2) in value:
                    return True
        return False




    def Back_track(self):


        if self.number_current_assigned == len(self.variables):
            return self.current_assignement
        variabale = self.select_variables()
        for value in self.ordered_value(variabale):
            if self.is_consistence(variabale, value):
                self.assigne(variabale, value)
                domain_copy = copy.deepcopy(self.domains)
                if self.filtering(variabale, value):
                    result = self.Back_track()
                    if result is not None:
                        return result
                self.domains = domain_copy
                self.unassigne(variabale, value)
        return None

    def get_info_helper(self, number, relevant_vars, constraint_position,is_vertical):

        if is_vertical:
            self.vertical_current_assigneds[constraint_position] = set()
            self.numbers_current_verconstraints_assigned[constraint_position] = 0
            self.vertical_constraint_current_sum[constraint_position] = 0
            for var in relevant_vars:
                self.horizontal_current_assigneds[constraint_position] = set()
                self.vertical_constraints[var] = number
                self.vertical_constrainPo_variable[var] = constraint_position
        else:
            self.numbers_current_hoconstraints_assigned[constraint_position] = 0
            self.horizontal_constraint_current_sum[constraint_position] = 0
            for var in relevant_vars:
                self.horizontal_constraints[var] = number
                self.horizontal_constrainPo_variable[var] = constraint_position
        if len(relevant_vars) == 1:
            self.domains[relevant_vars[0]].append(number)


        dom = set()
        perms = permutations([1, 2, 3, 4, 5, 6, 7, 8, 9], len(relevant_vars))
        possible_perms = []
        for perm in perms:
            if sum(perm) == number:
                possible_perms.append(perm)
                for num in perm:
                    dom.add(num)
        dom = list(dom)

        for perm in possible_perms:
            for i in range(len(relevant_vars)):
                for j in range(len(relevant_vars)):
                    if i != j:
                        self.constraints[(relevant_vars[i], relevant_vars[j])].add((perm[i], perm[j]))
                        self.constraints[(relevant_vars[j], relevant_vars[i])].add((perm[j], perm[i]))

        for domain in dom:
            for var in relevant_vars:
                if var not in self.domains or domain not in self.domains[var]:
                    self.domains[var].append(domain)


        # for var in relevant_vars:
        #         self.domains[var] = [1, 2, 3, 4, 5, 6, 7, 8, 9]



        for v1 in relevant_vars:
            for v2 in relevant_vars:
                if v1 != v2:
                    self.neighbors[v1].add(v2)
                    self.neighbors[v2].add(v1)
                    if is_vertical:
                        self.row_neighbors[v1].add(v2)
                        self.row_neighbors[v2].add(v1)
                    else:
                        self.column_neighbors[v1].add(v2)
                        self.column_neighbors[v2].add(v1)
