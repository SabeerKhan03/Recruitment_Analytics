from pathlib import Path
import pandas as pd, streamlit as st, plotly.express as px
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'outputs'
st.set_page_config(page_title='Recruitment Analytics',layout='wide'); st.title('Recruitment Operations & AI Screening Analytics'); st.caption('Synthetic portfolio dataset')
p=OUT/'application_analysis.csv'
if not p.exists(): st.warning('Run python python/run_analysis.py first.'); st.stop()
df=pd.read_csv(p,parse_dates=['application_date','hire_date']); options=sorted(df.source_name.unique()); selected=st.sidebar.multiselect('Recruitment source',options,default=options); df=df[df.source_name.isin(selected)]
offers=int(df.offered.sum()); hires=int(df.hired.sum()); accept=int(df.offer_accepted.sum()); avg=df.loc[df.hired.eq(1),'time_to_hire_days'].mean()
c=st.columns(5); c[0].metric('Applications',f'{len(df):,}'); c[1].metric('Offers',f'{offers:,}'); c[2].metric('Hires',f'{hires:,}'); c[3].metric('Offer acceptance',f'{accept/offers:.1%}' if offers else '—'); c[4].metric('Avg. time-to-hire',f'{avg:.1f} days' if pd.notna(avg) else '—')
l,r=st.columns(2); src=df.groupby('source_name',as_index=False).agg(Applications=('application_id','count'),Hires=('hired','sum')); l.plotly_chart(px.bar(src,x='source_name',y=['Applications','Hires'],barmode='group',title='Applications and hires by source'),use_container_width=True)
monthly=df.assign(month=df.application_date.dt.to_period('M').astype(str)).groupby('month',as_index=False).size(); r.plotly_chart(px.line(monthly,x='month',y='size',markers=True,title='Monthly applications'),use_container_width=True)
df['score_band']=pd.cut(df.ai_screening_score,bins=[-1,39,59,74,89,100],labels=['0-39','40-59','60-74','75-89','90-100']); band=df.groupby('score_band',observed=False).agg(Applications=('application_id','count'),Hires=('hired','sum')).reset_index(); band['Hire rate']=band.Hires/band.Applications.replace(0,pd.NA); st.plotly_chart(px.bar(band,x='score_band',y='Hire rate',title='Observed hire rate by screening-score band'),use_container_width=True)
st.subheader('Job performance'); st.dataframe(df.groupby(['job_title','department'],as_index=False).agg(Applications=('application_id','count'),Hires=('hired','sum')),use_container_width=True); st.caption('Synthetic scores and outcomes; not evidence of real AI accuracy or fairness.')
