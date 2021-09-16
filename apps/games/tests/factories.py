import datetime

import factory
import factory.fuzzy
import pytz

from apps.my_auth.tests.factories import CustomUserFactory
from apps.teams.tests.factories import TeamFactory

from ..models import Game, Point


class PointFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Point

    class Params:
        inputScoredOn = factory.SubFactory(CustomUserFactory)

    scorer = factory.SubFactory(CustomUserFactory)
    typeOfPoint = factory.fuzzy.FuzzyChoice(item[0] for item in
                                            Point.TYPE_CHOICES)
    scoredOn = factory.LazyAttribute(lambda x: x.inputScoredOn
                                     if x.typeOfPoint
                                     in ['TK', 'SK', 'BS', 'PS'] else None)


class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Game

    time_started = factory.fuzzy.FuzzyDateTime(datetime.datetime(2021, 3, 12, tzinfo=pytz.utc))
    time_ended = factory.LazyAttribute(lambda o: o.time_started + datetime.timedelta(minutes=25))
    team_one = factory.SubFactory(TeamFactory)
    team_two = factory.SubFactory(TeamFactory)

    team_one_score = 11
    team_two_score = 9

    confirmed = False
