# Github Pull Request Stats

I wanted to know what my organizational contributions were on Github. These scripts help me gather that data from [Github's official api](https://developer.github.com/v3/).

## Installation

Install the python dependencies:

```bash
$ pip3 install -r requirements.txt
```

Create a [Github personal access token](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/). It should have the following permissions:

* `repo`
* `read:user`

Fill in your `.env` file.

```bash
$ cp .env.example .env
$ vim .env
```

## Usage

### Pull Requests Reviewed

Use this to calculate how many pull requests you reviewed, returning the latest reviewed state you left for each pull request.

This does not include any reviews made on pull requests you created.

```bash
$ python3 pull_requests_reviewed.py --since 2018-09-01 --until 2019-01-01
```
