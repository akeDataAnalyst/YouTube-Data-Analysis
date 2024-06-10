#!/usr/bin/env python
# coding: utf-8

# In[1]:


from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# In[8]:


api_key = 'AIzaSyB9rsTgyVjYpBUYGv5O7PbUwzYWajnwxEM'
channel_ids = ['UCHWbZM3BIGgZksvXegx_h3w',      #Enes Yilmazer
                'UCG98giOsUxIlXV0rNUhxLew',    #RyanSerhant
                  'UCu8ucb1LRJd1gwwXutYDgTg']  #Erikvanconover

youtube = build('youtube','v3',developerKey=api_key)


# ## Function to get channel statistics

# In[9]:


def get_channel_stats(youtube,channel_ids):
    all_data = []
    request = youtube.channels().list(
        part='snippet, contentDetails,statistics',
        id=','.join(channel_ids)) #scince channel ids are list we need to convert list into string
                       #which has values separetade commas(use join method)

    response = request.execute()

    for i in range(len(response['items'])):
          data = dict(channel_name = response['items'][i]['snippet']['title'],
                 Subscribers = response['items'][i]['statistics']['subscriberCount'],
                 Views = response ['items'][i]['statistics']['viewCount'],
                 Total_videos = response ['items'][i]['statistics']['videoCount'],
                 playList_id= response ['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
          all_data.append(data)   
    
    return all_data


# In[10]:


get_channel_stats(youtube,channel_ids) 


# In[11]:


channel_statistics= get_channel_stats(youtube,channel_ids)


# In[12]:


channel_data=pd.DataFrame(channel_statistics)


# In[13]:


channel_data


# In[33]:


channel_data.dtypes


# In[41]:


channel_data['Subscribers'] = pd.to_numeric(channel_data['Subscribers'])	
channel_data['Views'] = pd.to_numeric(channel_data['Views'])	
channel_data['Total_videos'] = pd.to_numeric(channel_data['Total_videos'])	
channel_data.dtypes


# In[ ]:





# In[50]:


ax=sns.barplot(x='channel_name',y='Subscribers',data=channel_data)


# In[51]:


ax=sns.barplot(x='channel_name',y='Total_videos',data=channel_data)


# In[52]:


ax=sns.barplot(x='channel_name',y='Views',data=channel_data)


# ## PART -2

# ### SCRAP, ANALAYZ AND VISUALIZE VIDEO DETAILS

# ### Function to get video ids

# In[14]:


channel_data


# In[16]:


playlist_id= channel_data.loc[channel_data['channel_name']=='Enes Yilmazer','playList_id'].iloc[0]


# In[17]:


playlist_id


# In[50]:


def get_video_ids(youtube,playlist_id):

    request = youtube.playlistItems().list(
             part='contentDetails',
             playlistId = playlist_id,
             maxResults = 50)
    response= request.execute()

    video_ids=[]

    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])

    next_page_token = response.get('nextPageToken')
    more_pages = True

    while more_pages:
        if next_page_token is None:
           more_pages = False
        else:
            request = youtube.playlistItems().list(
                        part='contentDetails',
                         playlistId = playlist_id,
                         maxResults = 50,
                         pageToken =next_page_token)
            response= request.execute()

            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])
             
            next_page_token = response.get('nextPageToken')
                                           
    return video_ids


# In[51]:


get_video_ids(youtube, playlist_id)


# In[52]:


video_ids = get_video_ids(youtube, playlist_id)


# In[49]:


video_ids


# ### functions to get video

# In[ ]:


def get_video_details(youtube,video_ids):

    request = youtube.videos().list(
        part ='snippet,statistics',
        id =','.join(video_ids[:50]))
    response= request.execute()

    return response
        


# In[74]:


get_video_details(youtube,video_ids)


# In[77]:


def get_video_details(youtube,video_ids):
    all_video_stats = []
    
    for i in range(0,len(video_ids),50):
        request = youtube.videos().list(
                 part ='snippet,statistics',
                 id =','.join(video_ids[i:i+50]))
        response= request.execute()

        for video in response['items']:
             video_stats = dict(Title = video['snippet']['title'],
                               Published_date = video['snippet']['publishedAt'],
                               Views = video['statistics']['viewCount'],
                               Likes = video['statistics']['likeCount'],
                               Favorites = video['statistics']['favoriteCount'],
                               Comment = video['statistics']['commentCount'])
             all_video_stats.append(video_stats)
    
    return all_video_stats
        


# In[78]:


get_video_details(youtube,video_ids)


# In[79]:


video_details = get_video_details(youtube,video_ids)


# In[80]:


video_data = pd.DataFrame(video_details)


# In[81]:


video_data


# In[82]:


video_data['Published_date']= pd.to_datetime(video_data['Published_date']).dt.date
video_data['Views']= pd.to_numeric(video_data['Views'])
video_data['Likes']= pd.to_numeric(video_data['Likes'])
video_data['Favorites']= pd.to_numeric(video_data['Favorites'])
video_data['Comment']= pd.to_numeric(video_data['Comment'])
video_data


# In[85]:


top10_videos = video_data.sort_values(by ='Views', ascending = False).head(10)


# In[86]:


top10_videos


# In[87]:


ax1=sns.barplot(x='Views', y='Title', data = top10_videos)


# In[88]:


video_data


# In[89]:


video_data['Month'] = pd.to_datetime(video_data['Published_date']).dt.strftime('%b')


# In[90]:


video_data


# In[98]:


videos_per_month = video_data.groupby('Month',as_index =False).size()


# In[99]:


videos_per_month 


# In[95]:


sort_order =['Jan','Feb','Mar','Apr','May','Jun','Jul',
             'Aug','Sep','Oct','Nov','Dec']


# In[100]:


videos_per_month.index = pd.CategoricalIndex(videos_per_month['Month'],categories=sort_order, ordered=True) 


# In[101]:


videos_per_month.sort_index()


# In[102]:


ax2 = sns.barplot(x='Month',y='size',data =videos_per_month)


# In[104]:


video_data.to_csv('Video_Details(Enes Yilmazer).csv')


# In[ ]:




