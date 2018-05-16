import requests
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

# make an API call and store the resposne
url = 'https://api.github.com/search/repositories?q=language:python&sort=stars' # API call to request for information
r = requests.get(url)   # send API request and store response object as r
print('Status code:', r.status_code)    # response object has an attribute called status_code, satus_code = 200 indicates successful response

# store API response in a variable
response_dict = r.json()    # the API returns the information in JSON format, json() converts the information to a Python dictionary
# response_dict = {'total_count': 2636866, 'incomplete_result': False, 'items': [{dictionary for each repository on github using python}]}
print('Total repositories:', response_dict['total_count'])

# explore information about the repositories
repo_dicts = response_dict['items']
print('Repositories returned:', len(repo_dicts))    # return number of returned repositories

# extract information from the returned repositories
names, plot_dicts = [], []
for repo_dict in repo_dicts:
    names.append(repo_dict['name'])
    plot_dict = {
        'value':repo_dict['stargazers_count'],
        'label':str(repo_dict['description']),
        'xlink':repo_dict['html_url']   # make the plot interactive
        }
    plot_dicts.append(plot_dict)

# visualize data
my_style = LS('#333366', base_style=LCS)
chart = pygal.Bar(style=my_style, x_label_rotation=45, show_legend=False)
chart.title = 'Most starred Python projects on GitHub'
chart.x_labels = names
chart.add('', plot_dicts)

chart.render_to_file('python_repos.svg')
