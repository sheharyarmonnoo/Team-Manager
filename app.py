import streamlit_authenticator as stauth, streamlit as st, plotly.express as px
import sys,  pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid
from streamlit_option_menu import option_menu
import datetime
import regex as re , calendar



sys.tracebacklimit = 0

def convert_df(x):
   return x.to_csv(index=False).encode('utf-8')

# Create a new thread

st.set_page_config(page_title= 'Team Manager',page_icon = "",layout="wide")
hide_st_style = """ <style>                  
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    header {visibility: hidden;} 
                    </style> """
                    
st.markdown(hide_st_style, unsafe_allow_html=True)

Warning = False   



with open("styles.css") as f:
    sidebar_collapse_design = st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
    


def collect_data():
    
    submission_date = datetime.datetime.now().date()
        
    date_contact = st.date_input("Date of contacting Lance Gooden's office")
    
    letters_written = st.number_input("How many letters have you written to Lance Gooden?", min_value=0)
    
    staff_contacted = st.text_input("Who on his staff have you contacted?")
    
    calls_made = st.number_input("How many calls have you made?", min_value=0)
    
    calls_picked_up =  st.number_input("How many calls were answered?", min_value=0)    
    
    emails_sent = st.number_input("How many emails have you sent?", min_value=0)
    
    emails_responded = st.number_input("How many emails were responded to?", min_value=0)    
    
    meetings_attended = st.number_input("How many group meetings have you attended?", min_value=0)
    
    notes = st.text_area("Notes")
    
    future_plan = st.text_area("Future Action Plan")
    
    submitter = st.button('Submit')
    
    

        
    if submitter: 
             
            data = {'User':main_name , 'Submission_Date': submission_date , 'Contact_Date' : date_contact,
            'staff_contacted': staff_contacted, 'letters_written': letters_written,
            'calls_made': calls_made, 'calls_picked_up': calls_picked_up, 
            'emails_sent': emails_sent, 'emails_responded': emails_responded, 
            'meetings_attended': meetings_attended, 'notes': notes, 'future_plan': future_plan}
            

            messages_df = pd.read_csv('messages.csv')
            
            messages_df = messages_df.append(data, ignore_index=True)
        
            messages_df.to_csv('messages.csv', index=False)
        
            st.success("Message posted!")
                        
