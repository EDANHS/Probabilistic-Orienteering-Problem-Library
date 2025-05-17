class DefaultAcceptanceCriterion:
    def __call__(self, min_cost, new_cost):
      return new_cost > min_cost