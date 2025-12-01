from matchers import And, HasAtLeast, PlaysIn, HasFewerThan, All, Or

class QueryBuilder:
    def __init__(self, matcher=All()):
        self.matcher = matcher

    def plays_in(self, team):
        return QueryBuilder(And(self.matcher, PlaysIn(team)))

    def has_at_least(self, value, attr):
        return QueryBuilder(And(self.matcher, HasAtLeast(value, attr)))

    def has_fewer_than(self, value, attr):
        return QueryBuilder(And(self.matcher, HasFewerThan(value, attr)))

    def one_of(self, builder1, builder2):
        return QueryBuilder(Or(builder1.build(), builder2.build()))

    def build(self):
        return self.matcher