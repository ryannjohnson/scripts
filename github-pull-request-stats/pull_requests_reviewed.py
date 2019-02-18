#!/usr/bin/env python3

import argparse
from datetime import datetime
from github.NamedUser import NamedUser
from github.PullRequest import PullRequest
from github.Repository import Repository
import json
from settings import github_session, GITHUB_ORGANIZATION_NAME
import sys
from typing import Generator, List


def for_all_users(since: datetime=None, until: datetime=None, verbose=False):
    user = github_session.get_user()

    output = dict()
    user_pulls = dict()

    for repo in organization_repos(user, GITHUB_ORGANIZATION_NAME):
        for pull in repo_pull_requests(repo, since=since, until=until):

            num_reviews = 0
            for review in pull.get_reviews().reversed: # Reverse chronological order.

                if pull.user.login == review.user.login:
                    # Don't count reviews on own pull request.
                    continue

                user_output = output.setdefault(review.user.login, dict(repos=dict(), totals=dict()))

                if pull.id in user_pulls.setdefault(review.user.login, set()):
                    # Already recorded the latest review for this user.
                    continue

                user_pulls[review.user.login].add(pull.id)
                num_reviews += 1

                add_review_to_user(user_output, repo, pull, review)

            if verbose:
                review_state = fixed_width(str(num_reviews), 5)
                repo_name = fixed_width("{} #{}".format(repo.name, pull.number), 24)
                pull_title = '"{}"'.format(pull.title)
                print(review_state, repo_name, pull_title, file=sys.stderr)

    return output


def for_single_user(since: datetime=None, until: datetime=None, username: str=None, verbose=False):
    user = github_session.get_user()
    if not username:
        username = user.login

    output = dict(repos=dict(), totals=dict())

    for repo in organization_repos(user, GITHUB_ORGANIZATION_NAME):
        for pull in repo_pull_requests(repo, since=since, until=until):

            # Don't count ones you created.
            if pull.user.login == username:
                continue

            for review in pull.get_reviews().reversed: # Reverse chronological order.
                if review.user.login != username:
                    continue

                add_review_to_user(output, repo, pull, review)

                if verbose:
                    review_state = fixed_width(review.state, 17) # Longest should be CHANGES_REQUESTED
                    repo_name = fixed_width("{} #{}".format(repo.name, pull.number), 24)
                    pull_title = '"{}"'.format(pull.title)
                    print(review_state, repo_name, pull_title, file=sys.stderr)

                # Only take the latest.
                break

    return output


def add_review_to_user(user_output, repo, pull, review):
    user_repo = user_output['repos'].setdefault(repo.name, {})
    user_repo.setdefault(review.state, 0)
    user_repo[review.state] += 1

    user_output['totals'].setdefault(review.state, 0)
    user_output['totals'][review.state] += 1


def repo_pull_requests(repo: Repository, since: datetime=None, until: datetime=None) -> Generator[PullRequest, None, None]:
    for pull in repo.get_pulls(sort='created', direction='desc', state='all'):
        if since and pull.created_at < since:
            break
        if until and pull.created_at > until:
            continue
        yield pull


def organization_repos(user: NamedUser, organization_name: str) -> Generator[Repository, None, None]:
    for repo in user.get_repos():
        if not repo.organization:
            continue
        if repo.organization.login != organization_name:
            continue
        yield repo


def fixed_width(s: str, length: int) -> str:
    return (s + " " * length)[:length]


def to_datetime(s: str) -> datetime:
    return datetime.strptime(s, '%Y-%m-%d')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get pull request stats')
    parser.add_argument('-s', '--since', metavar='YYYY-MM-DD', type=to_datetime, required=True)
    parser.add_argument('-u', '--until', metavar='YYYY-MM-DD', type=to_datetime, default=None)
    parser.add_argument('-U', '--username', default=None)
    parser.add_argument('-q', '--quiet', nargs='?', const=True, default=False)

    args = parser.parse_args()

    kwargs = {
        key: args.__dict__[key]
        for key in list(args.__dict__.keys())
        if key in ['since', 'until']
    }
    kwargs['verbose'] = not args.quiet

    if args.username:
        stats = for_single_user(username=args.username, **kwargs)
    else:
        stats = for_all_users(**kwargs)

    print(json.dumps(stats, indent=2, sort_keys=True))
