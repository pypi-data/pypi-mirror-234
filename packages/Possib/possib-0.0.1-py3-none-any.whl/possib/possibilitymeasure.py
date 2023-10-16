class DiscretePNDistribution:
    '''
    Discrete possibility and necessity distribution.
    
    https://en.wikipedia.org/wiki/Possibility_theory
    https://stats.stackexchange.com/a/590925/69508
    https://stats.stackexchange.com/questions/445832/plausibility-possibility-and-probability
    '''

    def __init__(self, nabla):

        assert max(nabla.values()) == 1

        self.nabla = nabla
        self.omega = frozenset().union(*nabla.keys())

        if frozenset() not in self.nabla:
            self.nabla[frozenset()] = 0
        else:
            assert self.nabla[frozenset()] == 0

    def possibility(self, A):
        '''
        Compute possibility of a set A.
        '''
        if A in self.nabla:
            return self.nabla[A]
        elif A == set():
            return 0
        else:
            result = 0
            explored = frozenset()
            for fs in self.nabla:
                if fs.issubset(A):
                    explored = explored.union(fs)
                    result = max(result, self.possibility(fs))
                    if explored == A:
                        return result
                    else:
                        continue
                else:
                    continue
            return None

    def bound_joint_possiblity(self, sets):
        '''
        Lower and upper bounds on the possilibity of
        an intersection of sets.
        '''
        lower = self.necessity(A)
        upper = min([self.possibility(s) for s in sets])
        return lower, upper

    def necessity(self, A):
        '''
        Compute necessity of a set A.
        '''
        return 1 - self.possibility(self.omega - A)

    def bound_union_necessity(self, sets):
        '''
        Lower and upper bounds on the necessity of
        an union of sets.
        '''
        lower = 0
        upper = self.possibility(frozenset().union(*sets))
        return lower, upper

    def excess_possibility(self, A):
        return self.possibility(A) + self.possibility(self.omega - A) - 1

d = {frozenset({i}):0.5 for i in range(10)}
d.update({frozenset({10}):1})
model = DiscretePNDistribution(d)
