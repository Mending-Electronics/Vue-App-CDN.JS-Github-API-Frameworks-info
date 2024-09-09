import requests

def get_github_issues(repo_url):
    issues_url = f"{repo_url}/issues"
    security_url = f"{repo_url}/security/advisories"
    releases_url = f"{repo_url}/releases/latest"

    issues_response = requests.get(issues_url)
    security_response = requests.get(security_url)
    releases_response = requests.get(releases_url)

    if issues_response.status_code == 200:
        issues_count = len(issues_response.json())
    else:
        issues_count = 0

    if security_response.status_code == 200:
        security_count = len(security_response.json())
    else:
        security_count = 0

    if releases_response.status_code == 200:
        latest_release = releases_response.json().get('tag_name', 'No release found')
    else:
        latest_release = 'No release found'

    return issues_count, security_count, latest_release

if __name__ == "__main__":
    repo_url = "https://api.github.com/repos/twbs/bootstrap"
    issues_count, security_count, latest_release = get_github_issues(repo_url)
    print(f"Issues: {issues_count}")
    print(f"Security Issues: {security_count}")
    print(f"Latest Release: {latest_release}")
