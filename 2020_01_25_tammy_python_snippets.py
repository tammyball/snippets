## IMPORTS ##
import sys
import os
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
%matplotlib inline

# Retina on Mac
%config InlineBackend.figure_format = 'retina'

## turn this off if doing image work
import seaborn as sns
sns.set_color_codes()

## pivot table /group by unstack
pd.pivot_table(df, values='total', columns ['x','y'], index = 'date',aggfunc=sum, margins =True)
df.groupby(['field1','field2']).dollars.sum().unstack()

## NULLS ##
df.field = df.field.astype(float).fillna(0.0)
# Fill in NAN in percent
df['pct'] = df.pct.astype(float).fillna(0)
# subset of df where it's NAN
df[df.field.apply(np.isnan)]
# identify which fields have null
df.apply(lambda x: x.isnull().value_counts())

## DATES ##
# Translate date to date format
df['date'] = df.ds.astype('datetime64[ns]')
df['date'] = pd.to_datetime(df['effective_date'],errors='coerce') ## if you need to convert to date

# group by date parts
df.groupby([pd.Grouper(key='date',freq='M')]).expenses.sum()

#generate day information
df['day_of_week'] = df.date.dt.weekday_name
df['weekend_flag'] = np.where(df.day_of_week.isin(['Saturday','Sunday']),'weekend','weekday')
df['week_num'] = df.date.dt.weekofyear
df['month'] = df.date.dt.month
df['year'] = df.date.dt.year

# which weeks are partial weeks?
df.groupby('week_num').agg({'date':['min','max','nuninque']})
week_num_dates = df.groupby('week_num').date.min()
# sort by day of week
weekday_order = ['Saturday','Sunday','Monday','Tuesday','Wednesday','Thursday','Friday']
df.set_index(day_of_week, inplace=True)
df.reindex(weekday_order)

## week over week comparison
import datetime
df['7d_prior_date'] = df.date+ datetime.timedelta(days=-7)
df['7d_prior_value'] = df.dollars.shift(7)

## date diff in SQL
select date_diff('day', cast(firstdatefield as date), cast(todaydatefield as date)) as days_since_cohort
from table
where todaydatefield = '2020-01-01'
limit 10

##  start stop dates (pass parameter to SQL )
start_date = '2020-01-01'
end_date = '2020-01-31'
sql('''
select count(*)
from table
where date BETWEEN '{0}' AND '{1}'
'''.format(start_date, end_date),namespace='x')


## FORMATTING PERCENTS / THOUSANDS COMMA SEPARATOR ##
print("{:,.0%}".format(0.035789)) # percentage without decimals
print("{:,.2%}".format(0.035789)) # percentage w/ decimals
print("{0:,.0f}".format(123894021.8908)) # comma thousands without decimals
print("{0:,.2f}".format(123894021.8908)) # comma thousands w/ decimals

## Format values in dataframe: make new column
df['newcolumn'] = df.oldcolumn.apply("{:,.0%}".format) # percentage without decimals
df['newcolumn'] = df.oldcolumn.apply("{0:,.0f}".format) # comma thousands without decimals

## force scientific to number
df['formatted'] = df.numbercolumn.apply(lambda x: '%.0f' % x)

# Charting: format Y axis as percentage
ax = df.plot()
vals = ax.get_yticks()
ax.set_yticklabels(['{:,.0%}'.format(x) for x in vals])
# ax.set_yticklabels(['{:,.2%}'.format(x) for x in vals]) ## 2 decimal points
## ax.set_yticklabels(['{0:,.0f}'.format(x) for x in vals]) ## y axis comma separator


## CHART TYPES
df.plot(kind='bar', figsize= (15,5))
df.field.hist(bins=range(0,10,1))

## SEABORN CHART TYPES
g = sns.factorplot(x='event_type', y = 'total_clicks', hue = 'which_ad',col= 'company', data = df)
g = sns.barplot(x='event_type', y= 'total_clicks', data = df)
g = set_xticklabels(g.get_xticklabels(), rotation=90)

## MULTIPLE CHARTS
fig, (ax1, ax2) = plt.subplots(nrows = 1,ncols = 2, figsize= (15,7), sharex= True, sharey= True)
# Chart 1
mychart.plot(ax= ax1)
ax1.set_title('chart 1 title')
ax.set_ylabel('label')
# Chart 2
mychart2.plot(ax= ax2)
ax1.set_title('chart 2 title')
# finish the figure
fig.suptitle('big title', size = 20)
plt.savefig('2020-01-01_mychartname.png',bbox_inches ='tight',dpi=300)

