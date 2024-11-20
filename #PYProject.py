#PYProject2

#Import libaries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 

#Read_csv_filesa
quality=pd.read_csv(r"C:\Users\Mohamed Amr\Downloads\tmdb-movies.csv")
quantity=pd.read_csv(r"C:\Users\Mohamed Amr\Downloads\tmdb-movies (1).csv")

#Data Cleaning and Data Manipulation

#1-drop_duplicates
quality=quality.drop_duplicates()
quantity=quantity.drop_duplicates()

#2-drop_navalues
quantity.drop('homepage',axis='columns',inplace=True)
quantity = quantity[(quantity['budget_adj'] != 0)&(quantity['revenue_adj'] != 0)]

#3-splitting
quality['genres'] = quality['genres'].str.split('|')
quality = quality.explode('genres')

#4-Crafting Derived Features
quantity['month'] = pd.to_datetime(quantity['release_date']).dt.month

#5-Crafting Derived Features

#تعريف دالة classify_interval
def classify_interval(year):
    if 1960 <= year < 1980:
        return '1960-1980'
    elif 1980 <= year < 2000:
        return '1980-2000'
    elif 2000 <= year <= 2015:
        return '2000-2015'
    else:
        return 'Other'

#تعريف دالة classify_season
def classify_season(month):
    if 1 <= int(month) < 4:
        return 'Winter'
    elif 4 <= int(month) < 7:
        return 'Spring'
    elif 7 <= int(month) < 10:
        return 'Summer'
    elif 10 <= int(month) <= 12:
        return 'Fall'
    
quality['interval'] = quality['release_year'].apply(classify_interval)
quality['season'] = quality['month'].apply(classify_season)  

quantity['interval'] = quantity['release_year'].apply(classify_interval)
quantity['ROI'] = (quantity['revenue'] / quantity['budget']) * 100


#Data Analysing And Data Visualization
fig, axs = plt.subplots(2, 3, figsize=(12, 8))


#1-الانواع الاكثر شعبية لكل فترة 
genre_popularity = quality.groupby(['interval', 'genres'])['popularity'].mean().reset_index()
top_genres_by_popularity = genre_popularity.groupby('interval').apply(lambda x: x.nlargest(5, 'popularity')).reset_index(drop=True)
plt.figure(figsize=(10, 6))
#sns.barplot(x='interval', y='popularity', hue='genres', data=top_genres_by_popularity )
sns.barplot(x='interval', y='popularity', hue='genres', data=top_genres_by_popularity , ax=axs[0,0])
axs[0,0].set_title('Top 5 Most Popular Genres\n by Interval', )
axs[0,0].set_ylabel('Average popularity')
axs[0,0].set_xlabel('Year Interval')
axs[0, 0].legend(title='Genres', loc='best', fontsize=4 , title_fontsize=6 )


#2-انواع الافلام الشائعة فى فصل الخريف ذات 
grouped=quality[(quality['season']=='Fall') ]
grouped = grouped.groupby(['interval', 'genres']).size().reset_index(name='count')
grouped60=grouped[grouped['interval']=='1960-1980']
grouped60=grouped60.sort_values(by='count',ascending=False).head(3)
grouped80=grouped[grouped['interval']=='1980-2000']
grouped80=grouped80.sort_values(by='count',ascending=False).head(3)
grouped20=grouped[grouped['interval']=='2000-2015']
grouped20=grouped20.sort_values(by='count',ascending=False).head(3)
combined_data = pd.concat([grouped60, grouped80, grouped20])
#sns.barplot(data=combined_data, x='genres', y='count', hue='interval')
sns.barplot(data=combined_data, x='genres', y='count', hue='interval', ci=None,ax=axs[0,1])
axs[0,1].set_title('Top 3 Popular Genres by Fall Season \n Across Different Time Intervals')
axs[0,1].set_xlabel('Genres')
axs[0,1].set_ylabel('Number of Movies')
axs[0,1].legend(title='Time Interval', loc='best', fontsize=4 , title_fontsize=6)


#3-انواع الافلام الشائعة فى فصل الربيع ذات 
groupeds=quality[quality['season']=='Spring']
groupeds= groupeds.groupby(['interval', 'genres']).size().reset_index(name='count')
grouped60s=groupeds[groupeds['interval']=='1960-1980']
grouped60s=grouped60s.sort_values(by='count',ascending=False).head(3)
grouped80s=groupeds[groupeds['interval']=='1980-2000']
grouped80s=grouped80s.sort_values(by='count',ascending=False).head(3)
grouped20s=groupeds[groupeds['interval']=='2000-2015']
grouped20s=grouped20s.sort_values(by='count',ascending=False).head(3)
combined_datas = pd.concat([grouped60s, grouped80s, grouped20s])
#sns.barplot(data=combined_datas, x='genres', y='count', hue='interval', ci=None )
sns.barplot(data=combined_datas, x='genres', y='count', hue='interval', ci=None , ax=axs[0,2])
axs[0,2].set_title('Top 3 Popular Genres by Spring Season \n Across Different Time Intervals')
axs[0,2].set_xlabel('Genres')
axs[0,2].set_ylabel('Number of Movies')
axs[0,2].legend(title='Time Interval',  loc='best', fontsize=4 , title_fontsize=6)


#4-الشهور الاعلى ايرادات
quantityr=quantity.groupby(['month'])['revenue_adj'].sum()
#quantityr.plot(kind='line', color='skyblue',  marker='o', linestyle='-' )
quantityr.plot(kind='line', color='skyblue',  marker='o', linestyle='-' , ax=axs[1,0])
axs[1,0].set_title('revenue_adj for each month')
axs[1,0].set_xlabel('months')
axs[1,0].set_ylabel('the sum of revenue_adj')


#5-التغير فى متوسط مدة الفيلم لكل عام
avgduration=quality.groupby('release_year')['runtime'].mean()
avgduration.plot(kind='line', color='skyblue',  marker='o', linestyle='-',ax=axs[1,1])
axs[1,1].set_title('The Change in Average of \n Movies Runtime for each Year')
axs[1,1].set_xlabel('Release_Year')
axs[1,1].set_ylabel('Average of Movies Runtime')


#6-العلاقة بين مدة الفيلم و النسبة بين الايرادات و الميزانية فى الفترة من عام 2000 الى عام 2015
RoiD=quality[quality['interval']=='2000-2015']
RoiD=RoiD.groupby([ 'runtime'])['popularity'].mean()
axs[1,2].set_title('The Relation between Movies \n Runtime and Popularity Average')
axs[1,2].set_xlabel('Interval-Movie Runtime')
axs[1,2].set_ylabel('Average of Popularity')
#RoiD.plot(kind='area')
RoiD.plot(kind='area',ax=axs[1,2])


plt.tight_layout()
fig.subplots_adjust(hspace=0.6 , wspace=0.8)
plt.show()

