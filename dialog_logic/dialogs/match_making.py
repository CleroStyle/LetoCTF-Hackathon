from common.user import *


class MatchMaking:
    findings: list[User] = list()     # в поиске метча

    def add_matches(self, user: User) -> User or bool:
        if user.status == StatusUser.finding:
            possible_match = self._get_finding(not_user=user)
            if possible_match:
                self.findings.remove(possible_match)
                if user in self.findings:
                    self.findings.remove(user)

                possible_match.status = StatusUser.in_match
                user.status = StatusUser.in_match

                possible_match.teammate = user
                user.teammate = possible_match

                return possible_match

        if user not in self.findings:
            self.findings.append(user)
        return False

    def _get_finding(self, not_user: User = None) -> User or bool:
        for possible_match in self.findings:
            if possible_match != not_user:
                return possible_match
        return False

    def delete_match(self, user: User):
        teammate = user.teammate
        if teammate:
            teammate.status = StatusUser.not_playing
            teammate.teammate = None
            teammate.current_round = None
            teammate.count_current_round = 0

        user.status = StatusUser.not_playing
        user.teammate = None
        user.current_round = None
        user.count_current_round = 0

    def set_not_playing(self, user: User = None):
        if user in self.findings:
            self.findings.remove(user)

        teammate = user.teammate
        if teammate:
            teammate.status = StatusUser.finding
            teammate.teammate = None
            self.findings.append(teammate)

        user.status = StatusUser.not_playing
        user.teammate = None
