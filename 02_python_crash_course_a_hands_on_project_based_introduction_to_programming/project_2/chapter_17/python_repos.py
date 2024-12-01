import requests

# Make an API call and store the response
url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
headers = {'Accept': 'application/vnd.github.v3+json'}  # Ask for specific version of the API
r = requests.get(url, headers=headers)  # Make the call to the API
print(f'Status code: {r.status_code}')

# Store API response in a variable
response_dict = r.json()  # r - JSON format, using .json() to convert it to a Python dictionary
print(f'Total repositories: {response_dict['total_count']}')

# Explore information about the repositories
repo_dicts = response_dict['items']
print(f'Repositories returned: {len(repo_dicts)}')

# Examine the first repository
# repo_dict = repo_dicts[0]
# print(f'\nKeys: {len(repo_dict)}')  # Print number of keys
# for key in sorted(repo_dict.keys()):
#     print(f'\t{key}')

for repo_dict in repo_dicts:
    print(f'\nName: {repo_dict['name']}')
    print(f'Owner: {repo_dict['owner']['login']}')
    print(f'Stars: {repo_dict['stargazers_count']}')
    print(f'Repository: {repo_dict['html_url']}')
    print(f'Created: {repo_dict['created_at']}')
    print(f'Updated: {repo_dict['updated_at']}')
    print(f'Description: {repo_dict['description']}')
