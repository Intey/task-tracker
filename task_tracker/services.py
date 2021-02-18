from task_tracker.entities import User, Issue
import typing as t


class IStorage:
    def get_issues(self, skills: t.List[str] = None, assigned=False) -> t.List[Issue]:
        return []

    def get_users(self, skills: t.List[str] = None) -> t.List[User]:
        return []