## CHART FORMATTING ##
plt.title('my title \n new line break', size = 15)
plt.ylabel('y label')
plt.xlabel('x label')
plt.savefig('2020-01-01_mychartname.png',bbox_inches ='tight',dpi=300)
## wrap titles
from textwrap import textwrap
my_title = 'this is a very long title and gets cropped or runs off the chart'
plt.title(''.join(wrap(my_title,60)))
# rotate chart labels
plt.xticks(rotation = 0)
ax.set_xticklabels(ax1, rotation=90)
## set y axis label min and max
ax.set_ylim([0,100])

# Charting: format Y axis as percentage
ax = df.plot()
vals = ax.get_yticks()
ax.set_yticklabels(['{:,.0%}'.format(x) for x in vals])
# ax.set_yticklabels(['{:,.2%}'.format(x) for x in vals]) ## 2 decimal points
# ax.set_yticklabels(['{0:,.0f}'.format(x) for x in vals]) ## y axis comma separator

# Turn off grid in seaborn
ax = df.plot()
ax.grid(False)

## COLORS ##
# color brewer http://colorbrewer2.org/#type=sequential&scheme=YlGnBu&n=3
# how far apart colors are https://gka.github.io/palettes/#/9|s|00429d,96ffea,ffffe0|ffffe0,ff005e,93003a|1|1
# wes anderson color palettes https://wesandersonpalettes.tumblr.com/
# https://lisacharlotterost.de/2016/04/22/Colors-for-DataVis/

# https://www.w3schools.com/colors/colors_converter.asp
# https://www.w3schools.com/colors/colors_complementary.asp
sns.set_color_codes() # to use the seaborn colors, ex: df.plot(color = 'b')
# 'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'

sns.color_palette('Paired') # Muted, colorblind, Dark
# sequential colors: 'Blues', 'BuGn_r', 'GnBu-d'
# diverging colors: 'coolwarm'
df.plot(color = sns.color_palette('Blues'))

## red, white, blue palette of 5 colors
sns.palplot(sns.diverging_palette(240, 10, n=5))

## dark /light palettes
sns.palplot(sns.dark_palette("purple"))
sns.palplot(sns.light_palette("purple"))
sns.palplot(sns.dark_palette("seagreen", reverse=True))

## your own colors
my_colors =['#9b59b6','#3498db']
sns.palplot(sns.color_palette(my_colors))
sns.palplot(sns.color_palette(['#edf8b1','#7fcdbb','#2c7fb8']))

## hatch marks
df.plot(kind='bar', edgecolor= 'w', hatch = '//')

g = sns.FacetGrid(flat, col='expense_type', col_order=['Food','Transportation'])
g = g.map(sns.barplot,'year','amount')
axes = np.array(g.axes.flat)
two_colors = ['#9b59b6','#3498db']
for n in range(len(two_colors)):
    p1,p2 = axes[n].patches
    p1.set_color(two_colors[n])
    p2.set_color(two_colors[n])
    p2.set_edgecolor('w')
    p2.set_hatch('////')

## String manipulation
df['ticker_length'] = df['ticker_symbol'].str.len() ## length

## extract substring
df = raw_df['myfield'].str.split(',',expand=True)

## CATEGORIZE
df['store_size_cateogry'] = np.where( ( df.store_num <=5 )  , 'big store', 'other')
df['store_size_cateogry'] = np.where( ( df.store_num ==5 ) | ( df.store_num ==9 ) , 1, 0)  ## where this OR that
df['store_size_cateogry'] = np.where( ( df.store_num.isin([1,2,3,4,5]) ) , 1, 0  ) ## in list
df['gas_station_or_not'] = np.where( df.Description.str.contains('SHELL',na=False)  , 'gas', 'other')   ## text like this

# cateogrize with map
my_map = {'iphone6':'iOS','iphone5':'iOS','samsung':'Android'} # all others will be NAN
df['os'] = df.device.map(my_map)
df = df.fillna({'os':'other'}) # fill the uncategorized with others

# bins and cut
bins = [0,141, 143.9, 145]
bin_name = ['0-141','142-143','144']
df['bucket'] = pd.cut(df.my_number, bins, label=bin_name)
df.groupby('bucket').my_number.agg({'min','max'})

## IMAGES ##
import matplotlib.image as mpimg
img = mpimg.imread('myphoto.PNG')
with sns.axes_style("white"):
    plt.imshow(img)
