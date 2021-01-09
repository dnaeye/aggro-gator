# Create HTML table from CSV file
# Started 2021-01-01
# Updated 2021-01-01

# Import libraries
import pandas as pd

# Config to show all dataframe columns
pd.set_option('display.max_columns', None)

# Get user input
class import_data:
    def __init__(self):
        self.site = input("Enter site code (Pitchfork=p, Boomkat=b): ")
        self.year = input("Enter year: ")

def get_input():
    return import_data()

user_input = get_input()

if user_input.site == 'p':
    site = 'pitchfork'
elif user_input.site  == 'b':
    site = 'boomkat'
else:
    print('Enter appropriate code.')

year = user_input.year

filename = site + "_" + year + "_html.csv"

# Import album data
df = pd.read_csv("data/" + filename)
try:
    df = df.drop(columns='genre')
except:
    pass

# Create hyperlink to album review
df['album'] = "<a href='" + df['review_url'] + "' target='_blank'>" + df['album'] + "</a>"

df = df.drop(columns='review_url')

# Create webpage header and footer content
html_head = '''
<html>
    <head><title>''' + site.title() + ''''s Top Albums of ''' + year + '''</title></head>
    <link rel="stylesheet" href="css/style.css"/>
    <body>
    <h1>''' + site.title() + ''''s Top Albums of ''' + year + '''</h1>
'''
html_end = '''
    </body>
</html>
'''

# Output HTML code to file
outfile = site + "-" + year + ".html"

with open("html/" + outfile, 'w', encoding="utf-8-sig") as f:
    f.write(html_head)
    f.write('<table width=1280px class="center">')
    f.write('<col style = "width:5%">')
    f.write('<col style = "width:5%">')
    f.write('<col style = "width:15%">')
    f.write('<col style = "width:50%">')
    f.write('<col style = "width:25%">')
    f.write('<thead>')
    f.write('<tr>')
    for header in df.columns:
        if header == 'html':
            f.write('<th>' + "Play Album" + '</th>')
        else:
            f.write('<th>' + str(header).title() + '</th>')
    f.write('</tr>')
    f.write('</thead>')

    for i in range(len(df)):
        f.write('<tr>')
        for col in df.columns:
            value = df.iloc[i][col]
            f.write('<td>' + str(value) + '</td>')
        f.write('<tr>')
    f.write('</table>')
    f.write(html_end)




