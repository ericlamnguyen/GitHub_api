import requests
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

langs = ['python','JavaScript','Ruby','C','Java','Perl','Haskell','Go']     # list of languages
repo_counts = []    # list of number of repositories for each language
plot_dicts = []

for lang in langs:
    # make an API call and store the response for each language
    url = 'https://api.github.com/search/repositories?q=language:'+lang+'&sort=stars' # API call to request for information
    r = requests.get(url)   # send API request and store response object as r
    print('Status code for '+lang+':', r.status_code)    # response object has an attribute called status_code, satus_code = 200 indicates successful response
    # store API response in a variable

    response_dict = r.json()    # the API returns the information in JSON format, json() converts the information to a Python dictionary
                                # response_dict = {'total_count': 2636866, 'incomplete_result': False, 'items': [{dictionary for each repository on github using python}]}
    repo_counts.append(response_dict['total_count'])

    # return the first repository, i.e. the highest starred
    top_repo_dict = response_dict['items'][0]   # the highest starred repository

    # extract information from the returned repositories
    plot_dict = {
    'value':top_repo_dict['stargazers_count'],
    'label':str(top_repo_dict['description']),
    'xlink':top_repo_dict['html_url']   # embed the link to the repository
    }
    plot_dicts.append(plot_dict)

# visualize data
my_style1 = LS('#0000ff', base_style=LCS)
chart1 = pygal.Bar(style=my_style1, x_label_rotation=45, show_legend=False)
chart1.title = 'Number of repositories by languages'
chart1.x_labels = langs
chart1.add('', repo_counts)
chart1.render_to_file('total_repos.svg')

my_style2 = LS('#ffb6c1', base_style=LCS)
chart2 = pygal.Bar(style=my_style2, x_label_rotation=45, show_legend=False)
chart2.title = 'Most popular repository for each language'
chart2.x_labels = langs
chart2.add('', plot_dicts)
chart2.render_to_file('most_popular_repo.svg')
