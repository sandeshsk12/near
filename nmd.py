import streamlit as st 
# import seaborn as sns
import plotly.express as px
import pandas as pd
from datetime import datetime as dt
import matplotlib.pyplot as plt
import time
from plotly.subplots import make_subplots
import numpy as np 
from urllib.request import urlopen 
import json
import requests
from PIL import  Image
import plotly.graph_objects as go
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import udf
import numpy as np 
import streamlit.components.v1 as components


st.set_page_config(page_title="Near marketing DAO", layout="wide",initial_sidebar_state="collapsed")

st.markdown('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">',unsafe_allow_html=True)

with st.spinner(text='loading'):
    time.sleep(15)

c1,c2=st.columns((20,80))
c1.image('2023-02-01_23-43.png',use_column_width=True)
c2.markdown(f"""
<div style='text-align: center'>
<div class="card text-white bg-danger mb-3" >

  <div class="card-header"> <h2> <br> Near MarketingDAO Dash <br></h2></div>    
    <p class="card-text"></p>
  </div>
  </div>
""", unsafe_allow_html=True)

Overview, dashboard_in_depth, proposal_info_tab, writeup, takeaways, recommendation  = st.tabs(['**Overview**','**In-Depth dashboard**','**Proposal information**','**Writeup**','**Takeaways**','**Recommendation**'])

