import requests

from plotly.graph_objs import Bar
from plotly import offline

# Make an API call and store the response
url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
headers = {'Accept': 'application/vnd.github.v3+json'}  # Ask for specific version of the API
r = requests.get(url, headers=headers)  # Make the call to the API
print(f'Status code: {r.status_code}')

# Store API response in a variable
response_dict = r.json()  # r - JSON format, using .json() to convert it to a Python dictionary

# Process Results
repo_dicts = response_dict['items']
repo_links, stars, labels = [], [], []
for repo_dict in repo_dicts:
    repo_name = repo_dict['name']
    repo_url = repo_dict['html_url']
    repo_link = f'<a href="{repo_url}">{repo_name}</a>'
    repo_links.append(repo_link)

    stars.append(repo_dict['stargazers_count'])

    owner = repo_dict['owner']['login']
    description = repo_dict['description']
    label = f'{owner}<br /> {description}'
    labels.append(label)

# Plotting
data = [{
    'type': 'bar',
    'x': repo_links,
    'y': stars,
    'hovertext': labels,
    'marker': {
        'color': 'rgb(245, 170, 66)',
        'line': {'width': 0.5, 'color': 'rgb(245, 102, 66)'},
    },
    'opacity': 0.7,
}]

my_layout = {
    'title': 'Most-Starred Python Projects on Github',
    'xaxis': {
        'title': 'Repository',
        'titlefont': {'size': 20},
        'tickfont': {'size': 20},
    },
    'yaxis': {
        'title': 'Stars',
        'titlefont': {'size': 20},
        'tickfont': {'size': 20},
    },
}

fig = {'data': data, 'layout': my_layout}  # data - List type, layout - Dictionary type
offline.plot(fig, filename='python_repos.html')
