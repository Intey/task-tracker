import typing as t
from dataclasses import dataclass
from datetime import date


@dataclass
class Issue:
    key: str
    summary: str
    description: str
    estimation_hours: int = 0
    due_date: date = None
    assignee: t.Optional[str] = None
    skill: t.Optional[str] = None

    def __hash__(self):
        return hash(self.key)

    def __repr__(self):
        return f"<Issue: {self.key}>"


class User:
    nick: str
    skill: str
    workdays_hours: t.Set[int]

    def __init__(self, nick: str, skill: str, workdays_hours: t.Set[int]):
        self.nick = nick
        self.skill = skill
        assert (
            len(workdays_hours) == 7
        ), "User workdays should be 7 days from MON to SUN"
        self.workdays_hours = workdays_hours

    def __str__(self):
        return f"<User {self.nick}>"

    def __repr__(self):
        return f"<User '{self.nick}'>"

    def __hash__(self):
        return hash(self.nick)


@dataclass
class Gantt:
    from_date: date
    to_date: date
    team: t.List[User]
    issues: t.List[Issue]

    def fullfill(
        self, users: t.List[User] = None, issues: t.List[Issue] = None
    ) -> "Plan":

        plan = Plan.empty()
        if users is None:
            users = self.team

        plan.load_team(users)
        if issues is None:
            issues = self.issues
        for i in issues:
            user = plan.most_free_user(skill=i.skill)
            plan.assign_issue(user, i)
        return plan


@dataclass
class Plan:
    user_tasks: t.Dict[User, t.Set[Issue]]
    skill_users: t.Dict[str, t.Set[User]]
    skill_issues: t.Dict[str, t.Set[Issue]]
    days: t.Dict[date, t.Dict[User, Issue]]

    @staticmethod
    def empty() -> "Plan":
        return Plan(
            user_tasks=dict(), skill_users=dict(), skill_issues=dict(), days=dict()
        )

    def assign_issue(self, user: User, issue: Issue):
        self.__add_user_tasks(user, issue)
        self.__add_skill_issue(issue)
        self.__add_skill_user(user)

    def most_free_user(self, skill: str = None) -> User:
        assert self.user_tasks
        minimal_issues = 1000000
        most_free_user_for_skill = None
        most_free_user = list(self.user_tasks.keys())[0]
        for user, issues in self.user_tasks.items():
            user_issues_count = len(list(issues))
            if user_issues_count < minimal_issues:
                most_free_user = user
                minimal_issues = user_issues_count
                if skill is None or user.skill == skill:
                    most_free_user_for_skill = user
        if most_free_user_for_skill is None:
            most_free_user_for_skill = most_free_user
        return most_free_user_for_skill

    def load_team(self, users: t.List[User]):
        for user in users:
            self.__add_skill_user(user)
            self.user_tasks[user] = set()

    def __add_skill_user(self, user: User):
        if self.skill_users.get(user.skill) is None:
            self.skill_users[user.skill] = set()
        self.skill_users[user.skill].add(user)

    def __add_user_tasks(self, user: User, issue: Issue):
        if self.user_tasks.get(user) is None:
            self.user_tasks[user] = set()
        self.user_tasks[user].add(issue)

    def __add_skill_issue(self, issue):
        if self.skill_issues.get(issue.skill) is None:
            self.skill_issues[issue.skill] = set()
        self.skill_issues[issue.skill].add(issue)