with Overview:
    
    ###### Distribution of proposals
    proposal_info = "https://node-api.flipsidecrypto.com/api/v2/queries/a3e4a5eb-bc71-4589-8ac9-d98f1c425cef/data/latest"
    proposal_info = pd.read_json(proposal_info)
    # st.dataframe(prop_pass[['PROPOSAL_SUBMITTED','PROPOSER','PROPOSAL_ID','PROPOSAL','PROPOSAL_URL','OUTCOME']])
    # c1,c2=st.columns(2)
    prop_info_pass_fail_dist_fig=px.pie(proposal_info.groupby(by='OUTCOME',as_index=False).count(),names='OUTCOME',values='PROPOSAL_ID',color_discrete_sequence=["blue", "red", "green", "goldenrod", "magenta"])
    prop_info_pass_fail_dist_fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(235,235,235,255)',})
    prop_info_pass_fail_dist_fig.update_layout(        
        width=600,
        height=400,)
    prop_info_pass_fail_dist_fig.update_layout(
        title="<a href='https://app.flipsidecrypto.com/velocity/queries/a3e4a5eb-bc71-4589-8ac9-d98f1c425cef'>Distribution of proposals</a>",
        # xaxis_title="Date",
        # yaxis_title="USD",
        # legend_title="",
        font=dict(
            # family="Courier New, monospace",
            size=18,
            color="black"
        ))
    prop_info_pass_fail_dist_fig.update_traces(hoverinfo='label+percent', textinfo='percent+value', textfont_size=20)
    #c1.plotly_chart(prop_info_pass_fail_dist_fig, use_container_width=True)


    proposal_info_for_pay = "https://node-api.flipsidecrypto.com/api/v2/queries/4c233639-4cdb-486c-af11-3ea18d365086/data/latest"
    proposal_info_for_pay = pd.read_json(proposal_info_for_pay)
    proposal_info_for_pay['target']=proposal_info_for_pay['PROPOSAL'].apply(udf.find_target)
    proposal_info_for_pay['target'].fillna(proposal_info_for_pay['PROPOSER'],inplace=True)

    prop_passed_time="https://node-api.flipsidecrypto.com/api/v2/queries/e9905d70-6870-44dd-aa32-8c6e7f32476f/data/latest"
    prop_passed_time=pd.read_json(prop_passed_time)
    prop_passed_time_with_info=pd.merge(proposal_info_for_pay,prop_passed_time, on='PROPOSAL_ID', how='left')
    prop_passed_time_with_info=prop_passed_time_with_info.rename(columns = {'BLOCK_TIMESTAMP':'Proposed_time','TX_HASH':'proposal_txn_hash'})

    usd_pay_proposals="https://node-api.flipsidecrypto.com/api/v2/queries/38932b59-1ed3-4ebe-bbbe-5d1600c9b1c2/data/latest"
    usd_pay_proposals = pd.read_json(usd_pay_proposals)
    usd_pay_proposals=usd_pay_proposals.rename(columns = {'BLOCK_TIMESTAMP':'payment_timestamp','TX_HASH':'payment_txn_hash','TX_RECEIVER':'Assest'})

    near_pay_proposals="https://node-api.flipsidecrypto.com/api/v2/queries/975c569b-eae7-47ec-a1bf-eae7b21e60a6/data/latest"
    near_pay_proposals = pd.read_json(near_pay_proposals)
    near_pay_proposals=near_pay_proposals.rename(columns = {'BLOCK_TIMESTAMP':'payment_timestamp','TX_HASH':'payment_txn_hash','TX_RECEIVER':'Assest'})
    pay=pd.concat([near_pay_proposals,usd_pay_proposals])
    pay['payment_timestamp'] = pd.to_datetime(pay['payment_timestamp'])
    prop_passed_time_with_info['Proposed_time'] = pd.to_datetime(prop_passed_time_with_info['Proposed_time'])
    pay.sort_index(inplace=True)
    prop_passed_time_with_info.sort_index(inplace=True)
    pass_prop_time_and_pay=pd.merge(prop_passed_time_with_info,pay,how='inner', left_on='target',right_on='RECEIVER' )
    pass_prop_time_and_pay['diff_days'] = (pass_prop_time_and_pay['payment_timestamp'] - pass_prop_time_and_pay['Proposed_time']) / np.timedelta64(1, 'D')
    payments=pass_prop_time_and_pay[(pass_prop_time_and_pay['diff_days'] < 60) & (pass_prop_time_and_pay['diff_days'] >0) & (pass_prop_time_and_pay['AMOUNT']<40000)]
    payments['payment_timestamp']=pd.to_datetime(payments['payment_timestamp'])
    payments_paid=payments.resample('M', on='payment_timestamp').sum()
    payment_trend_fig=px.bar(payments_paid,x=payments_paid.index,y='AMOUNT',color_discrete_sequence=["blue", "red", "green", "goldenrod", "magenta"])
    payment_trend_fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(235,235,235,255)',})
    payment_trend_fig.update_layout(        
        width=600,
        height=400,)
    payment_trend_fig.update_layout(
        title="<a href='https://app.flipsidecrypto.com/velocity/queries/38932b59-1ed3-4ebe-bbbe-5d1600c9b1c2'>Payments issued</a>",
        xaxis_title="Date",
        yaxis_title="USD",
        # legend_title="",
        font=dict(
            # family="Courier New, monospace",
            size=18,
            color="black"
        ))
    # c2.plotly_chart(payment_trend_fig, use_container_width=True)

    top_target_wallets=payments.groupby(by='target',as_index=False).sum()
    top_target_wallets.sort_values(by='AMOUNT',ascending=False,inplace=True)
    # top_target_wallets.head(5)
    top_target_wallets_fig=px.bar(top_target_wallets.head(5),x='target',y='AMOUNT',color_discrete_sequence=["blue", "red", "green", "goldenrod", "magenta"])
    top_target_wallets_fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(235,235,235,255)',})
    top_target_wallets_fig.update_layout(        
        width=600,
        height=500,)
    top_target_wallets_fig.update_layout(
        title="<a href='https://app.flipsidecrypto.com/velocity/queries/975c569b-eae7-47ec-a1bf-eae7b21e60a6'>Top target wallets</a>",
        xaxis_title="Date",
        yaxis_title="USD",
        # legend_title="",
        font=dict(
            # family="Courier New, monospace",
            size=18,
            color="black"
        ))
    # c1.plotly_chart(top_target_wallets_fig, use_container_width=True)

    voters_heatmap="https://node-api.flipsidecrypto.com/api/v2/queries/f62545cc-ee0f-4bc3-bb97-2124782bfdd2/data/latest"
    voters_heatmap=pd.read_json(voters_heatmap)
    top_voters=voters_heatmap.groupby(by='VOTER',as_index=False).sum()
    top_voters=top_voters.sort_values(by='NUMBER_OF_VOTES',ascending=False)
    top_voters_pivot_table=voters_heatmap.pivot(index='MONTH',columns='VOTER',values='NUMBER_OF_VOTES')
    top_voters_pivot_table = top_voters_pivot_table.reindex(columns=top_voters['VOTER'].tolist())
    top_voters_heatmap=px.imshow(top_voters_pivot_table.transpose(),text_auto=True,color_continuous_scale=px.colors.sequential.Viridis)
    top_voters_heatmap.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(235,235,235,255)',})
    top_voters_heatmap.update_layout(        
        width=600,
        height=500,)
    top_voters_heatmap.update_layout(
        title="<a href='https://app.flipsidecrypto.com/velocity/queries/f62545cc-ee0f-4bc3-bb97-2124782bfdd2''>Top voters</a>",
        # xaxis_title="Date",
        # yaxis_title="USD",
        # legend_title="",
        font=dict(
            # family="Courier New, monospace",
            size=18,
            color="black"
        ))
    # c2.plotly_chart(top_voters_heatmap, use_container_width=True)

    c1,c2,c3,c4=st.columns(4)
    number_of_approved_props=proposal_info.groupby(by='OUTCOME',as_index=True).count()
    fig = go.Figure(go.Indicator(
        mode = "number",
        value = int(number_of_approved_props.loc['Approved']['TX_HASH']),
        # delta=1,
        # number = {'prefix': "$"},
        title="Approved proposals",
        # delta = {'position': "bottom", 'reference': round(float(dao_twitter['Followers'][1]),3)},
        domain = {'x': [0, 1], 'y': [0, 1]}))
    fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(215,215,215,255)',})
    fig.update_layout(font=dict(
            # family="Courier New, monospace",
            # size=18,
            color="black"
        ))
    fig.update_layout(height=260, width=600)
    c1.plotly_chart(fig,use_container_width=True)

    fig = go.Figure(go.Indicator(
        mode = "number",
        value = int(payments_paid[['AMOUNT']].sum().values[0]),
        # delta=1,
        number = {'prefix': "$"},
        title="Amount Disbursed",
        # delta = {'position': "bottom", 'reference': round(float(dao_twitter['Followers'][1]),3)},
        domain = {'x': [0, 1], 'y': [0, 1]}))
    fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(215,215,215,255)',})
    fig.update_layout(height=260, width=600)
    fig.update_layout(font=dict(
            # family="Courier New, monospace",
            # size=18,
            color="black"
        ))
    c2.plotly_chart(fig,use_container_width=True)

    fig = go.Figure(go.Indicator(
        mode = "number",
        value = int(top_target_wallets.shape[0]),
        # delta=1,
        # number = {'prefix': "$"},
        title="Number of target wallets",
        # delta = {'position': "bottom", 'reference': round(float(dao_twitter['Followers'][1]),3)},
        domain = {'x': [0, 1], 'y': [0, 1]}))
    fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(215,215,215,255)',})
    fig.update_layout(height=260, width=600)
    fig.update_layout(font=dict(
            # family="Courier New, monospace",
            # size=18,
            color="black"
        ))
    c3.plotly_chart(fig,use_container_width=True)

    fig = go.Figure(go.Indicator(
        mode = "number",
        value = int(5),
        # delta=1,
        # number = {'prefix': "$"},
        title="Number of Active council members",
        # delta = {'position': "bottom", 'reference': round(float(dao_twitter['Followers'][1]),3)},
        domain = {'x': [0, 1], 'y': [0, 1]}))
    fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(215,215,215,255)',})
    fig.update_layout(height=260, width=600)
    fig.update_layout(font=dict(
            # family="Courier New, monospace",
            # size=18,
            color="black"
        ))
    c4.plotly_chart(fig,use_container_width=True)


    
    c1,c2=st.columns(2)
    c1.plotly_chart(prop_info_pass_fail_dist_fig, use_container_width=True)
    c2.plotly_chart(payment_trend_fig, use_container_width=True)
    c1.plotly_chart(top_target_wallets_fig, use_container_width=True)
    c2.plotly_chart(top_voters_heatmap, use_container_width=True)

