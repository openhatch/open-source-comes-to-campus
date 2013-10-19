import requests
import requests.auth
import urllib

OAUTH_BASIC_CREDS = open('settings.txt').read().strip()

def make_issues_url(owner, repo):
    url = 'https://api.github.com/repos/%s/%s/issues' % (
        urllib.quote(owner),
        urllib.quote(repo))
    return url

def get_source_issues():
    from_owner = 'openhatch'
    from_repo = 'github-website-editing-demo'
    url = make_issues_url(from_owner, from_repo)
    all_issues = requests.get(url)
    return all_issues

def copy_en_masse(response, new_owner, new_name):
    for item in response.json():
        copy_issue_to(OAUTH_BASIC_CREDS, new_owner, new_name,
                      item['title'], item['body'])

def copy_issue_to(oauth_basic_creds, repo_owner, repo_name,
                  title, body):
    auth = requests.auth.HTTPBasicAuth(OAUTH_BASIC_CREDS,
                                       'x-oauth-basic')
    url = make_issues_url(repo_owner, repo_name)
    data = {'title': title,
            'body': body}
    response = requests.post(url, auth=auth, data=data)
    assert response.status_code == 200

def make_repo(oauth_basic_creds, repo_owner, repo_name,
              for_org=True):
    assert for_org # NOTE: URL below doesn't work for non-org repos
    url = 'https://api.github.com/orgs/%s/repos' % (
        urllib.quote(repo_owner),)
    response = requests.post(url, data={'name': repo_name})
    assert response.status_code == 200
