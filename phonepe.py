import streamlit as st
import plotly.express as plt
import pandas as pd
import pymysql
from streamlit_option_menu import option_menu
import json

#sql connectivity:
myconnection=pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='Naveenk02',
                             database='phonepeproject')
cur=myconnection.cursor()


#set page congiguration
st.set_page_config(page_title="Phonepe Pulse Data Visualization and Exploration",
                   layout= "wide",
                   initial_sidebar_state= "expanded")

st.sidebar.header(":violet[Phonepe_Pulse]")
with st.sidebar:
    selected = option_menu("Menu", ["Home","Explore Data"], 
                    icons=["house","bar-chart-line", "exclamation-circle"],
                    menu_icon= "menu-button-wide",
                    default_index=0,
                    styles={"nav-link": {"font-size": "13px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                            "nav-link-selected": {"background-color": "#6F36AD"}})   


#Home Page
if selected=='Home':
    st.title(":violet[Phonepe Pulse Data Visualization and Exploration]")
    st.markdown("## :violet[DOMAIN]: Fintech")
    st.markdown("## :violet[Technologies used]: Google colab,Jupyter Notebook, Mysql, matplot these are the technologies are used in this peoject")
    st.markdown("## :violet[Overview] : In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on.")

#Explore Data
if selected=="Explore Data":
    #st.sidebar.header(":violet[Choose it]")
    add_sidebar=st.sidebar.selectbox(":violet[**Select Page**]",options=['Top 10 of State and District','Geo Visualization','Bar chat Visualization'])
    if add_sidebar=='Top 10 of State and District':
        st.markdown("#### :violet[Explore Data]")
        col1, col2 = st.columns([1,1],gap="large")
        with col1:
            Type=st.selectbox(":violet[**Select Type**]",("Transaction","Users"))
            Year=st.selectbox(":violet[**Select Year**]",options=['2018','2019','2020','2021','2022'] )
            Quarter=st.selectbox(":violet[**Select Quarter**]",options=['1','2','3','4'])

            #Transaction in Explore Data
            if Type=="Transaction":
                st.markdown("### :violet[**Top 10 State**]")
                st.write(":violet[Overall top 10 state,Transcation amount and Transaction count]")
                sql1='Select State, sum(Transaction_count) , sum(Transaction_amount) from agg_trans where Year= {} and Quarter= {} group by State order by 3 desc limit 10'.format(Year,Quarter)
                df=cur.execute(sql1)
                df2=cur.fetchall()
                a=pd.DataFrame(df2,index=[1,2,3,4,5,6,7,8,9,10],columns=['State','Transaction_count','Transaction_amount'])
                st.write(a)
                st.markdown(":violet[**Here you  can see the charts for State stats**]")
                fig = plt.pie(a, values='Transaction_amount',
                                names='State',
                                title=('Top 10 Over all Transaction amount state'),
                                color_discrete_sequence=plt.colors.sequential.Agsunset,
                                #color_discrete_sequence=px.colors.sequential.Purples,
                                hover_data=['Transaction_count'],
                                labels={'Transactions_count':'Transactions_count'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)
        
        with col2:
            if Type=="Transaction":
                st.markdown("### ")
                st.markdown("### ")
                st.markdown("### ")
                st.markdown("### ")
                st.markdown("### ")
                st.markdown("### ")
                st.markdown("### ")
                st.markdown("### ")
                st.markdown("### ")
                st.markdown("### ")
                st.markdown("### :violet[Top 10 District]")
                st.write(":violet[Overall top 10 District,Transcation amount and Transaction count]")
                sql2='select District,sum(Transaction_count),sum(Transaction_amount) from map_trans where Year={} and Quarter={} group by District order by 3 desc limit 10'.format(Year,Quarter)
                df3=cur.execute(sql2)
                df4=cur.fetchall()
                a1=pd.DataFrame(df4,index=[1,2,3,4,5,6,7,8,9,10],columns=['District','Transaction_count','Transaction_amount'])
                st.write(a1)
                st.markdown(":violet[**Here you  can see the charts for District stats**]")
                fig = plt.pie(a1, values='Transaction_amount',
                                names='District',
                                title=('Top 10 Over all Transaction amount District'),
                                #color_discrete_sequence=plt.colors.sequential.Agsunset,
                                #color_discrete_sequence=plt.colors.sequential.Purples,
                                color_discrete_sequence=plt.colors.sequential.Viridis,
                                hover_data=['Transaction_count'],
                                labels={'Transactions_count':'Transactions_count'})
                
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)
            
            #User Type in Explore Data
            if Type=='Users':
                with col1:
                    st.markdown("### :violet[Top 10 Brands and Counts]")
                    sql3='select Brands,round(sum(count),1) as Total_count from agg_user where Year={} and Quarter= {} group by (brands) order by 2 desc limit 10;'.format(Year,Quarter)
                    df5=cur.execute(sql3)
                    df6=cur.fetchall()
                    b=pd.DataFrame(df6,index=[1,2,3,4,5,6,7,8,9,10],columns=['Brands','Total_count'])
                    st.write(b)
                    fig = plt.bar(b,
                                title='Top 10 Brands and Counts ',
                                y="Brands",
                                x="Total_count",
                                orientation='h',
                                color='Total_count',
                                color_continuous_scale=plt.colors.sequential.Agsunset)
                    st.plotly_chart(fig,use_container_width=True)   
                with col2:
                    st.markdown("##### :violet[Note:]")
                    st.markdown("##### Here you can see the usage of :violet[Phonepe] by Top 10 brands and Top 10 State followed by RegisterUsers")
                    st.markdown("##### If you choose :violet[Year] is 2022 and :violet[Quarter] in 2,3,4 Top 10 Brands and Counts :violet[(display no data)] because no records are found in these circumstance")
                    st.markdown("### ")
                    st.markdown("### ")
                    st.markdown("### :violet[Top 10 State and RegisterUsers]")
                    sql4="select State,sum(RegisteredUsers)  from top_user where Year= {} and Quarter = {} group by State order by 2 desc limit 10;".format(Year,Quarter)
                    df7=cur.execute(sql4)
                    df8=cur.fetchall()
                    b1=pd.DataFrame(df8,index=[1,2,3,4,5,6,7,8,9,10],columns=['State','RegisteredUsers'])
                    st.write(b1)
                    fig = plt.bar(b1,
                                title='Top 10 State and RegisterdUsers ',
                                y='State',
                                x='RegisteredUsers',
                                orientation='h',
                                color='RegisteredUsers',
                                color_continuous_scale=plt.colors.sequential.Agsunset)
                    st.plotly_chart(fig,use_container_width=True)
    

    #Geo Visualization :

    if add_sidebar=='Geo Visualization':
        st.subheader(' :violet[Geo Visualization]',divider='violet')

        Type=st.selectbox(":violet[**Select Type**]",("Transaction","Users"))
        Year=st.selectbox(":violet[**Select Year**]",options=['2018','2019','2020','2021','2022'] )
        Quarter=st.selectbox(":violet[**Select Quarter**]",options=['1','2','3','4'])

        #Geo Visualization in Transaction

        if Type=='Transaction':
            st.markdown("### :violet[Geo Visualization of Total amount by State]")
            cur.execute("select State,round(sum(Transaction_amount),1) as Total_amount,sum(Transaction_count) as Total_count from map_trans where Year={} and Quarter={} group by State order by State".format(Year,Quarter))
            dff2=pd.DataFrame(cur.fetchall(),columns=['State','Total_amount','Total_count'])
            states=[]
            with open('state.json','r') as file:     #read the json file and then load after the extract that and store in a states
                data=json.load(file)
            for i in data['features']:
                states.append(i['properties']['ST_NM']) 
            dff2.State=states

            fig = plt.choropleth(dff2,
                                geojson='https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson',
                                featureidkey='properties.ST_NM',
                                locations='State',
                                color='Total_amount',
                                color_continuous_scale='reds')
                                
            fig.update_geos(fitbounds="locations", visible = True)
            st.plotly_chart(fig,use_container_width=True)

        #Geo visualization in Users
   
        if Type=='Users':
            st.markdown("### :violet[Geo Visualization of Total user by state]")
            cur.execute("select State,sum(RegisteredUser) as Total_user from map_user where Year= {} and Quarter= {} group by State order by State".format(Year,Quarter))
            dff4=pd.DataFrame(cur.fetchall(),columns=['State','Total_user'])
            
            #Extract the states names from the json file
            states=[]
            with open('state.json','r') as file:
                data=json.load(file)
            for i in data['features']:
                states.append(i['properties']['ST_NM']) 
            dff4.State=states
            
            fig = plt.choropleth(dff4,
                                geojson='https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson',
                                featureidkey='properties.ST_NM',
                                locations='State',
                                color='Total_user',
                                color_continuous_scale='reds')
                                
            fig.update_geos(fitbounds="locations", visible = True)
            st.plotly_chart(fig,use_container_width=True)
    
    #Bar chat Visualization

    if add_sidebar=='Bar chat Visualization':
        st.subheader(":violet[Bar chat Visualization]",divider='violet')
        Type=st.selectbox(":violet[**Select Type**]",("Transaction","Users"))
        Year=st.selectbox(":violet[**Select Year**]",options=['2018','2019','2020','2021','2022'] )
        Quarter=st.selectbox(":violet[**Select Quarter**]",options=['1','2','3','4'])
        
        states = st.selectbox(':violet[**Choose State:**]',options=('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                                                                    'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                                                                    'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                                                                    'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                                                                    'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                                                                    'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'))
        
        #Transaction type in bar chat

        if Type=='Transaction':
            sql5=f'select State,District,Year,Quarter,sum(Transaction_count) as Total_count,sum(Transaction_amount) as Total_amount from map_trans where Year= {Year} and Quarter={Quarter} and State= "{states}" group by State,District,Year,Quarter order by State,District'
            cur.execute(sql5)
            dff1=pd.DataFrame(cur.fetchall(),columns=['State','District','Year','Quarter','Total_count','Total_amount'])
            st.markdown("### :violet[State with District wise Transaction amount]")

            fig = plt.bar(dff1,
                        title=states,
                        x="District",
                        y="Total_amount",
                        orientation='v',
                        color='Total_amount',
                        color_continuous_scale=plt.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)

            sql6=f'select State,Year,Quarter,Transaction_type,sum(Transaction_count) as Total_count from agg_trans where Year= {Year} and Quarter= {Quarter} and State= "{states}" group by State,Transaction_type order by State,Year,Quarter,Transaction_type'
            cur.execute(sql6)
            dff2=pd.DataFrame(cur.fetchall(),columns=['State','Year','Quarter','Transaction_type','Total_count'])
            
            st.markdown("### :violet[State with Transaction Type and its count]")
            fig=plt.bar(dff2,
                        title=states,
                        x="Transaction_type",
                        y="Total_count",
                        orientation='v',
                        color='Total_count',
                        color_continuous_scale=plt.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)

        #User type in bar chat
        if Type=='Users':
            sql7=f'select State,Year,Quarter,District,sum(RegisteredUser) as Total_Registration from map_user where Year= {Year} and Quarter= {Quarter} and State= "{states}" group by State,District,Year,Quarter order by State,District;'
            cur.execute(sql7)
            dff3=pd.DataFrame(cur.fetchall(),columns=['State','Year','Quarter','District','Total_Registration'])
            st.markdown("### :violet[State with District wise Total Registration]")
            
            fig=plt.bar(dff3,
                        title=states,
                        x='District',
                        y='Total_Registration',
                        orientation='v',
                        color='Total_Registration',
                        color_continuous_scale=plt.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)





                
                


        

                        
                



                

                
                


    

    

        

    
                            


    

    



