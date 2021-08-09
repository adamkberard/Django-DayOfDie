from apps.core.checker import BaseChecker
from apps.my_auth.tests.checkers import AuthTesting


class FriendTesting(BaseChecker):

    def assertFriendEqual(self, data1, data2):
        userTester = AuthTesting()
        self.fields = [
            'uuid', 'status', 'team_name', 'wins', 'losses', 'league'
        ]
        self.assertDictEqual(data1, data2)

        # Now we check the two users
        userTester.assertBasicUserEqual(data1.get('team_captain'), data2.get('team_captain'))
        userTester.assertBasicUserEqual(data1.get('teammate'), data2.get('teammate'))

    def assertFriendsEqual(self, data1, data2):
        self.assertEqual(len(data1), len(data2))

        for i in range(len(data1)):
            self.assertFriendEqual(data1[i], data2[i])

    def assertFriendDataEqual(self):
        self.loadJSONSafely()

        self.assertFriendEqual(self.responseData, self.check_against_data)