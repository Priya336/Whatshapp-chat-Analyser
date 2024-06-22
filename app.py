import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

(st.sidebar.title("Whatsapp Chat Analyser"))
uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)


    #fetch unique user
    user_list=df['user'].unique().tolist()
    if user_list.count('group_notification')>0:
      user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("Show analysis wrt" ,user_list)
    if  st.sidebar.button("Show Analysis"):
        num_messages,words,num_media,num_link=helper.fetch_stats(selected_user,df)
        st.title('Top Statistics')
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media)
        with col4:
            st.header("Link Shared")
            st.title(num_link)

# Monthly timeline
        st.title('Monthly Timeline')
        timeline=helper.monthly_analysis(df,selected_user)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
#daily Timeline
        st.title('Daily Timeline')
        daily_df=helper.daily_timeline(df,selected_user)
        fig, ax = plt.subplots()
        ax.plot(daily_df['only_date'], daily_df['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        col1,col2=st.columns(2)

#activity map
        with col1:
           st.title("Weekly Activity Map")
           weekly_activity_df=helper.week_activity_map(selected_user,df)
           fig,ax=plt.subplots()
           ax.bar(weekly_activity_df.index,weekly_activity_df.values)
           plt.xticks(rotation='vertical')
           st.pyplot(fig)

        # Monthly_activity map
        with col2:
           st.title(" Monthly Activity Map")
           monthly_activity_df = helper.monthly_activity_map(selected_user, df)
           fig, ax = plt.subplots()
           ax.bar(monthly_activity_df.index, monthly_activity_df.values,color='orange')
           plt.xticks(rotation='vertical')
           st.pyplot(fig)

        if selected_user=="Overall":
            st.title("Most Busy User")
            x,new_df=helper.fetch_most_busy_user(df)
            fig,ax=plt.subplots()
            col1,col2=st.columns(2)
            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
              x=(x/df.shape[0])*100
              st.dataframe(new_df)


        #Word Cloud
        st.header('Word Cloud')
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        st.title("Most Common Word")
        most_common_df=helper.most_common_word(df,selected_user)
        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        #emoji analysis
        st.title('Emoji Count')
        emoji_df = helper.emoji_helper(selected_user, df)
        st.dataframe(emoji_df)

        #heatMap
        st.title("Weekly Heat Map")
        user_heatmap=helper.user_heat_map(selected_user,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)