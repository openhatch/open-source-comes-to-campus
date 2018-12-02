import requests
import requests.auth
import urllib
import json
import tempfile
import subprocess

def _make_auth():
    OAUTH_BASIC_CREDS = open('settings.txt').read().strip()
    auth = requests.auth.HTTPBasicAuth(OAUTH_BASIC_CREDS,
                                       'x-oauth-basic')
    return auth

def sanity_check_creds(oauth_basic_creds):
    resp = requests.get('https://api.github.com/user', auth=_make_auth())
    assert resp.json()['login']

def make_issues_url(owner, repo):
    url = 'https://api.github.com/repos/%s/%s/issues' % (
        urllib.quote(owner),
        urllib.quote(repo))
    return url

def get_source_issues(from_owner, from_repo):
    url = make_issues_url(from_owner, from_repo)
    all_issues = requests.get(url)
    return all_issues

def copy_en_masse(response, new_owner, new_name):
    for item in response.json():
        copy_issue_to(new_owner, new_name,
                      item['title'], item['body'])

def copy_issue_to(repo_owner, repo_name, title, body):
    url = make_issues_url(repo_owner, repo_name)
    data = {'title': title,
            'body': body}
    response = requests.post(url, auth=_make_auth(), data=json.dumps(data))
    assert response.status_code == 201, response.status_code

def make_repo(repo_owner, repo_name, for_org=True):
    assert for_org # NOTE: URL below doesn't work for non-org repos
    url = 'https://api.github.com/orgs/%s/repos' % (
        urllib.quote(repo_owner),)
    response = requests.post(url, auth=_make_auth(), data=json.dumps({'name': repo_name}))
    assert response.status_code == 201, response.status_code


def repo_exists(repo_owner, repo_name):
    url = 'https://api.github.com/repos/%s/%s' % (
        urllib.quote(repo_owner), urllib.quote(repo_name),)
    response = requests.get(url, auth=_make_auth())
    return (response.status_code == 200)


def repo_has_commits(repo_owner, repo_name):
    url = 'https://api.github.com/repos/%s/%s/branches' % (
        urllib.quote(repo_owner), urllib.quote(repo_name),)
    response = requests.get(url, auth=_make_auth())
    if response.status_code == 200:
        return bool(response.json())
    else:
        assert response.status_code == 404
        return False

def _print(s):
    print s

### FIXME: Someone needs to go through this and make the function names make
### sense. Sorry to everyone who reads this before I do that.

def interactive_prepare_event(
        event_name,
        how_many_to_create,
        from_owner,
        from_repo):
    print ("Now is a good time to go create %d Github organizations, "
           "starting with '%s-'." % (how_many_to_create, event_name))
    raw_input("Press enter when you have done that...")

    print ("Great! Now I will go copy GitHub issues from the %s organization "
           "and its %s repo." % (from_owner, from_repo))

    print "First, I will download them..."
    issues = get_source_issues(from_owner, from_repo)

    print "And then, I will copy them..."

    for i in range(how_many_to_create + 1):
        repo_number = i+1 # This is because we use 1-indexing in
        # the name of the repo, e.g. columbia-1.github.io

        org_name = "%s-%d" % (event_name, repo_number)
        repo_name = "%s.github.io" % (org_name,)

        if repo_exists(org_name, repo_name):
            print "Weirdly, %s/%s already exists. Skipping this number." % (
                org_name, repo_name)
            continue

        make_repo(org_name, repo_name)
        copy_en_masse(issues, org_name, repo_name)

    print ("Now I will make sure they all "
           "have the content from the template repository.")


    ### prepare a git clone of template repo
    tempdir = tempfile.mkdtemp(prefix='git_clone_')
    print "Using %s as temp directory for clone..." % (tempdir,)
    print subprocess.check_output(
        ['git', 'clone',
         'https://github.com/%s/%s' % (from_owner, from_repo),
         tempdir])

    for i in range(how_many_to_create):
        repo_number = i+1 # This is because we use 1-indexing in
        # the name of the repo, e.g. columbia-1.github.io

        org_name = "%s-%d" % (event_name, repo_number)
        repo_name = "%s.github.io" % (org_name,)

        if repo_has_commits(org_name, repo_name):
            print (
                "Odd: %s/%s seems to already have content in it. Skipping." % (
                    org_name, repo_name))
            continue


        argv = ['git', 'remote', 'add', str(repo_number), 'git@github.com:%s/%s.git' % ( 
                org_name, repo_name)]
        print subprocess.check_output(argv, cwd=tempdir)
        print subprocess.check_output(['git', 'push', str(repo_number), 'HEAD:master'],
                                      cwd=tempdir)

    print "Okay! It's all done."


def get_parent_github_repo():
    DEFAULT_USERNAME = 'openhatch'
    DEFAULT_REPO = 'github-website-editing-demo'

    # Ask...
    inp = raw_input(
        "What git repo do you want to clone, issues and all? Press enter to"
        " accept the default, which is %s/%s, or provide your own. >" % (
            DEFAULT_USERNAME, DEFAULT_REPO))

    # Handle the empty input, aka defaults
    if not inp.strip():
        return (DEFAULT_USERNAME, DEFAULT_REPO)

    # Syntax-check...
    if inp.count('/') != 1:
        print "You have to specify it in the format of githubusername/githubreponame."
        return get_parent_github_repo()

    # OK! Seems legit.
    return inp.strip().split('/')

def main():
    print "Testing that your credentials work..."
    sanity_check_creds(_make_auth())
    print "Good."
    print ""

    event_name = raw_input("What is the event shortname? This is the "
                           "name used on the web, e.g. for "
                           "columbia.openhatch.org, type columbia here. >")
    how_many = int(raw_input("How many git repositories do you want? "
                             "I recommend no fewer than 3. Up to you, though. >"))
    from_owner, from_repo = get_parent_github_repo()
    interactive_prepare_event(
        event_name,
        how_many,
        from_owner,
        from_repo)
