from pytest_factoryboy import register

import factories


register(factories.UserFactory)
register(factories.BoardFactory)
register(factories.BoardParticipantFactory)
register(factories.GoalCategoryFactory)
register(factories.GoalCommentFactory)
register(factories.GoalFactory)

pytest_plugins = 'tests.fixtures'
