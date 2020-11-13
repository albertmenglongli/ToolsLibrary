from enum import Enum
from typing import List, Union

import gitlab

# URL and Token to provide
GITLAB_URL = ''
GITLAB_TOKEN = ''

gitlab_instance = gitlab.Gitlab(GITLAB_URL, oauth_token=GITLAB_TOKEN, api_version='4')


class GitBranchType(Enum):
    BRANCH = 'branch'
    TAG = 'tag'
    COMMIT = 'commit'


def get_repo_latest_tags(repo_id: Union[str, int], num: int = 5) -> List[str]:
    project = gitlab_instance.projects.get(id=repo_id)
    tags = project.tags.list(per_page=num)
    tag_names = list(map(lambda o: o.name, tags))
    return tag_names


def is_valid_git_branch(repo_id: Union[str, int], branch_tag_commit_id: str) -> bool:
    project = gitlab_instance.projects.get(id=repo_id, lazy=True)
    commits = project.commits.list(ref_name=branch_tag_commit_id, all=False, max_retries=3, obey_rate_limit=False)
    return len(commits) > 0


def get_branch_name_type(repo_id: Union[str, int], branch_name: str) -> GitBranchType:
    from gitlab.exceptions import GitlabGetError
    project = gitlab_instance.projects.get(id=repo_id)

    manager_res_map = {
        'branches': GitBranchType.BRANCH,
        'tags': GitBranchType.TAG,
        'commits': GitBranchType.COMMIT,
    }

    if is_valid_git_branch(repo_id, branch_name):
        for project_xx_manager in manager_res_map.keys():
            try:
                __ = getattr(project, project_xx_manager).get(id=branch_name, max_retries=3)
            except GitlabGetError:
                pass
            else:
                return manager_res_map[project_xx_manager]

    raise ValueError(f'Invalid branch/commit/tag: {branch_name}')


if __name__ == '__main__':
    # repo id in gitlab to provide
    repo_id = ''

    print(get_repo_latest_tags(repo_id))
    assert get_branch_name_type(repo_id, 'master') == GitBranchType.BRANCH
