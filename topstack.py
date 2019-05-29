import requests
import argparse
import log

logger = log.get_logger(__name__)


def retrive_n_top_vote_by_tag(tag, n=10, version='2.2', timeout=10):
    """
    Get N questions have top votes at stackoverflow.com. Using API

    :param n: (int) Number questions need to fetch.
    Default is 10
    :param tag: (string)  Tag filter
    :param version: (string) The version of API you
    connecting to. The default of 2.2 is current version
    :param timeout: (int) Timeout requests module
    :return: (list) The list contains tuples
        Form: [(title question, url question)]
    """

    base_url = 'https://api.stackexchange.com/{}/questions/'.format(version)

    params = {
        'page': 1,
        'sort': 'votes',
        'filter': 'default',
        'pagesize': 100,
        'site': 'stackoverflow'
    }

    result = []
    while True:
        if len(result) > n:
            break

        response = requests.get(base_url, params=params, timeout=timeout)
        response = response.json()

        if 'has_more' in response and response['has_more']:
            params['page'] += 1

        r_questions = []
        if not response['items']:
            raise ValueError('Not data found')
        else:
            r_questions.extend(response['items'])

        for question in r_questions:
            if 'title' not in question:
                continue

            if tag in question['tags']:
                answer_id = (question.get('accepted_answer_id')
                             or question.get('question_id'))
                top_answer_link = ("https://stackoverflow.com/a/{}"
                                   .format(answer_id))
                result.append((question['title'], top_answer_link))

    return result


def main():
    parse = argparse.ArgumentParser(
        description='Get top questions at stackoverflow')

    parse.add_argument('n', action='store', type=int,
                       help='Amount of questions need to get')
    parse.add_argument('tag', action='store',
                       help='Questions tag need to get')

    args = parse.parse_args()
    print(retrive_n_top_vote_by_tag(n=args.n, tag=args.tag))


if __name__ == '__main__':
    main()