def box_grid(x,ch):
    
    
        gb = GridOptionsBuilder.from_dataframe(x)
        gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
        gb.configure_side_bar() #Add a sidebar
        gb.configure_selection('single', use_checkbox=False
                                , groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
        
        gb.configure_default_column(groupable=True, 
                            value=True, 
                            enableRowGroup=True, 
                            editable=True,
                            enableRangeSelection=True,
                            filterable=True
                        )
        
        
        gridOptions = gb.build()
        
 
      
        
        grid_response = AgGrid( x,      gridOptions=gridOptions,                data_return_mode='AS_INPUT',
                                        fit_columns_on_grid_load=True,    enable_enterprise_modules=False,        
                            height=700,            width='100%')    
        return grid_response              

@st.cache
def get_analytics_user():
            
    
    x_name = 'User'    
    
    data = messages_df[x_name].value_counts()

    state_total_graph = px.bar(
    data

    )

    state_total_graph.update_layout(title = "Submissions by Users",
        template = GRAPH_TEMPLATE, xaxis_title = '', 
        
        yaxis = dict(
        tickmode = 'linear',
        tick0 = 1,
        dtick = 1),
        
        yaxis_title = '', width = GRAPH_WITHD, height = GRAPH_HEIGHT, 
        annotations = [dict(xref='paper',
        yref='paper',
        x=-0.04, y=-0.15,
        showarrow=False,
        
        text ='')] )

    
    state_total_graph.update(layout_showlegend=False)
    state_total_graph.update_layout(legend=dict(title=""))


        
    
    state_total_graph.update_traces(width=0.1)
    
    return state_total_graph   

@st.cache
def get_analytics_month():
            
    
    x_name = 'Submission_Date'    
    
    # data = messages_df[x_name].value_counts()

    messages_df['period'] = pd.to_datetime(messages_df[x_name]).dt.strftime('%Y%m')    
    messages_df['month'] = pd.DatetimeIndex(messages_df[x_name]).month
    
    
    messages_df['month'] = messages_df['month'].apply(lambda x : calendar.month_name[int(x)])
    # messages_df['month'] = str(messages_df['month']) + "-" + str(messages_df['year'])

    
    
    state_total = messages_df.groupby(['month','period'],as_index=False)[x_name].count().sort_values(by = 'period')
    
    

    state_total_graph = px.bar(
    state_total , x = 'month' , y = x_name

    )

    state_total_graph.update_layout(title = "Submissions by Month",
        template = GRAPH_TEMPLATE, xaxis_title = '', 
        
        yaxis = dict(
        tickmode = 'linear',
        tick0 = 1,
        dtick = 1),
        
        yaxis_title = '', width = GRAPH_WITHD, height = GRAPH_HEIGHT, 
        annotations = [dict(xref='paper',
        yref='paper',
        x=-0.04, y=-0.15,
        showarrow=False,
        
        text ='')] )

    
    state_total_graph.update(layout_showlegend=False)
    state_total_graph.update_layout(legend=dict(title=""))


        
    
    state_total_graph.update_traces(width=0.1)
    
    return state_total_graph   



def main():
    
    

    if main_name == 'Sidd':
        grid_opt =  [ 'Member History','Activity','Submissions','Update History','Admin Analytics']
        
    else:
        grid_opt = [ 'Member History','Activity','Submissions']
    
    with st.sidebar:
        
        _ , col_2 = st.columns([.2,1])
        with col_2:
                 st.write(f"Logged in as : {main_name}")
        
        choice = option_menu(
            menu_title = 'Navigation',
            menu_icon = ' ',
            # icons = ['broadcast-pin', 'unlock', 'umbrella'],
            options = grid_opt,
            styles = {
                "container": {"padding": "5px"},
                "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px"},
                "nav-link-selected": {"background-color": "#323130"}
                
                } )
        authenticator.logout("Logout")

    if choice == 'Member History':        
        st.subheader('Legal History')
                        
        alpha = st.container()
        

                    
        with alpha:                    
            col_1_alpha , col_2 = st.columns([9,2])
            

            
            with col_2:
                st.download_button( "Export to CSV",   csv_status,   "ALL_Deals.csv",   "text/csv",   key='download-csv')                                 
        
        
        chart_data = DF_STATUS[['Date','Member','Status', 'Vote','Period','Bill Title','Refresh Time']]\
            .sort_values(by=['Date'],ascending=False)
        
        gr = box_grid(chart_data, ch = 2)

    if choice == 'Activity':     
         
        
        st.title('Activity')
        
        collect_data()    
    
    if choice == 'Submissions':  
        
        st.subheader('Submissions')
                        
        alpha = st.container()
        

                    
        with alpha:                    
            _ , col_2 = st.columns([9,2])
            

            
            with col_2:
                st.download_button( "Export to CSV",   csv_status,   "ALL_Deals.csv",   "text/csv",   key='download-csv')                                 
        
        chart_data = messages_df[['Submission_Date','Contact_Date','User','staff_contacted','meetings_attended']]\
            .sort_values(by=['Submission_Date'],ascending=False).rename({'staff_contacted':'Staff Contacted', 'meetings_attended': 'Meetings Attended'},axis = 1)
        
        gr = box_grid(chart_data, ch = 0)
    
    if choice == 'Update History':
        
        a , _  = st.columns([1,3])
        
        with a:
        
            names = {'G000589':'Lance Gooden'}
            
            st.write('Current members on file: \n', names)                   
            
            upd = st.button('Run Refresh')
            
            if upd:
                
                with st.spinner():
                    try:                          
                        
                        data = pd.DataFrame()                    
                        for memberID in names:
                            for page in range(1,5): # Number of Pages to scrape
                                hldr = pd.read_html(f'https://clerk.house.gov/members/ViewRecentVotes?memberID={memberID}&Page={page}')[0]
                                hldr['Period'] = pd.to_datetime(hldr['Date']).dt.strftime('%Y%m')
                                hldr['Date'] = pd.to_datetime(hldr['Date'])        
                                hldr['Refresh Time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")      
                                data = data.append(hldr)
                                data['Member'] = names[memberID]
                                data.to_csv('Leg.csv',index=False)
                                
                        st.success("Refresh Success!")
                    except:
                        st.error("Refresh Failed!")
                    
    if choice == 'Admin Analytics':
        
        st.plotly_chart(get_analytics_user())
        
        st.plotly_chart(get_analytics_month())
        
        
GRAPH_WITHD = 1000
GRAPH_HEIGHT = 600
GRAPH_TEMPLATE = 'simple_white'


DF_STATUS = pd.read_csv('Leg.csv')
DF_STATUS['Bill Title'] = DF_STATUS['Bill Title'].apply(lambda x :  re.sub(r'[^a-zA-Z0-9]',' ', str(x)) if pd.isna(x) != True else "-")
DF_STATUS['BillNumber'] = DF_STATUS['BillNumber'].apply(lambda x :  re.sub(r'[^a-zA-Z0-9]',' ', str(x)) if pd.isna(x) != True else "-")

csv_status  = convert_df(DF_STATUS)

messages_df = pd.read_csv('messages.csv')

users_df = pd.read_csv('users.csv')

USERNAMES = users_df['user_name'].values.tolist()
NAMES = users_df['user'].values.tolist()
HASHED_PASSWORDS = stauth.Hasher(users_df['pass_code'].values.tolist()).generate()

# NAMES = [USERS['user'][0] for USERS in users_df]
# HASHED_PASSWORDS = [USERS['pass_code'][0] for USERS in users_df]

authenticator = stauth.Authenticate(NAMES,USERNAMES,HASHED_PASSWORDS,"Team Manager",'codass',cookie_expiry_days = 1)

main_name , authentication_status, username = authenticator.login("Team Manager","main")

if authentication_status == False:
    st.error("Username/Password is incorrect")

elif authentication_status:
    main()