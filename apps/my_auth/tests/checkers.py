from apps.core.checker import BaseChecker


class BasicUserTesting(BaseChecker):
    fields = ['username', 'uuid', 'wins', 'losses']


class PlayerTesting(BaseChecker):
    fields = ['email', 'username', 'uuid', 'wins', 'losses']


class AuthTesting(BaseChecker):
    fields = ['user', 'games', 'teams', 'all_users']
    auth_user_fields = ['email', 'username', 'uuid', 'token']
    basic_user_fields = ['username', 'uuid', 'wins', 'losses']
    full_user_fields = ['email', 'username', 'uuid', 'token']

    def assertBasicUserEqual(self, data1, data2):
        self.assertDictEqual(data1, data2, self.basic_user_fields)

    def assertFullUserEqual(self, data1, data2):
        self.assertDictEqual(data1, data2, self.full_user_fields)

    def assertAllUsersEqual(self, data, check_against_data):
        self.assertEqual(len(data), len(check_against_data))
        # Need to make sure they're the same order someday

        for username in check_against_data:
            try:
                data.remove(username)
            except ValueError:
                self.fail('All user list didnt match.')

    def assertLoginDataEqual(self):
        # First make sure we got the right fields back
        for field in self.fields:
            self.assertTrue(field in self.responseData)

        # Now we gotta import the other testers
        from apps.games.tests.checkers import GameTesting
        from apps.teams.tests.checkers import TeamTesting

        gameTester = GameTesting()
        teamTester = TeamTesting()

        # First we check the user dict. Fairly simple
        self.assertDictEqual(self.responseData.get('user'),
                             self.check_against_data.get('user'),
                             self.auth_user_fields)

        # Now check the games
        gameTester.assertGamesEqual(self.responseData.get('games'),
                                    self.check_against_data.get('games'))

        # Now check the teams
        teamTester.assertTeamsEqual(self.responseData.get('teams'),
                                    self.check_against_data.get('teams'))

        # Now make sure all the users are there
        self.assertDictListSame(self.responseData.get('all_users'),
                                self.check_against_data.get('all_users'),
                                self.basic_user_fields)