with proposal_info_tab:
    c1,c2,c3=st.columns((20,60,20))
    input_prop_id=c2.number_input(label='Enter proposal ID',min_value=0,value=500)
    # st.write(input_prop_id)
    prop_pass = "https://node-api.flipsidecrypto.com/api/v2/queries/a3e4a5eb-bc71-4589-8ac9-d98f1c425cef/data/latest"
    prop_pass = pd.read_json(prop_pass)
    prop_pass['target']=prop_pass['PROPOSAL'].apply(udf.find_target)
    prop_pass['target'].fillna(prop_pass['PROPOSER'],inplace=True)
    passed_time="https://node-api.flipsidecrypto.com/api/v2/queries/e9905d70-6870-44dd-aa32-8c6e7f32476f/data/latest"
    passed_time=pd.read_json(passed_time)
    prop_pass=pd.merge(prop_pass,passed_time, on='PROPOSAL_ID', how='left')
    prop_pass=prop_pass.rename(columns = {'BLOCK_TIMESTAMP':'Proposed_time','TX_HASH':'proposal_txn_hash'})
    

    # input_prop_id=500
    df=prop_pass[prop_pass['PROPOSAL_ID']==input_prop_id]
    c1,c2,c3,c4=st.columns(4)
    # fig = go.Figure(go.Indicator(
    #     mode = "number",
    #     # value = df['PROPOSAL_ID'].values[0],
    #     # delta=1,
    #     # number = {'prefix': "$"},
    #     title="Proposal ID : {}".format(df['PROPOSAL_ID'].values[0]),
    #     # delta = {'position': "bottom", 'reference': round(float(dao_twitter['Followers'][1]),3)},
    #     domain = {'x': [0, 1], 'y': [0, 1]}))
    # fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(215,215,215,255)',})
    # fig.update_layout(height=180, width=600)
    # c1.plotly_chart(fig,use_container_width=True)
    
    if df['OUTCOME'].values[0]=='Approved':
        c1.markdown(
            """
            <div class="card text-white bg-{} mb-5" >
        <div class="card-header"> Proposal ID </div>
        <div class="card-body">
            <h2 class="card-title">
            {}
            </h2>
            <p class="card-text"></p>
        </div>
        """.format('success',df['PROPOSAL_ID'].values[0]), unsafe_allow_html=True)
    elif df['OUTCOME'].values[0]=='Rejected':
        c1.markdown(
            """
            <div class="card text-white bg-{} mb-5" >
        <div class="card-header"> Proposal ID </div>
        <div class="card-body">
            <h2 class="card-title">
            {}
            </h2>
            <p class="card-text"></p>
        </div>
        """.format('danger',df['PROPOSAL_ID'].values[0]), unsafe_allow_html=True)
    else:
        c1.markdown(
            """
            <div class="card text-white bg-{} mb-5" >
        <div class="card-header"> Proposal ID </div>
        <div class="card-body">
            <h2 class="card-title">
            {}
            </h2>
            <p class="card-text"></p>
        </div>
        """.format('secondary',df['PROPOSAL_ID'].values[0]), unsafe_allow_html=True)


    if df['OUTCOME'].values[0]=='Approved':
        c4.markdown(
            """
            <div class="card text-white bg-{} mb-5" >
        <div class="card-header"> Status </div>
        <div class="card-body">
            <h2 class="card-title">
            {}
            </h2>
            <p class="card-text"></p>
        </div>
        """.format('success',df['OUTCOME'].values[0]), unsafe_allow_html=True)
    elif df['OUTCOME'].values[0]=='Rejected':
        c4.markdown(
            """
            <div class="card text-white bg-{} mb-5" >
        <div class="card-header"> Status </div>
        <div class="card-body">
            <h2 class="card-title">
            {}
            </h2>
            <p class="card-text"></p>
        </div>
        """.format('danger',df['OUTCOME'].values[0]), unsafe_allow_html=True)
    else:
        c4.markdown(
            """
            <div class="card text-white bg-{} mb-5" >
        <div class="card-header"> Status </div>
        <div class="card-body">
            <h2 class="card-title">
            {}
            </h2>
            <p class="card-text"></p>
        </div>
        """.format('secondary',df['OUTCOME'].values[0]), unsafe_allow_html=True)



    
    date_string = df['PROPOSAL_SUBMITTED'].values[0]
    date_format = '%Y-%m-%d'
    date_object = datetime.strptime(date_string, date_format)

    desired_format = '%B %d, %Y'
    formatted_date = date_object.strftime(desired_format)
    if df['OUTCOME'].values[0]=='Approved':
        c2.markdown(
            """
            <div class="card text-white bg-{} mb-5" >
        <div class="card-header"> Submission Date </div>
        <div class="card-body">
            <h2 class="card-title">
            {}
            </h2>
            <p class="card-text"></p>
        </div>
        """.format('success',formatted_date), unsafe_allow_html=True)
    elif df['OUTCOME'].values[0]=='Rejected':
        c2.markdown(
            """
            <div class="card text-white bg-{} mb-5" >
        <div class="card-header"> Submission Date </div>
        <div class="card-body">
            <h2 class="card-title">
            {}
            </h2>
            <p class="card-text"></p>
        </div>
        """.format('danger',formatted_date), unsafe_allow_html=True)
    else:
        c2.markdown(
            """
            <div class="card text-white bg-{} mb-5" >
        <div class="card-header"> Submission Date </div>
        <div class="card-body">
            <h2 class="card-title">
            {}
            </h2>
            <p class="card-text"></p>
        </div>
        """.format('secondary',formatted_date), unsafe_allow_html=True)


    # fig = go.Figure(go.Indicator(
    #     mode = "number",
    #     # value = df['PROPOSAL_ID'].values[0],
    #     # delta=1,
    #     # number = {'prefix': "$"},
    #     title="Proposal submitted on {}".format(formatted_date),
    #     # delta = {'position': "bottom", 'reference': round(float(dao_twitter['Followers'][1]),3)},
    #     domain = {'x': [0, 1], 'y': [0, 1]}))
    # fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(215,215,215,255)',})
    # fig.update_layout(height=160, width=600)
    # c2.plotly_chart(fig,use_container_width=True)
    # import datetime



    # date_string = df['PASSED_TIME'].values[0]
    # date_format = '%Y-%m-%d'
    # date_object = datetime.strptime(date_string, date_format)

    # desired_format = '%B %d, %Y'
    # formatted_date = date_object.strftime(desired_format)

    if df['OUTCOME'].values[0]=='Approved':
        c3.markdown(
            """
            <div class="card text-white bg-{} mb-5" >
        <div class="card-header"> Decision made </div>
        <div class="card-body">
            <h2 class="card-title">
            {}
            </h2>
            <p class="card-text"></p>
        </div>
        """.format('success',str(df['PASSED_TIME'].values[0])[:10]), unsafe_allow_html=True)
    elif df['OUTCOME'].values[0]=='Rejected':
        c3.markdown(
            """
            <div class="card text-white bg-{} mb-5" >
        <div class="card-header"> Decision made </div>
        <div class="card-body">
            <h2 class="card-title">
            {}
            </h2>
            <p class="card-text"></p>
        </div>
        """.format('danger',str(df['PASSED_TIME'].values[0])[:10]), unsafe_allow_html=True)
    else:
        c3.markdown(
            """
            <div class="card text-white bg-{} mb-5" >
        <div class="card-header"> Decision made </div>
        <div class="card-body">
            <h2 class="card-title">
            {}
            </h2>
            <p class="card-text"></p>
        </div>
        """.format('secondary',str(df['PASSED_TIME'].values[0])[:10]), unsafe_allow_html=True)



    c1,c2=st.columns((30,70))
    fig = go.Figure(go.Indicator(
        mode = "number",
        # value = df['PROPOSAL_ID'].values[0],
        # delta=1,
        # number = {'prefix': "$"},
        title="Proposal submitted by {}".format(df['PROPOSER'].values[0]),
        # delta = {'position': "bottom", 'reference': round(float(dao_twitter['Followers'][1]),3)},
        domain = {'x': [0, 1], 'y': [0, 1]}))
    fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(215,215,215,255)',})
    fig.update_layout(height=160, width=600)
    fig.update_layout(font=dict(
            # family="Courier New, monospace",
            # size=18,
            color="black"
        ))
    c1.plotly_chart(fig,use_container_width=True)

    fig = go.Figure(go.Indicator(
        mode = "number",
        # value = df['PROPOSAL_ID'].values[0],
        # delta=1,
        # number = {'prefix': "$"},
        title="Target wallet provided {}".format(df['target'].values[0]),
        # delta = {'position': "bottom", 'reference': round(float(dao_twitter['Followers'][1]),3)},
        domain = {'x': [0, 1], 'y': [0, 1]}))
    fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(215,215,215,255)',})
    fig.update_layout(height=160, width=600)
    fig.update_layout(font=dict(
            # family="Courier New, monospace",
            # size=18,
            color="black"
        ))
    c1.plotly_chart(fig,use_container_width=True)

    fig = go.Figure(go.Indicator(
        mode = "number",
        # value = df['PROPOSAL_ID'].values[0],
        # delta=1,
        # number = {'prefix': "$"},
        title="Amount requested :$ {}".format(udf.find_amount(df['PROPOSAL'].values[0])),
        # delta = {'position': "bottom", 'reference': round(float(dao_twitter['Followers'][1]),3)},
        domain = {'x': [0, 1], 'y': [0, 1]}))
    fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(215,215,215,255)',})
    fig.update_layout(height=160, width=600)
    fig.update_layout(font=dict(
            # family="Courier New, monospace",
            # size=18,
            color="black"
        ))
    c1.plotly_chart(fig,use_container_width=True)


    astro_page_url= ('https://app.astrodao.com/dao/marketing.sputnik-dao.near/proposals/marketing.sputnik-dao.near-') 
    c2.markdown(
        """
            <div class="card bg-light mb-3">
            <div class="card-header"> Proposal </div>
            <div class="card-body">
            <h2 class="card-title">
            {}
            <br>
            <br>
            <a href="{}">{}</a>
            <br>
            <br>
            <a href="{}">{}</a>
            <br>
            <br>
            </h2>
            <p class="card-text"></p>
            </div>
        """.format(df['PROPOSAL'].values[0],df['PROPOSAL_URL'].values[0],'Governance Page',astro_page_url+str(df['PROPOSAL_ID'].values[0]),'Astro DAO page'), unsafe_allow_html=True)
    components.html("""<hr style="height:5px;border:none;color:#333;background-color:#333;" /> """)

    st.header('Vote Information for proposal {}'.format(input_prop_id))
    votes_for_proposal="https://node-api.flipsidecrypto.com/api/v2/queries/7ec28185-d882-4a7f-89e8-991f7bb80ead/data/latest"
    votes_for_proposal=pd.read_json(votes_for_proposal)
    votes_for_proposal=votes_for_proposal[votes_for_proposal['PROPOSAL_ID']==input_prop_id]
    st.dataframe(votes_for_proposal[['BLOCK_TIMESTAMP','TX_HASH','VOTER','VOTE']],use_container_width=True)
   


