from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
extractor=URLExtract()
def fetch_stats(selected_user,df):
    if selected_user!="Overall":
        df=df[df['user']==selected_user]

    num_messages=df.shape[0]
    words=[]
    for messages in df['message']:
        words.extend(messages.split())
    nums_media=df[df['message']=='<Media omitted>\n'].shape[0]

    # extract.find_urls => is a function which exctract url
    link=[]

    for message in df['message']:
        link.extend(extractor.find_urls(message))
    return    num_messages,len(words),nums_media,len(link)

def fetch_most_busy_user(df):
    x=df['user'].value_counts().head()
    new_df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name' ,'user':'percentage'})
    return x ,new_df

def  create_wordcloud(selected_user,df):
    f=open('stop_hinglish.txt')
    stop_words=f.read()
    if selected_user!="Overall":
        df=df[df['user']==selected_user]
    temp = df[df['user'] != 'group notification']
    temp =temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'null\n']
    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc=wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def most_common_word(df,selected_user):
    f = open('stop_hinglish.txt')
    stop_words = f.read()
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group notification']
    temp = df[df['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'null\n']
    words=[]
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df=pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

#emogji Analysis
def emoji_helper(selected_user,df):
    emojis=[]
    if(selected_user!='Overall'):
        df=df[df['user']==selected_user]

    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

#Monthly Analysis
def monthly_analysis(df,selected_user):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time=[]
    for i in range(timeline.shape[0]) :
        time.append(timeline['month'][i]+'-'+str(timeline['year'][i]))
    timeline['time']=time
    return timeline

#Daily Timeline
def daily_timeline(df,selected_user):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    daily_timeline=df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    weekly_activity_df=df['day_name'].value_counts()
    return weekly_activity_df

def monthly_activity_map(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    monthly_activity_df=df['month'].value_counts()
    return monthly_activity_df

def user_heat_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap=df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return user_heatmap