with dashboard_in_depth:
    st.title('Grants Approved')
    c1,c2=st.columns(2)
    c1.plotly_chart(prop_info_pass_fail_dist_fig, use_container_width=True)

    prop_pass_monthly = "https://node-api.flipsidecrypto.com/api/v2/queries/4e76cabf-5362-4535-aeca-3ef817f807f5/data/latest"
    prop_pass_monthly = pd.read_json(prop_pass_monthly)
    prop_pass_monthly_fig=px.bar(prop_pass_monthly,x='MONTH',y='PROPS',color='OUTCOME',color_discrete_sequence=["blue", "red", "green", "goldenrod", "magenta"])
    prop_pass_monthly_fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(235,235,235,255)',})    
    prop_pass_monthly_fig.update_layout(        
        width=600,
        height=400,)
    prop_pass_monthly_fig.update_layout(
        title="<a href='https://app.flipsidecrypto.com/velocity/queries/4e76cabf-5362-4535-aeca-3ef817f807f5'> Proposals over time</a>",
        xaxis_title="Date",
        yaxis_title="USD",
        # legend_title="",
        font=dict(
            # family="Courier New, monospace",
            size=18,
            color="black"
        ))

    c2.plotly_chart(prop_pass_monthly_fig, use_container_width=True)

    c1,c2,c3=st.columns((30,30,40))
    top_proposers=proposal_info[proposal_info['OUTCOME']=='Approved']
    top_proposers=top_proposers.groupby(by='PROPOSER',as_index=False).count()
    top_proposers=top_proposers.sort_values(by='PROPOSAL_ID',ascending=False)
    top_proposers_fig=px.bar(top_proposers.head(5),x='TX_HASH',y='PROPOSER',color='PROPOSER',orientation='h',color_discrete_sequence=["blue", "red", "green", "goldenrod", "magenta"])
    top_proposers_fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(235,235,235,255)',})    
    top_proposers_fig.update_layout(        
        width=600,
        height=400,)
    top_proposers_fig.update_layout(
        title="<a href='https://app.flipsidecrypto.com/velocity/queries/4e76cabf-5362-4535-aeca-3ef817f807f5> Top grant awardees </a>",
        xaxis_title="Grants awarded",
        yaxis_title="Proposer",
        # legend_title="",
        font=dict(
            # family="Courier New, monospace",
            size=11,
            color="black"
        ))
    c1.plotly_chart(top_proposers_fig,use_container_width=True)

    prop = "https://node-api.flipsidecrypto.com/api/v2/queries/a3e4a5eb-bc71-4589-8ac9-d98f1c425cef/data/latest"
    prop = pd.read_json(prop)
    prop['target']=prop['PROPOSAL'].apply(udf.find_target)
    prop['target'].fillna(prop['PROPOSER'],inplace=True)
    passed_time="https://node-api.flipsidecrypto.com/api/v2/queries/e9905d70-6870-44dd-aa32-8c6e7f32476f/data/latest"
    passed_time=pd.read_json(passed_time)
    pass_prop_time=pd.merge(prop,passed_time, on='PROPOSAL_ID', how='left')
    pass_prop_time=pass_prop_time.rename(columns = {'BLOCK_TIMESTAMP':'Proposed_time','TX_HASH':'proposal_txn_hash'})
    pass_prop_time['PROPOSAL_SUBMITTED']=pd.to_datetime(pass_prop_time['PROPOSAL_SUBMITTED'])
    pass_prop_time['diff_days'] = (pass_prop_time['PASSED_TIME'] - pass_prop_time['PROPOSAL_SUBMITTED']) / np.timedelta64(1, 'D')
    pass_prop_time.sort_values(by='PROPOSAL_SUBMITTED',ascending=True,inplace=True)
    pass_prop_time=pass_prop_time[pass_prop_time['diff_days']>0]
    avg_duration_between_sub_and_pass=px.violin(pass_prop_time,y='diff_days',color_discrete_sequence=["blue", "red", "green", "goldenrod", "magenta"])
    avg_duration_between_sub_and_pass.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(235,235,235,255)',})    
    avg_duration_between_sub_and_pass.update_layout(        
        width=600,
        height=400,)
    avg_duration_between_sub_and_pass.update_layout(
        title="<a href='https://app.flipsidecrypto.com/velocity/queries/e9905d70-6870-44dd-aa32-8c6e7f32476f'> Avg. Decision Time </a>",
        # xaxis_title="Date",
        yaxis_title="Number of days",
        # legend_title="",
        font=dict(
            # family="Courier New, monospace",
            size=18,
            color="black"
        ))
    c2.plotly_chart(avg_duration_between_sub_and_pass,use_container_width=True)

    received_applications=pd.read_excel('Marketing_dao.xlsx',skiprows=6)
    received_applications_cat=received_applications['Category'].value_counts().head(10)
    received_applications_cat_fig=px.pie(received_applications_cat,names=received_applications_cat.keys(),values=received_applications_cat.values,color_discrete_sequence=["blue", "red", "green", "goldenrod", "magenta"])
    received_applications_cat_fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(235,235,235,255)',})    
    received_applications_cat_fig.update_layout(        
        width=600,
        height=400,)
    received_applications_cat_fig.update_layout(
        title="<a href='https://gov.near.org/t/approved-marketing-dao-council-remuneration-revised-for-relaunch/31912'> Grant requests recieved by category </a>",
        # xaxis_title="Date",
        # yaxis_title="Number of days",
        # legend_title="",
        font=dict(
            # family="Courier New, monospace",
            size=18,
            color="black"
        ))
    c3.plotly_chart(received_applications_cat_fig,use_container_width=True)

    st.title('Funds disbursed')
    c1,c2,c3=st.columns((45,25,30))
    
    c1.plotly_chart(payment_trend_fig, use_container_width=True)
    payments=pass_prop_time_and_pay[(pass_prop_time_and_pay['diff_days'] < 45) & (pass_prop_time_and_pay['diff_days'] >0) & (pass_prop_time_and_pay['AMOUNT']<20000)]
    
    average_duration_for_pay=px.violin(payments,y='diff_days',color_discrete_sequence=["blue", "red", "green", "goldenrod", "magenta"])
    average_duration_for_pay.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(235,235,235,255)',})    
    average_duration_for_pay.update_layout(        
        width=600,
        height=400,)
    average_duration_for_pay.update_layout(
        title="<a href='https://app.flipsidecrypto.com/velocity/queries/38932b59-1ed3-4ebe-bbbe-5d1600c9b1c2'> Avg. Payment Time</a>",
        # xaxis_title="Date",
        yaxis_title="Number of days",
        # legend_title="",
        font=dict(
            # family="Courier New, monospace",
            size=18,
            color="black"
        ))
    c2.plotly_chart(average_duration_for_pay,use_container_width=True)

    coin_preference=px.pie(payments.groupby(by='COIN',as_index=False).sum(),names='COIN',values='AMOUNT',color_discrete_sequence=["blue", "red", "green", "goldenrod", "magenta"])
    coin_preference.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(235,235,235,255)',})    
    coin_preference.update_layout(        
        width=600,
        height=400,)
    coin_preference.update_layout(
        title="<a href='https://app.flipsidecrypto.com/velocity/queries/38932b59-1ed3-4ebe-bbbe-5d1600c9b1c2'>Payout asset</a>",
        # xaxis_title="Date",
        # yaxis_title="Number of days",
        # legend_title="",
        font=dict(
            # family="Courier New, monospace",
            size=18,
            color="black"
        ))
    c3.plotly_chart(coin_preference,use_container_width=True)


    st.title('Target wallets')
    c1,c2=st.columns((60,40))
    c1.plotly_chart(top_target_wallets_fig, use_container_width=True)
    fig = go.Figure(go.Indicator(
        mode = "number",
        value = int(top_target_wallets.shape[0]),
        # delta=1,
        # number = {'prefix': "$"},
        title="Number of target wallets",
        # delta = {'position': "bottom", 'reference': round(float(dao_twitter['Followers'][1]),3)},
        domain = {'x': [0, 1], 'y': [0, 1]}))
    fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(215,215,215,255)',})
    fig.update_layout(height=220, width=600)    
    fig.update_layout(font=dict(
            # family="Courier New, monospace",
            # size=18,
            color="black"
        ))
    # c2.plotly_chart(fig,use_container_width=True)
    c2.plotly_chart(fig, use_container_width=True)

    prop = "https://node-api.flipsidecrypto.com/api/v2/queries/4c233639-4cdb-486c-af11-3ea18d365086/data/latest"
    prop = pd.read_json(prop)
    prop['target']=prop['PROPOSAL'].apply(udf.find_target)
    prop['target'].fillna(prop['PROPOSER'],inplace=True)
    df=prop

    # Convert the Join Date column to a datetime format
    df['BLOCK_TIMESTAMP'] = pd.to_datetime(df['BLOCK_TIMESTAMP'])

    # Extract the month and year from the Join Date column
    df['Month'] = df['BLOCK_TIMESTAMP'].dt.strftime('%Y-%m')

    # Group the data by the Month column and count the number of users in each group
    grouped_df = df.groupby(by='Month',as_index=False).count()

    # Calculate the month-over-month growth of new users by subtracting the previous month's count from the current month's count
    grouped_df['MoM Growth'] = grouped_df['target'].pct_change()

    # Show the result
    grouped_df['Month'] = pd.to_datetime(grouped_df['Month'], format='%Y-%m')
    mom_target=(grouped_df.sort_values(by='Month',ascending=True))
    mom_target['MoM Growth']=mom_target['MoM Growth']*100
    # px.line(mom_target,x='Month',y='MoM Growth')
    target_mom_growth=px.line(mom_target,x='Month',y='MoM Growth',color_discrete_sequence=["blue", "red", "green", "goldenrod", "magenta"])
    target_mom_growth.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(235,235,235,255)',})    
    target_mom_growth.update_layout(        
        width=600,
        height=220,)
    target_mom_growth.update_layout(
        title="<a href='https://app.flipsidecrypto.com/velocity/queries/4c233639-4cdb-486c-af11-3ea18d365086'>Month-on-month growth of target</a>",
        xaxis_title="Date",
        yaxis_title="Growth %",
        # legend_title="",
        font=dict(
            # family="Courier New, monospace",
            size=12,
            color="black"
        ))
    c2.plotly_chart(target_mom_growth,use_container_width=True)
    c2.caption('Spike is attributed to the hiatus taken by Marketing dao. Read more here https://gov.near.org/t/announcement-marketing-dao-resumes-operations/31028')

    st.title('Council member & votes')
    Current_members=pd.DataFrame(['whendacha.near', 'so608.near', 'cryptocredit.near', 'klint.near', 'alejandro.near'])
    Current_members.columns=['Council members']
    
    c1,c2=st.columns((30,70))
    fig = go.Figure(go.Indicator(
        mode = "number",
        value = 5,
        # delta=1,
        # number = {'prefix': "$"},
        title="Number of current council members",
        # delta = {'position': "bottom", 'reference': round(float(dao_twitter['Followers'][1]),3)},
        domain = {'x': [0, 1], 'y': [0, 1]}))
    fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(215,215,215,255)',})
    fig.update_layout(height=220, width=600)
    fig.update_layout(font=dict(
            # family="Courier New, monospace",
            # size=18,
            color="black"
        ))
    c1.plotly_chart(fig,use_container_width=True)

    c1.dataframe(Current_members,use_container_width=True)


    # st.header('Vote Information for proposal {}'.format(input_prop_id))
    votes_for_proposal_all="https://node-api.flipsidecrypto.com/api/v2/queries/7ec28185-d882-4a7f-89e8-991f7bb80ead/data/latest"
    votes_for_proposal_all=pd.read_json(votes_for_proposal_all)
    votes_for_proposal=votes_for_proposal_all[votes_for_proposal_all['VOTER'].isin(['whendacha.near', 'so608.near', 'cryptocredit.near', 'klint.near', 'alejandro.near'])]
    temp=votes_for_proposal[['VOTER','VOTE','PROPOSAL_ID']]
    temp=temp.groupby(by=['VOTER','VOTE'],as_index=False).count()
    pv=temp.pivot(index='VOTER',columns='VOTE',values='PROPOSAL_ID')
    # px.line(mom_target,x='Month',y='MoM Growth')
    voting_activity=px.imshow(pv,text_auto=True,color_continuous_scale=px.colors.sequential.Greens_r)
    voting_activity.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(235,235,235,255)',})    
    voting_activity.update_layout(        
        width=600,
        height=450,)
    voting_activity.update_layout(
        title="<a href='https://app.flipsidecrypto.com/velocity/queries/7ec28185-d882-4a7f-89e8-991f7bb80ead'>Voting activity of council members</a>",
        # xaxis_title="Date",
        # yaxis_title="Growth %",
        # legend_title="",
        font=dict(
            # family="Courier New, monospace",
            size=12,
            color="black"
        ))
    c2.plotly_chart(voting_activity,use_container_width=True)

    c1,c2=st.columns((60,40))
    votes_for_proposal_all="https://node-api.flipsidecrypto.com/api/v2/queries/7ec28185-d882-4a7f-89e8-991f7bb80ead/data/latest"
    votes_for_proposal_all=pd.read_json(votes_for_proposal_all)

    start=votes_for_proposal_all.groupby(by='VOTER',as_index=False).min()[['VOTER','BLOCK_TIMESTAMP']]
    start.columns=['VOTER','First_day']
    end=votes_for_proposal_all.groupby(by='VOTER',as_index=False).max()[['VOTER','BLOCK_TIMESTAMP']]
    end.columns=['VOTER','last_day']
    start_end=start.merge(end, on='VOTER', how='inner')

    start_end_fig = px.timeline(start_end, x_start="First_day", x_end="last_day", y="VOTER",color_discrete_sequence=["blue", "red", "green", "goldenrod", "magenta"])
    start_end_fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up
    start_end_fig.update_layout({'plot_bgcolor': 'rgba(100, 0, 0, 0)','paper_bgcolor': 'rgba(235,235,235,255)',})    
    start_end_fig.update_layout(        
        width=600,
        height=500,)
    start_end_fig.update_layout(
        title="<a href='https://app.flipsidecrypto.com/velocity/queries/7ec28185-d882-4a7f-89e8-991f7bb80ead'>Start and end of Voting members</a>",
        # xaxis_title="Date",
        # yaxis_title="Growth %",
        # legend_title="",
        font=dict(
            # family="Courier New, monospace",
            size=12,
            color="black"
        ))
    c2.plotly_chart(start_end_fig,use_container_width=True)
    c1.plotly_chart(top_voters_heatmap, use_container_width=True)

    with writeup:
        
        st.markdown(
            """
            <div class="card text-white bg-secondary mb-3" >
        <div class="card-header"> <h2>  </h2></div>
        <div class="card-body">
            <t>
            Find the entire code here https://github.com/sandeshsk12/near.git<br>
            Discord handle : sandesh#8645 <br>
            Twitter link : https://twitter.com/Sandesh_K_12/status/1621732207315546112?s=20
            <p class="card-text"></p>
        </div>
        """, unsafe_allow_html=True)
        c1,c2=st.columns((60,40))
        c1.title('Introduction')
        c1.markdown("""
            ### Near Marketing DAO

            The Near Marketing DAO is a decentralized autonomous organization in the NEAR ecosystem, made up of global marketing professionals, creatives, and NEAR enthusiasts.

            #### Responsibilities
            - Monitoring proposals and Community comments
            - Reviewing proposals to evaluate strength and value to the NEAR Community
            - Providing feedback to allocate funds to quality marketing activities
            - Tracking decision-making processes with transparency
            - Offering advice and support to Community members
            - Reviewing reports and supporting documentation to ensure responsible fund allocation

            #### Origins
            The Near Marketing DAO originated from the Sputnik DAO and is one of the most active DAOs in the NEAR ecosystem.

        """
        )
        c2.title('Objective')
        c2.markdown("""
        ### MarketingDAO Analytics Dashboard Objective

        The objective of the MarketingDAO's analytics dashboard is to track proposals and funding for the grants program by using data available in the proposals on AstroDAO. The dashboard should display key metrics, including the number of grants approved, the amount of funds disbursed over time, project names, target wallets, council members, and votes. The purpose of this dashboard is to provide a clear and comprehensive overview of the grants program, enabling the MarketingDAO to make data-driven decisions and allocate funds effectively.


        """)
        st.title('Grant Approval Process')
        st.image('flow_nmd.png',use_column_width=True)
        st.title('Methodology')
        with st.expander("Identifying Proposals and their Status"):
            st.markdown("""

            ## Identifying proposals and their status. 

            

            ### Identifying proposals
            - We use the `near.core.fact_transactions` to identify the proposal submission. 
            - We filter the transactions based on method being `add_proposal`, tx_receiver being `marketing.sputnik-dao.near`. 
            - Decoding the arguments under actions field results in Proposal id and the proposal text.

           

            ### Identifying votes
            - `near.core.fact_receipts` tables from flipside are used instead of `near.core.fact_transactions` as the transactions table does not identify all the votes and proposals. 
            - For example, `https://nearblocks.io/txns/GEX8tAHPmBPMTB2ub6d3fab3w4dTdsmCk74mjUguTHTU#execution` has the proposal id required to identify the vote and proposal in the second receipt which is not available in the fact transactions table. Hence we go with `near.core.fact_receipts` tables. 
            
            

            ### Deciding if the proposal is Approved, Rejected or Expired. 
            `Near marketingDAO`  needs a simple majority to pass the proposal. With there being 5 council members at a given time, the proposal needs at least 3 votes to being considered as Approved or Rejected. 
            - Using the same rule, we identify 
            - proposals with less than 3 as expired
            - Proposals with more Approve votes than rejects as Approved 
            - Proposals with more Reject votes than approved as Rejected. 
            - We extract the URL from the proposal text using regular expressions.
            
            

            Query Link : https://app.flipsidecrypto.com/velocity/queries/a3e4a5eb-bc71-4589-8ac9-d98f1c425cef


            Proposal category: the proposal category is dervied from Near MarketingDAO's transparency report which is available here.https://gov.near.org/t/approved-marketing-dao-council-remuneration-revised-for-relaunch/31912 .
            The data obtained from the transaparency report is wrangled and displayed using python. 

            """)
        with st.expander("Grants issued"):
            st.markdown("""
            Payments issued: 
            Identifying payments is a tricky affair. The payments are made not from a separate entity but rather from the near foundation. Hence, to identify the payments made we look at the near foundation accounts, ( 'nf-payments.near','nf-payments1.near','nf-payments2.near','nf-payments3.near','nf-payments4.near','nf-payments5.near' ) 
            In order to accurately identify payments made only to near marketing grantees, we join the payments table and the proposal table on the target wallet provided. We further limit the entries to those having only 45 days difference between the proposal time and payment time. However, a caveat here is that if the target wallet had received grant money from another near DAO through near foundation in the same period, then it will be double counted. 
            The data for payments made by near foundation to the respective wallets is extracted from near tables using Flipside query and is joined with proposal information using Pandas in python. 
            The query for extracting payment info can be accessed here: 

            1. Near ecosystem token : https://app.flipsidecrypto.com/velocity/queries/38932b59-1ed3-4ebe-bbbe-5d1600c9b1c2
            
            2. Near token: https://app.flipsidecrypto.com/velocity/queries/975c569b-eae7-47ec-a1bf-eae7b21e60a6

            3. Proposal Information: https://app.flipsidecrypto.com/velocity/queries/a3e4a5eb-bc71-4589-8ac9-d98f1c425cef

            Wrong approach used by other works, Some reports attempt to use the “kind” argument under actions to calculate the funds disbursed, this is a wrong approach, as even rejected transactions show up as having funds disbursed. For example, Proposal id 597, Example transaction hash: https://nearblocks.io/txns/CMVquTbk1LWoZHJsFntVPtkLV7cm3W9pNkmSRk8WVpSf#execution


            """)
        
        with st.expander("Target wallets"):
            st.markdown("""
            ## Target wallet
            The target wallets may differ from the proposer's address. To identify the target wallet, we use information from the proposal. With the help of a Regex in Python, we extract the target wallet from the proposal text. In cases where the target wallet information is missing from the proposal, we use the proposer's address as a substitute. 

            """)
        with st.expander("Voting activity"):
            st.markdown("""
            ## Identifying votes and voters



            ### Identifying votes 
            - Near.core.fact_receipts tables from flipside are used instead of near.core.fact_transactions 
            - The transactions table does not identify all the votes and proposals. For example, 
                https://nearblocks.io/txns/GEX8tAHPmBPMTB2ub6d3fab3w4dTdsmCk74mjUguTHTU#execution has the 
                proposal id required to identify the vote and proposal in the second receipt which is not 
                available in the fact transactions table. Hence we go with Near.core.fact_receipts tables. 
            - The conditions placed while querying include:
            - method name being `act_proposal`
            - receiver id being `marketing.sputnik-dao.near`


            
            ### Identifying voters
            - Voters are identified using the `predecessor_id` under the `actions` attribute
            - The vote information can be extracted from the table after decoding the `argos` variable under the `actions` attribute in the `fact_receipts` table
            - We consider a voter to be a council member at some point of the time only if they have voted a minimum of 5 times
            - The query used to extract the voting activity:
            https://app.flipsidecrypto.com/velocity/queries/7ec28185-d882-4a7f-89e8-991f7bb80ead



            """)

        st.title('Glossary')
        st.markdown("""
        Avg. Decision Time: 
        The average number of days taken for a submitted proposal to receive an Approval or Rejection decision.

        Avg. Payment Time:
        The average number of days taken for an approved proposal to be Paid.

        """)
        st.markdown(f"""
            # <div style='text-align: center'>
            <div class="card text-white bg-secondary mb-3" >

            <div class="card-header">Note to reviewer <h2> <br> 

            Observation on Project Names: 
            
            It has been observed that out of the 500+ proposals, only 26 have a clearly defined project name. This makes it difficult to extract the project name using text processing. As a result, the metric of project name has been dropped from the dashboard.

            Extraction for Interested Users

            For users who are interested in extracting project names, the following python expression can be used:

            Python code: <br>
            ```match = re.search(r"Project name: (.*?),|Project Name: (.*?)|project name: (.*?),|Project name: (.*?):|Project name: (.*?);|Project name : (.*?),|Project: (.*?).", text)```
            <br></h2></div>    
                <p class="card-text"></p>
            </div>
            </div>
            """, unsafe_allow_html=True)

        st.title('SQL Queries')
        st.markdown("""
            
            1. https://app.flipsidecrypto.com/velocity/queries/ed5b2960-2873-4f3b-bdf6-64733e94d8df

            2. https://app.flipsidecrypto.com/velocity/queries/742b1591-89ff-48b7-84f3-275d11510ed8

            3. https://app.flipsidecrypto.com/velocity/queries/38932b59-1ed3-4ebe-bbbe-5d1600c9b1c2

            4. https://app.flipsidecrypto.com/velocity/queries/975c569b-eae7-47ec-a1bf-eae7b21e60a6

            5. https://app.flipsidecrypto.com/velocity/queries/f62545cc-ee0f-4bc3-bb97-2124782bfdd2

            6. https://app.flipsidecrypto.com/velocity/queries/4e76cabf-5362-4535-aeca-3ef817f807f5

            7. https://app.flipsidecrypto.com/velocity/queries/a3e4a5eb-bc71-4589-8ac9-d98f1c425cef

            8. https://app.flipsidecrypto.com/velocity/queries/e9905d70-6870-44dd-aa32-8c6e7f32476f

            9. https://app.flipsidecrypto.com/velocity/queries/4c233639-4cdb-486c-af11-3ea18d365086

            10. https://app.flipsidecrypto.com/velocity/queries/7ec28185-d882-4a7f-89e8-991f7bb80ead

            """)
        with takeaways:
            st.title('Key takeaways')
            st.markdown("""
            - 439 proposals, or 75% of all submissions, have been approved with 10% of them expiring. The declining trend of expired proposals indicates prompt decision making with an average decision time of just 3 days, mostly being made within a week. The grant requests received are divided into 30% for community-related initiatives and 25% for creative projects.
            - To date, grant funds of 1 million dollars have been disbursed to 75 wallets, with an average payment time of 20 days after approval. Most of the disbursed funds were in the form of NEAR tokens.
            - Funding has been distributed to 71 target wallets, with the Russian community and Cizi31.near (a Turkish Near community) receiving the highest amount.
            - The council of the community-driven organization has several members responsible for managing community resources and decision making on proposals. Recently, four members - whendacha, cryptocredit, alejandro, and So608 - have been particularly active in decision making and furthering community goals. Among the voters currently on the council, whendacha is the most active, exercising their right to remove votes and finalize decisions. This showcases whendacha's dedication and the council's experience and commitment in community management as they have been serving the community for an extended period of time.

            """)
        with recommendation:
            st.title("Recommendation to the Near Marketing DAO team")
            st.markdown("""
            To build a complete on-chain dashboard, two main obstacles must be overcome:

            - Information Extraction: To extract information from proposal texts, text processing is used in either SQL or Python to retrieve parameters such as target wallet, amount requested, project name, governance forum URL, and proposal category. However, the presence of non-standard data, such as the requested amount, can complicate the process. For example, the requested amount can have multiple formats (e.g., 500 USD, \$500, 500\$, 500 US Dollars, 500 Near worth USDC, 250\$ + 250\$, etc.). To make the system more robust and avoid this complexity, it is recommended to enforce a stricter standard template for proposals.

            - Payments: Currently, payments are made through nf2-foundation.near and related addresses without any identification that it is a grant release for the Near Marketing DAO. To improve transparency, it is recommended that future payments made from Near Foundation-related accounts include a message indicating that it is for the Marketing DAO and include the proposal ID. This will help ensure that the source of the funds and the purpose for which they are being used is clear to all parties involved.
            """)
            st.markdown("")
            st.markdown("""
            It has been noted that some approved proposals have yet to receive a grant. In particular, six such proposals have been identified. This issue could stem from either the grantees' lack of knowledge about the requirement to fill out the Ironclad form, or from a delay in processing by the team. To address this, it is recommended to raise awareness about the process and to ensure timely follow-up of approved proposals, in order to reduce the risk of duplicate submissions.
            """)










    