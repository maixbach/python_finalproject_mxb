# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 15:08:28 2021

@author: Administrator
"""
################################################################################################
####         A web app to help student know and solving any problem in Macroeconomics 
                                    #Author: Mai Xuan Bach                                  ####
################################################################################################

import streamlit as st
from streamlit_player import st_player
import wbdata as wb      #worldbank data                                 
import pandas as pd
import numpy as np                                     
import datetime as dt 
from matplotlib import pyplot as plt 
from matplotlib import ticker
import random
import calendar
import re

#Import form func_solver.py for some function needed
from func_solver import *

#Set page config (first use of streamlit)
st.set_page_config(page_title = 'Macroeconomics', layout = 'wide')

sb = st.container()
bd = st.container()

################################################################################################
####                                Display the home page                                   ####
################################################################################################
intro = st.container()
report = st.container()
solver = st.container()
a1,a2,a3,a4 = st.columns(4)
abt_us = st.container()

add_selectbox = st.sidebar.selectbox("Which part do you want to choose?", 
                                     ('Home Page', 'One-click Report', 'One-minute Solver')) 

if add_selectbox == 'Home Page':
    
    with intro:
        st.image("https://github.com/maixbach/python_project_mxbach_dseb_neu/blob/main/Macroeconomics%20in%20a%20nutshell.png?raw=true", width = 1000)
        st.title("PRINCIPLES OF ECONOMICS: MACROECONOMICS")
        st.markdown("**Macroeconomics in a nutshell** is a web-app to help you with making **super-fast economics report** and learning **everything in macroeconomics**. Causes of wealth, GDP, growth rate, CPI, unemployment, inflation, business cycles, monetary system, and more.")

    with report:
        st.header(":rocket: One-click Report")
        st.markdown("**One-click report** is an **automatic economic report maker** using APIs to extract real-time data from **World Bank** and instantly make a basic analysis of any country's economic situation. The report includes the analysis of:")
        st.markdown("* **Gross Domestic Product (GDP) growth *with graphs* **")
        st.markdown("* **Demand & Supply sides of production**")
        st.markdown("* **Unemployment & Inflation rate **")
        st.caption("Please click on 'One-click Report' in the left column to try it out!")
    
    with solver:
        st.header(":pencil2: One-minute Solver")
        st.markdown("**One-minute Solver** provides **main contents** of macroeconomics and helps you **solve as many as problems** in macroeconomics. The solver includes:")
        st.caption("Please click on 'One-minute Solver' in the left column to try it out!")
    with a1:
        st.success("\t**Production & Income (GDP)**")
    with a2:
        st.success("\t**Consumer price index (CPI) & Inflation rate**")
    with a3:
        st.success("\t**Unemployment**")
    with a4:
        st.success("\t**Monetary system**")
    
    with abt_us:
        st.header(":small_red_triangle_down: About me: ") 
        st.markdown("This web-app is created by **Mai Xuan Bach (maixbach)** - DSEB62 - NEU, with the hope of helping people study macroeconomics with ease. Have a good time studying!")
        st.image("https://github.com/maixbach/python_project_mxbach_dseb_neu/blob/main/Xu%C3%A2n%20B%C3%A1ch%203_cut.jpg?raw=true", width = 200)
        st.caption("I would love to say thank to Mr. Jesson Pagaduan (from Asian Development Bank) for material and inspiration for One-click Report and Mr. Nguyen Viet Hung (NEU) for macroeconomics knowledge from his course!")

################################################################################################
####                                    ONE-CLICK REPORT SECTION                            ####
################################################################################################

###                            SOME FUNCTIONS TO DISPLAY MAIN CONTENTS

################################################################################################
####                                    GDP Growth Section                                  ####
################################################################################################
def display_gdp_growth_section():    
    # 1 - Set placeholders + Qualify changes
    # wout/ placeholders, Python would try and compare objects (and not values) and it would fail
    change = ''
    if df_all['GDP growth (%)'].last('Y').values[0] > 0:
        change = random.choice(['increased', 'picked up', 'rose'])
    elif df_all['GDP growth (%)'].last('Y').values[0] == 0:
        change = random.choice(['remained at', 'stayed at'])
    else:
        change = random.choice(['decreased', 'contracted', 'slowed down'])
    
    # 2 - Heading qualifying GDP growth
    st.subheader(f'GDP in {dt.date.today().year - 1} {change}')
    #growth
    # 3 - State the change
    st.write(f"* GDP {change} by {abs(df_all['GDP growth (%)'].last('Y').values[0])}% year-on-year (yoy) in {df_all['GDP growth (%)'].last('Y').index.year.values[0]}.")
    #growth
    # 4 - Demand-side: Top contribution in the same direction as GDP growth
    st.write(f"* On the demand side, {top_demand_contributions.index[0].lower()} ({top_demand_shares.loc[top_demand_contributions.index[0]].values[0]}% of GDP) contributed the most to {'growth' if df_all['GDP growth (%)'].last('Y').values[0] > 0 else 'contraction'}, with {top_demand_contributions.values[0][0]} percentage points (pp).")
    
    # 5 - Supply-side: Top contributions in the same direction as overall growth
    st.write(f"* On the supply side, {top_production_contributions.index[0].lower()} ({top_production_shares.loc[top_production_contributions.index[0]].values[0]}% of GDP) contributed the most to {'growth' if df_all['GDP growth (%)'].last('Y').values[0] > 0 else 'contraction'}, with {top_production_contributions.values[0][0]}pp.")
    
   
################################################################################################
####                            Make GDP Contribution Graphs                                ####
################################################################################################

def display_gdp_contribution_graph():
    # Create the dataframe that will be plotted
    df_chart_gdp = df_all[['GDP growth (%)'] + [f'{item} (contribution, pp)' for item in demand_components + production_components]].dropna()
    df_chart_gdp.index = df_chart_gdp.index.year
    df_chart_gdp.reset_index(inplace=True)
    
    # Create a Pandas Excel writer using xlsxwriter as the engine
    writer = pd.ExcelWriter(f'{country}-charts.xlsx', engine='xlsxwriter')
    df_chart_gdp[['date', 'GDP growth (%)'] + [f'{item} (contribution, pp)' for item in demand_components]].to_excel(writer, sheet_name='GDP-demand', index=False)
    df_chart_gdp[['date', 'GDP growth (%)'] + [f'{item} (contribution, pp)' for item in production_components]].to_excel(writer, sheet_name='GDP-production', index=False)
    
    # Create a blank canvas
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(10, 5), sharey=True)
    plt.style.use('default')
    
    # Create a stacked bar chart of the components
    df_chart_gdp[[f'{item} (contribution, pp)' for item in demand_components]].plot(kind='bar', stacked=True, ax=axs[0])
    
    df_chart_gdp[[f'{item} (contribution, pp)' for item in production_components]].plot(kind='bar', stacked=True, ax=axs[1])
    
    # Create a line plot of the GDP growth series
    for i in range(len(axs)):
        axs[i].plot(df_chart_gdp.loc[:, 'GDP growth (%)'], lw=2.5, marker='D', markersize=10, color='black')
        # Set labels in the x-axis
        axs[i].set_xticklabels(df_chart_gdp.date, rotation=0)
        axs[i].set_ylabel('percentage points')
        axs[i].yaxis.set_major_locator(ticker.MaxNLocator(6))
        axs[i].set_xlabel('')
        axs[i].axhline(color='black', linewidth=0.5)
    
    # Set legend
    axs[0].legend(['GDP growth (%)'] + demand_components)
    axs[1].legend(['GDP growth (%)'] + production_components)
    
    # Set graph formatting and save to local folder
    axs[0].set_title('Demand-side contributions to growth')
    axs[1].set_title('Supply-side contributions to growth')
    
    plot = plt.show()
    st.pyplot(plot)

################################################################################################
####                                    Demand-side Section                                 ####
################################################################################################

def display_demand_side_section():
    
    # 1 - Heading stating largest contributor
    change = {}
    for item in demand_components:
        if df_all[f'{item} (annual growth, %)'].last('2Y').values[-1] > 0:
            change[f'{item}'] = random.choice(['expanded', 'grew', 'increased', 'picked up', 'jumped'])
        else:
            change[f'{item}'] = random.choice(['decreased', 'contracted', 'shrank', 'declined', 'plunged'])
    
    
    st.subheader(f"{top_demand_growth.index[0]} {change[top_demand_growth.index[0]]} the fastest on the demand side")
    
    # 2 - Demand-side: Item with the largest growth
    st.markdown(f"* {top_demand_growth.index[0]} {change[top_demand_growth.index[0]]} by the largest margin ({top_demand_growth.values[0][0]}%).")
    
    # 4 - Other items that grew
    i = 1
    while np.sign(top_demand_growth.values[i][0]) == np.sign(df_all['GDP growth (%)'].last('Y').values[0]):
        st.markdown(f"* {top_demand_growth.index[i]} {change[top_demand_growth.index[i]]} by {top_demand_growth.values[i][0]}%.") 
        i += 1
        if i >= len(top_demand_growth):
            break 
    
    # 5 - Items that contracted
    for i in range(1, len(top_demand_growth)):
        if np.sign(top_demand_growth.values[i][0]) != np.sign(df_all['GDP growth (%)'].last('Y').values[0]):
            st.markdown(f"* On the other hand, {top_demand_growth.index[i].lower()} {change[top_demand_growth.index[i]]} by {abs(top_demand_growth.values[i][0])}%.")
    
  
################################################################################################
####                                    Supply-side Section                                 ####
################################################################################################

def display_supply_side_section():
    # 1 - Heading stating largest contributor
    change = {}
    for item in production_components:
        if df_all[f'{item} (annual growth, %)'].last('2Y').values[-1] > 0:
            change[f'{item}'] = random.choice(['expanded', 'grew', 'increased', 'picked up', 'jumped'])
        else:
            change[f'{item}'] = random.choice(['decreased', 'contracted', 'shrank', 'declined', 'plunged'])
    
    st.subheader(f"On the supply side, {top_production_growth.index[0].lower()} {change[top_production_growth.index[0]]} the fastest")
    
    # 2 - Item with the largest growth
    st.markdown(f"* {top_production_growth.index[0]} {change[top_production_growth.index[0]]} the most rapidly ({top_production_growth.values[0][0]}%).")
    
    # 4 - Other items that grew
    i = 1
    while np.sign(top_production_growth.values[i][0]) == np.sign(df_all['GDP growth (%)'].last('Y').values[0]):
        st.markdown(f"* {top_production_growth.index[i]} {change[top_production_growth.index[i]]} by {top_production_growth.values[i][0]}%.") 
        i += 1
        if i >= len(top_production_growth):
            break 
    
    # 5 - Items that contracted
    for i in range(1, len(top_production_growth)):
        if np.sign(top_production_growth.values[i][0]) != np.sign(df_all['GDP growth (%)'].last('Y').values[0]):
            st.markdown(f"* On the other hand, {top_production_growth.index[i].lower()} {change[top_production_growth.index[i]]} by {abs(top_production_growth.values[i][0])}%.")


################################################################################################
####                                Unemployment & Inflation                                ####
################################################################################################
def display_unemployment_inflation():
    
    # 1 - Set placeholders & Qualify changes
    phillips = ['Unemployment rate (%)', 'Inflation rate (%)']
    change = {}
    for item in phillips:
        if df_all[item].last('2Y').values[-1] > df_all[item].last('2Y').values[-2]:
            change[item] = random.choice(['increased', 'increased', 'increased'])
        elif df_all[item].last('2Y').values[-1] == df_all[item].last('2Y').values[-2]:
            change[item] = random.choice(['remained', 'stayed'])
        else:
            change[item] = random.choice(['improved', 'declined', 'declined'])
    
    # 2 - Heading stating changes of each
    st.subheader(f"Unemployment {change['Unemployment rate (%)']}; inflation {change['Inflation rate (%)']}")
    
    # 3 - Sentence on Unemployment
    st.markdown(f"* Unemployment {change['Unemployment rate (%)']} from {df_all['Unemployment rate (%)'].last('2Y').values[-2]}% in {df_all['Unemployment rate (%)'].last('2Y').index[-2].year} to {df_all['Unemployment rate (%)'].last('2Y').values[-1]}% in {df_all['Unemployment rate (%)'].last('2Y').index[-1].year},")
    
    # 4 - Sentence on Inflation
    st.markdown(f"* While inflation {change['Inflation rate (%)']} from {'a deflation of' + str(abs(df_all['Inflation rate (%)'].last('2Y').values[-2])) if df_all['Inflation rate (%)'].last('2Y').values[-2] < 0 else df_all['Inflation rate (%)'].last('2Y').values[-2]}% to {'a deflation of ' + str(abs(df_all['Inflation rate (%)'].last('2Y').values[-1])) if df_all['Inflation rate (%)'].last('2Y').values[-1] < 0 else df_all['Inflation rate (%)'].last('2Y').values[-1]}%.")
    
    if policy_rate_annual.shape[0] > 0:
    # 5 - Sentence on CB Policy rate
        st.markdown(f"* {' At the end of ' + str(policy_rate_annual.last('Y').index.year[0]) + ', the central bank set the policy rate at ' + str(policy_rate_annual.last('Y').values[0][0]) + '%'}.")
    
#################################################################################################
####                                DISPLAY ONE-CLICK REPORT SECTION                         ####
#################################################################################################   

if add_selectbox == 'One-click Report':
    
    with bd:
        st.header(f" {add_selectbox}!")
        st.write("""**One-click report** is an **automatic economic report maker** using APIs to extract real-time data 
                 from World Bank and instantly make a basic analysis of any country, which is in Asia and the Pacific, 's economic situation.""")
        st.caption("Sources of data: Consensus Economics, The World Bank, UN Comtrade, Haver Analytics, and National Sources")
        
        
        #Let user input the name and turn it into ADB code for running
        adf = pd.read_excel(r'C:\Users\Administrator\Final_Project_Python\all_data.xlsx', sheet_name = "data")
        adb_code_lst = adf["adb_code"].tolist()
        adb_country_lst = adf["country_name"].tolist()
        name_country = st.sidebar.text_input("Name of country in area of Asia and the Pacific for economic analysis")
        
        if name_country:
            if name_country.title() not in adb_country_lst:
                st.error("We don't have data for this country. We will imporve to help you later! Please select another country!")
            index_find = adb_country_lst.index(name_country.title())
            country = adb_code_lst[index_find]
            
            # Create a dictionary of all indicators to be scraped from the World Bank API
            all_indicators = {'NY.GDP.MKTP.KD.ZG': 'GDP growth (%)',
                              'NE.CON.PRVT.ZS': 'Private consumption (% of GDP)', 
                              'NE.CON.GOVT.ZS': 'Government expenditure (% of GDP)',
                              'NE.GDI.TOTL.ZS': 'Gross capital formation (% of GDP)', 
                              'NE.EXP.GNFS.ZS': 'Exports (% of GDP)',
                              'NE.IMP.GNFS.ZS': 'Imports (% of GDP)',
                              'NE.CON.PRVT.KD.ZG': 'Private consumption (annual growth, %)', 
                              'NE.CON.GOVT.KD.ZG': 'Government expenditure (annual growth, %)',
                              'NE.GDI.TOTL.KD.ZG': 'Gross capital formation (annual growth, %)',
                              'NE.EXP.GNFS.KD.ZG': 'Exports (annual growth, %)',
                              'NE.IMP.GNFS.KD.ZG': 'Imports (annual growth, %)',
                              'NE.EXP.GNFS.CD': 'Exports (current prices, USD)',
                              'NE.IMP.GNFS.CD': 'Imports (current prices, USD)',
                              'NV.AGR.TOTL.ZS': 'Agriculture (% of GDP)',
                              'NV.AGR.TOTL.KD.ZG': 'Agriculture (annual growth, %)',
                              'NV.IND.TOTL.ZS': 'Industry (including construction) (% of GDP)',
                              'NV.IND.TOTL.KD.ZG': 'Industry (including construction) (annual growth, %)',
                              'NV.SRV.TOTL.ZS': 'Services (% of GDP)',
                              'NV.SRV.TOTL.KD.ZG': 'Services (annual growth, %)',
                              'SL.UEM.TOTL.NE.ZS': 'Unemployment rate (%)',
                              'FP.CPI.TOTL.ZG': 'Inflation rate (%)',
                              'BN.CAB.XOKA.GD.ZS': 'Current account balance (% of GDP)',
                              'BN.GSR.GNFS.CD': 'Net trade in goods and services (current USD)',
                              'BN.GSR.MRCH.CD': 'Net trade in goods (current USD)',
                              'FI.RES.TOTL.CD': 'Total reserves (includes gold, current USD)',
                              'FI.RES.TOTL.MO': 'Total reserves in months of imports'}

            # Set the time period
            data_date = dt.datetime(dt.date.today().year - 6, 1, 1), dt.datetime(dt.date.today().year - 0, 1, 1)
            
            # Read Excel file of country codes and country names
            country_codes = pd.read_excel(r'C:\Users\Administrator\Final_Project_Python\all_data.xlsx', sheet_name='data', index_col= 'adb_code')
            
            # Read Excel file 
            policy_rate_annual = pd.read_excel(r'C:\Users\Administrator\Final_Project_Python\quarterly_monthly_data.xlsx', sheet_name=country, header=8, index_col=0, usecols='AH:AI', parse_dates=['year']).dropna()
            
            
            
            
            
            ################################################################################################
            ####                              Scrape + Prepare WB Yearly Data  and Make DataFrame                         ####
            ################################################################################################
            
                
            # Scrape data from the World Bank API (country in [] because want to access the 'RUS' row in country_codes DF, alternative to iat, etc.)
            df_all = wb.get_dataframe(indicators=all_indicators, country=country_codes.iso_code[country], data_date=data_date, convert_date=True, source=2, cache=False)
            
            # Sort data by year # Syntax: {} = dictionary; [] = list; () = arguments for functions
            df_all = df_all.sort_index() 
            
            # Generate share of net exports in GDP
            net_exports_share = df_all['Exports (% of GDP)'] - df_all['Imports (% of GDP)']
            
            # Insert 'net_exports_share' as the 6th column, labeled 'Net exports (% of GDP)'
            df_all.insert(6, 'Net exports (% of GDP)', net_exports_share)
            
            # Generate net exports annual growth
            net_exports_growth = (df_all['Exports (current prices, USD)'] - df_all['Imports (current prices, USD)']).pct_change() * 100
            
            # Insert 'net_exports_growth' as the 12th column, labeled 'Net exports (annual growth, %)'
            df_all.insert(12, 'Net exports (annual growth, %)', net_exports_growth)
            
            # Generate contributions to GDP growth using a loop
            components = ['Private consumption', 'Government expenditure', 'Gross capital formation', 
                          'Exports', 'Imports', 'Agriculture', 'Industry (including construction)', 'Services']
            for item in components:
                df_all[f'{item} (contribution, pp)'] = df_all[f'{item} (% of GDP)'].shift(1) / 100 * df_all[f'{item} (annual growth, %)']
            
            # Generate net export contribution to GDP growth
            df_all['Net exports (contribution, pp)'] = df_all['Exports (contribution, pp)'] - df_all['Imports (contribution, pp)']
            
            # Round to one decimal
            df_all = df_all.round(1)
            
            # Create dataframe for top three sources of growth on the demand/production side
            demand_components = ['Private consumption', 'Government expenditure', 'Gross capital formation', 
                                 'Net exports']
            production_components = ['Agriculture', 'Industry (including construction)', 'Services']
            components = demand_components + production_components
            
            #  test: df_all['GDP growth (%)'].last('Y').values[0] = -1
            
            # Create dataframe for top sources of growth on the demand side
            top_demand_contributions = []
            if df_all['GDP growth (%)'].last('Y').values[0] > 0:
                top_demand_contributions = df_all.last('Y')[[f'{item} (contribution, pp)' for item in demand_components]].transpose().sort_values(by=df_all.last('Y').index[0], ascending=False)
            else:
                top_demand_contributions = df_all.last('Y')[[f'{item} (contribution, pp)' for item in demand_components]].transpose().sort_values(by=df_all.last('Y').index[0])
            top_demand_contributions.index = [index.replace(' (contribution, pp)', '') for index in top_demand_contributions.index]
            
            # Create dataframe for top shares of GDP on the demand side
            top_demand_shares = df_all.last('Y')[[f'{item} (% of GDP)' for item in demand_components]].transpose()
            top_demand_shares.index = [index.replace(' (% of GDP)', '') for index in top_demand_shares.index]
            top_demand_shares = top_demand_shares.reindex(top_demand_contributions.index)
            
            # Create dataframe for top growth rates of GDP components on the demand side
            top_demand_growth = []
            if df_all['GDP growth (%)'].last('Y').values[0] > 0:
                top_demand_growth = df_all.last('Y')[[f'{item} (annual growth, %)' for item in demand_components]].transpose().sort_values(by=df_all.last('Y').index[0], ascending=False)
            else:
                top_demand_growth = df_all.last('Y')[[f'{item} (annual growth, %)' for item in demand_components]].transpose().sort_values(by=df_all.last('Y').index[0])
            top_demand_growth.index = [index.replace(' (annual growth, %)', '') for index in top_demand_growth.index]
            
            # Create dataframe for top sources of growth on the production side
            top_production_contributions = []
            if df_all['GDP growth (%)'].last('Y').values[0] > 0:
                top_production_contributions = df_all.last('Y')[[f'{item} (contribution, pp)' for item in production_components]].transpose().sort_values(by=df_all.last('Y').index[0], ascending=False)
            else:
                top_production_contributions = df_all.last('Y')[[f'{item} (contribution, pp)' for item in production_components]].transpose().sort_values(by=df_all.last('Y').index[0])
            top_production_contributions.index = [index.replace(' (contribution, pp)', '') for index in top_production_contributions.index]
            
            # Create dataframe for top shares of GDP on the supply side
            top_production_shares = df_all.last('Y')[[f'{item} (% of GDP)' for item in production_components]].transpose()
            top_production_shares.index = [index.replace(' (% of GDP)', '') for index in top_production_shares.index]
            top_production_shares = top_production_shares.reindex(top_production_contributions.index)
            
            # Create dataframe for top growth rates of GDP components on the production side
            top_production_growth = []
            if df_all['GDP growth (%)'].last('Y').values[0] > 0:
                top_production_growth = df_all.last('Y')[[f'{item} (annual growth, %)' for item in production_components]].transpose().sort_values(by=df_all.last('Y').index[0], ascending=False)
            else:
                top_production_growth = df_all.last('Y')[[f'{item} (annual growth, %)' for item in production_components]].transpose().sort_values(by=df_all.last('Y').index[0])
            top_production_growth.index = [index.replace(' (annual growth, %)', '') for index in top_production_growth.index]
    
            ################################################################################################
            ####                              DISPLAY ALL PARTS OF REPORT                               ####
            ################################################################################################
            
            st.markdown(f"<h1 style='text-align: center; color: red;'>{name_country.title()} economic report</h1>", unsafe_allow_html=True)
            display_gdp_growth_section()
            display_gdp_contribution_graph()
            display_demand_side_section()
            display_supply_side_section()
            display_unemployment_inflation()
        
        
#To make pyplot working      
st.set_option('deprecation.showPyplotGlobalUse', False)

 


#################################################################################################
####                                DISPLAY ONE-MINUTE SOLVER SECTION                         ####
#################################################################################################         
if add_selectbox == 'One-minute Solver':
    
    with bd:
        st.image("https://github.com/maixbach/python_project_mxbach_dseb_neu/blob/main/Macroeconomics%20in%20a%20nutshell.png?raw=true", width = 1000)
        option_of_solver = st.sidebar.selectbox("Which chapter do you want to learn?", 
                                     ('Production & Income', 'Consumer price index & Inflation rate', 'Unemployment', 'Monetary system'))
        
        #################################################################################################
####                                CHAPTER: PRODUCTION & INCOME                         ####
################################################################################################# 
        
        if option_of_solver == "Production & Income":
            option_of_prod_income = st.sidebar.radio("Choose problem: ", ["GDP calculator", "Economic growth rate", "Economic growth rate over time", "GDP deflator & Inflation"])
            
            #Display the main contents of this chapter
            st.header("**Measuring a nation's production & income**")
            
            st.subheader("**1. Gross Domestic Product (GDP)**")
            st.write('**Gross Domestic Product (GDP)** is the *market value* of *all final* goods and services *produced* within a *country* in a given period of *time*.')
            st.markdown("* Market value: GDP is measured in terms of **currency**")
            st.markdown("* Goods and services: GDP *excludes* the **self-sufficient** products")
            st.markdown("* Final goods: GDP *excludes* the **intermediate goods**")
            st.markdown("* Produced within a country: GDP *excludes* **imports**")
            st.markdown("* Produced in a given period of time: GDP *excludes* **goods produced in previous years**")
            st.write('**Examples: **')
            gdp1, gdp2 = st.columns(2)
            with gdp1:
                st.image("https://github.com/maixbach/python_project_mxbach_dseb_neu/blob/main/iphone12.jpg?raw=true", width = 300)
                st.markdown("**Iphone 13** that a **Vietnamese purchased** is *NOT INCLUDED* in GDP of Vietnam")
            with gdp2:
                st.image("https://github.com/maixbach/python_project_mxbach_dseb_neu/blob/main/samsungzfold.jpg?raw=true", width = 300)
                st.markdown("**Samsung Z Fold produced in Vietnam** is *INCLUDED* in GDP of Vietnam")
            
            st.subheader("**2. Three approaches to measure GDP**")
            st.markdown("* **Value added approach**")
            st.markdown("* **Income approach**")
            st.markdown("* **Production/Expenditure approach** *(most widely used)*")
            
            st.subheader("**3. The components of GDP**")
            st.title(" **GDP = C + I + G + NX**")
            st.markdown("* **Consumption (C)**: Spending by households on newly produced goods and services.")
            st.markdown("* **Investment (I)**: The purchase of capital equipment, inventories, new house built and structures.")
            st.markdown("* **Government purchases (G)**: Including spending on goods and services by local, state, and federal governments (except for transfer payments),")
            st.markdown("* **Net exports (NX)**: Exports minus Imports (E - I)")
            
            st.subheader("**4. Nominal GDP versus Real GDP**")
            st.markdown("* **Nominal GDP** values the production of goods and services at **current prices**")
            st.markdown("* **Real GDP** values the production of goods and services at **constant prices**")
            st.success("**       REAL GDP (2021) = PRICE (BASE YEAR) x QUANTITY (2021)**")
            st.error("**       NOMINAL GDP (2021) = PRICE (2021)  x  QUANTITY (2021)**")

            st.subheader("**5. GDP as a measure of welfare**")
            st.markdown("* *assess* the economic well-being of a country: using **GDP per capita**")
            st.markdown("* *compare* living standards in different countries: using **GDP (PPP)/Purchasing Power Parity per capita**")
            st.markdown("* *identify* economic growth trends")
            st.markdown("* *predict* and prevent recessions")
            st.image("https://github.com/maixbach/python_project_mxbach_dseb_neu/blob/main/hanoi_gdp.jpg?raw=true", width = 1000)
            
            st.subheader("**PROBLEM SOLVING: **")
            
            #Display the PROBLEM SOLVING section:
            if option_of_prod_income == "GDP calculator":
               st.subheader("* GDP calculator*")
               allof_firm_A = input_firm_info("A")
               allof_firm_B = input_firm_info("B")
               if allof_firm_A[5]:
                   if allof_firm_B[5]:
                       allof_firm_A_lst = list(allof_firm_A)
                       allof_firm_B_lst = list(allof_firm_B)
                       
                       for i in range(len(allof_firm_A_lst)):
                           allof_firm_A_lst[i] = float(allof_firm_A_lst[i])
                       for i in range(len(allof_firm_B_lst)):
                           allof_firm_B_lst[i] = float(allof_firm_B_lst[i])
                                
                       profit_firm_A = allof_firm_A_lst[0] - allof_firm_A_lst[4] - allof_firm_A_lst[5]
                       profit_firm_B = allof_firm_B_lst[0] - allof_firm_B_lst[4] - allof_firm_B_lst[5]
                           
                       if allof_firm_B_lst[0] != (allof_firm_B_lst[1] + allof_firm_B_lst[2]):
                           st.error("Total revenue must be sum of revenue get from final goods & revenue from selling to the other. Please re-enter at firm B")
                       
                       if allof_firm_A_lst[0] != (allof_firm_A_lst[1] + allof_firm_A_lst[2]):
                           st.error("Total revenue must be sum of revenue get from final goods & revenue from selling to the other. Please re-enter at firm A")
                       if allof_firm_A_lst[2] != allof_firm_B_lst[5]:
                           st.error("The intermediate goods of firm A must be equals to Cost of firm B")
                       elif allof_firm_A_lst[5] != allof_firm_B_lst[2]:
                           st.error("The intermediate goods of firm B must be equals to Cost of firm A")
                       else:
                           expenditure_cal = allof_firm_A_lst[1] + allof_firm_A_lst[3] + allof_firm_B_lst[1] + allof_firm_B_lst[3]
                           st.markdown("* **Expenditure (final goods) approach: {} + {} + {} + {} = {}**".format(allof_firm_A_lst[1], allof_firm_A_lst[3], allof_firm_B_lst[1], allof_firm_B_lst[3], expenditure_cal))
                           
                           value_added_cal = allof_firm_A_lst[0] + allof_firm_A_lst[3] - allof_firm_A_lst[5] + allof_firm_B_lst[0] + allof_firm_B_lst[3] - allof_firm_B_lst[5]
                           st.markdown(f"* **Value-added approach: {allof_firm_A_lst[0]} + {allof_firm_A_lst[3]} - {allof_firm_A_lst[5]} + {allof_firm_B_lst[0]} + {allof_firm_B_lst[3]} - {allof_firm_B_lst[5]} = {value_added_cal} **")
                           
                           income_cal = allof_firm_A_lst[4] + profit_firm_A + allof_firm_A_lst[3] + allof_firm_B_lst[4] + profit_firm_B + allof_firm_B_lst[3]
                           st.markdown(f"* **Income approach: {allof_firm_A_lst[4]} + {profit_firm_A} + {allof_firm_A_lst[3]} + {allof_firm_B_lst[4]} + {profit_firm_B} + {allof_firm_B_lst[3]} = {income_cal} **")
            
            if option_of_prod_income == "Economic growth rate":
               st.subheader("* Calculate economic growth rate (year t) (%): *")
               st.latex(r""" \left( \frac{{{GDP}_t}^{real}}{{{GDP}_{t-1}}^{real}} - 1 \right) * 100 \%""")
               
               real_gdp_t = enter_real_gdp("year")
               real_gdp_t_1 = enter_real_gdp("previous year")
               if real_gdp_t:
                   if real_gdp_t_1:
                       real_gdp_t = float(real_gdp_t)
                       real_gdp_t_1 = float(real_gdp_t_1)
                       
                       econ_growth_rate_cal = ((real_gdp_t / real_gdp_t_1) - 1) * 100
                       st.markdown("*RESULT:*")
                       st.markdown(f"** {econ_growth_rate_cal} **")
                       
            if option_of_prod_income == "Economic growth rate over time":
               st.subheader("* Calculate economic growth rate over time (%): *")
               st.latex(r""" \left( \left({\frac{{GDP}_{last}}{{GDP}_{first} }} \right)^{\frac{1}{n}} - 1  \right) * 100 \%""")
               
               last_year = st.sidebar.text_input("Last year")
               first_year = st.sidebar.text_input("First year")
               real_gdp_t = enter_real_gdp("last year")
               real_gdp_t_1 = enter_real_gdp("first year")
               
               if real_gdp_t and real_gdp_t_1 and last_year and first_year:
                   last_year = int(last_year)
                   first_year = int(first_year)
                   real_gdp_t = float(real_gdp_t)
                   real_gdp_t_1 = float(real_gdp_t_1)
                   
                   econ_growth_rate_cal = ((real_gdp_t / real_gdp_t_1)**(1 / (last_year - first_year)) - 1) * 100
                   st.markdown("*RESULT:*")
                   st.markdown(f"** {econ_growth_rate_cal} **")
                       
            if option_of_prod_income == "GDP deflator & Inflation":
                st.subheader("* Calculate GDP deflator (year t) (%): *")
                st.latex(r""" \left( \frac{{{GDP}_t}^{nominal}}{{{GDP}_{t}}^{real}} \right) * 100  """)
                
                real_gdp_t = enter_real_gdp("year")
                real_gdp_t_1 = enter_real_gdp("previous year")
                nominal_gdp_t = enter_nominal_gdp("year")
                nominal_gdp_t_1 = enter_nominal_gdp("previous year")
                
                if real_gdp_t and real_gdp_t_1 and nominal_gdp_t and nominal_gdp_t_1:
                    real_gdp_t = float(real_gdp_t)
                    real_gdp_t_1 = float(real_gdp_t_1)
                    nominal_gdp_t = float(nominal_gdp_t)
                    nominal_gdp_t_1 = float(nominal_gdp_t_1)
                    
                    gdp_deflator_t = (nominal_gdp_t / real_gdp_t) * 100
                    gdp_deflator_t_1 = (nominal_gdp_t_1 / real_gdp_t_1) * 100
                    st.markdown("*RESULT:*")
                    st.markdown("** GDP DEFLATOR OF YEAR t: **")
                    st.markdown(f"** {gdp_deflator_t} **")
                    st.markdown("** GDP DEFLATOR OF YEAR t-1: **")
                    st.markdown(f"** {gdp_deflator_t_1} **")
                    
                    st.subheader("* Calculate growth of price index - inflation rate (year t) (%): *")
                    st.latex(r""" \left( \frac{{{D}_t}^{GDP}}{{{D}_{t-1}}^{GDP}} - 1 \right) * 100 \%""")
                    growth_price_index = ((gdp_deflator_t / gdp_deflator_t_1) - 1) * 100
                    st.markdown("*RESULT:*")
                    st.markdown(f"** {growth_price_index} **")
###################################################################################################
####                                CHAPTER: CPI & INFLATION RATE                              ####
################################################################################################# 
        
 
        if option_of_solver == "Consumer price index & Inflation rate":
            option_of_cpi_infla = st.sidebar.radio("Choose problem: ", ["Consumer price index", "Inflation", "Wage bargain", "Interest rate"])
            
            #Display the main contents of this chapter
            st.header("**Consumer price index (CPI) & Inflation rate**")
            
            st.subheader("**1. Cost of living: Inflation rate**")
            st.write('**Inflation** refers to a situation in which the **economy’s overall price level** is **consistently rising overtime.** The inflation rate is the **percentage change** in the price level from the previous period.')
            st.write('**Examples: **')
            st.error("* Price of pork rises a lot while prices of other goods stays the same: **NOT INFLATION (NOT OVERALL PRICE RISES)**")
            st.error("* During Tet holiday, prices of goods rises but after holiday, prices reduce back to normal: **NOT INFLATION (NOT CONSISTENLY RISING)**")
            
            st.subheader("**2. Consumper price index**")
            st.markdown("This index measures **changes in prices of a fixed basket** of goods – a collection of items chosen to represent the purchasing pattern of a **typical consumer** – in **current year** relative to **base year**.")
            st.image("https://github.com/maixbach/python_project_mxbach_dseb_neu/blob/main/cpi_market.jpg?raw=true", width = 1000)
            
            st.subheader("**3. Problems in measuring CPI**: overestimate the actual cost of living")
            st.markdown("* **Substitution bias** ")
            st.markdown("* **Introduction of new goods**")
            st.markdown("* **Unmeasured quality changes**")
            
            st.subheader("**4. Difference in computing Inflation by GDP Deflator vs CPI**")
            st.markdown("* **GDP Deflator**: **produced domestically**")
            st.markdown("* **Real GDP**: **bought by typical consumers**")
            st.write('**Examples: ** *If price of Iphone rises, what happens to the inflation rate:*')
            st.error("Calculated by *GDP deflator*: **UNAFFECTED** because Iphone is **produced abroad**")
            st.success("Calculated by *CPI*: **RISE** because Iphone belongs to **basket of consumption goods**")
            
            st.subheader("**PROBLEM SOLVING: **")
            
            #Display the PROBLEM SOLVING section:
            if option_of_cpi_infla == "Consumer price index":
               st.subheader("* Consumer price index*")
               
               no_of_components = st.sidebar.text_input("Number of components in basket")
               if no_of_components:
                   no_of_components = int(no_of_components)
                   
                   amount_of_components = []
                   for i in range(no_of_components):
                       amount_of_components.append(enter_numb_basket_component(i + 1))
                   price_base = []
                   price_current = []
                   for i in range(no_of_components):
                       price_base.append(enter_price_basket(i + 1, "base"))
                       price_current.append(enter_price_basket(i + 1, "current"))
                       
                   if price_base[-1] and price_current[-1]:
                       price_base = [float(item) for item in price_base]
                       price_current = [float(ite) for ite in price_current]
                       amount_of_components = [float(itemm) for itemm in amount_of_components]
                       
                       st.markdown("***Step 1:** **Fix the basket**: Determine which goods and services are most important to the typical consumer.")
                       for i in range(no_of_components):
                           st.write(f" **{amount_of_components[i]}** unit(s) of component {i+1}")
                    
                       st.markdown("***Step 2:** **Find the Prices**: Find the prices of each of the goods and services in the basket for each point in time.")
                       components = [f" Price of component {i}" for i in range(1, no_of_components + 1)]
                       df_prices = pd.DataFrame(list(zip(price_base, price_current)), columns = ["Base year", "Current year"], index = components)
                       st.table(df_prices)
                    
                       st.markdown("***Step 3:** **Compute the Basket’s Cost**: Use the data on prices to calculate the cost of the basket of goods and services at different times.")
                       st.latex(r""" Cost = \sum_{k=1}^{n}  {Price}_{k} * {Quantity}_{k}""")
                       price_of_basket_base_current = []
                       cost_basket_base = 0
                       for i in range(no_of_components):
                           cost_basket_base += (amount_of_components[i] * price_base[i])
                       cost_basket_cur = 0
                       for i in range(no_of_components):
                           cost_basket_cur += (amount_of_components[i] * price_current[i])
                       price_of_basket_base_current.append(cost_basket_base)
                       price_of_basket_base_current.append(cost_basket_cur)
                       st.markdown(f"* **Cost of basket in base year: {price_of_basket_base_current[0]} **")
                       st.markdown(f"* **Cost of basket in current year: {price_of_basket_base_current[1]} **")
                       
                       st.markdown("***Step 4:** **Compute CPI in year t**")
                       st.latex(r""" \left( \frac{{{price}_{CURRENT}}}{{{price}_{BASE}}} \right) * 100  """)
                       
                       cpi_cal = (price_of_basket_base_current[1] / price_of_basket_base_current[0]) * 100
                       
                       st.markdown("*RESULT:*")
                       st.markdown(f"** {cpi_cal} **")
                       
            if option_of_cpi_infla == "Inflation":
               st.subheader("* Inflation rate (%)*")
               st.latex(r""" \left( \frac{{{CPI}_t}}{{{CPI}_{t-1}}} - 1 \right) * 100 \%""")
               
               cpi_year_t = st.sidebar.text_input("CPI current year")
               cpi_year_t_1 = st.sidebar.text_input("CPI previous year")
               if cpi_year_t and cpi_year_t_1:
                   cpi_year_t = float(cpi_year_t)
                   cpi_year_t_1 = float(cpi_year_t_1)
                   infla_year_t = ((cpi_year_t / cpi_year_t_1) - 1) * 100
                   st.markdown("*RESULT:*")
                   st.markdown(f"** {infla_year_t} **")
          
            if option_of_cpi_infla == "Wage bargain":
               st.subheader("* Wage bargain*")
               st.markdown("""When signing the contract the previous time, you received **PREVIOUS WAGE**. 
                           Now, you're **asking the boss for higher wage**. The boss offer an **ASSUMING WAGE. Will you accept or deny?**""")
               st.markdown("We will compute the **GROWTH RATE** of **REAL WAGE** of assuming wage")
               st.success("* If the growth rate > 0: **ACCEPT**")
               st.error("* If the growth rate < 0: **DENY**")
               st.subheader("The growth rate of real wage = the growth rate of nominal wage – the inflation rate")
               
               nominal_wage_previous = st.sidebar.text_input("The previous wage")
               nominal_wage_now = st.sidebar.text_input("The assuming wage of boss offering")
               inflation_rate_input = st.sidebar.text_input("The inflation rate")
               if nominal_wage_previous and nominal_wage_now and inflation_rate_input:
                  nominal_wage_previous = float(nominal_wage_previous)
                  nominal_wage_now = float(nominal_wage_now)
                  inflation_rate_input = float(inflation_rate_input)
                  
                  growth_rate_nominal = ((nominal_wage_now / nominal_wage_previous) - 1) * 100
                  growth_rate_real = growth_rate_nominal - inflation_rate_input
                  
                  st.markdown("*ANSWER: **Real growth rate:** *")
                  st.markdown(f"** {growth_rate_real} **")
                  if growth_rate_real > 0:
                      st.success("**You may happy to accept this offer. New wage is actually higher than previous one**")
                  else:
                      st.error("**You should deny this offer. New wage is actually lower than previous one**")
                      
            if option_of_cpi_infla == "Interest rate":
               st.subheader("* Interest rate*")
               st.markdown("* **The nominal interest rate** is the interest rate usually reported and **not corrected** for inflation.")
               st.markdown("* **The real interest rate** is the interest rate that is **corrected** for the effects of inflation.")
               st.markdown("""When you borrow or lend money, you should think of the real interest rate. 
                           It tells us how many goods and services you can really purchase more from your lending/borrowring.""")
               
               st.success("* If the real interest rate **HIGHER THAN** nominal: **LENDER BENEFITS**")
               st.success("* If the real interest rate **LOWER THAN** nominal: **BORROWER BENEFITS**")
               st.subheader("Real interest rate = Nominal interest rate – Inflation rate")
               
               role = st.sidebar.text_input("Lender or Borrower?")
               nominal_interest_rate = st.sidebar.text_input("Nominal interest rate")
               inflation_rate_input = st.sidebar.text_input("The inflation rate")
               if nominal_interest_rate and inflation_rate_input and role:
                  nominal_interest_rate = float(nominal_interest_rate)
                  inflation_rate_input = float(inflation_rate_input)
                  
                  real_interest_rate = nominal_interest_rate - inflation_rate_input
                  
                  st.markdown("*ANSWER: **The real interest rate:** *")
                  st.markdown(f"** {real_interest_rate} **")
                  if (real_interest_rate > nominal_interest_rate) and (role.lower() == "lender"):
                      st.success(f"You benefit {abs(real_interest_rate - nominal_interest_rate)} percents!")
                  elif (real_interest_rate > nominal_interest_rate) and (role.lower() == "borrower"):
                      st.error(f"You actually lost {abs(real_interest_rate - nominal_interest_rate)} percents!")
                  elif (real_interest_rate < nominal_interest_rate) and (role.lower() == "borrower"):
                      st.success(f"You benefit {abs(real_interest_rate - nominal_interest_rate)} percents!")
                  else:
                      st.error(f"You actually lost {abs(real_interest_rate - nominal_interest_rate)} percents!")

###################################################################################################
####                                CHAPTER:UNEMPLOYMENT                             ####
#################################################################################################                        

        if option_of_solver == "Unemployment":
            option_of_unemploy = st.sidebar.radio("Choose problem: ", ["Unemployment & Labor-force participation rate"])
            
            #Display the main contents of this chapter
            st.header("**Unemployment**")
            
            st.subheader("**1. How is unemployment measured?**")
            st.write("Based on the answers to the survey questions, the BLS places each **adult** into **one of three categories**:")
            st.markdown("* **Employed**: who is in the **working-age** range and has spent **most of the previous week working** at a paid job. ")    
            st.markdown("* **Unemployed**: who is in the **working age** range and being on **temporary layoff**, is looking for a job, or is waiting for the start date of a new job. ")
            st.markdown("* **Not in the labor force**: who **fits neither of these categories**, such as a full-time student, homemaker, or retiree.")
            st.markdown("** The labor force = Number of employed + Number of unemployed**")
            
            st.subheader("**2. Categories of Unemployment**")
            st.markdown("* **The natural rate of unemployment**: It is the amount of unemployment that the economy **normally experiences.**")    
            st.markdown("* **The cyclical rate of unemployment**: It refers to the **year-to-year fluctuations** in unemployment around its natural rate.")
            
            st.subheader("*2 types of Natural rate of unemployment:*")
            st.success("* **Frictional unemployment**: occurs with the normal workings of the economy, such as workers taking time to **search for suitable jobs** and firms taking time to **search for qualified employees**")    
            st.error("* **Structural unemployment**: occurs due to **structural imbalance** in the labor market. Prevailing wage exceeds the equilibrium level, so the number of labors supplied exceed the number of labors demanded")
 
            st.subheader("*Causes of structural unemployed:*")
            st.markdown("* **Minimum-wage law**")    
            st.markdown("* **Trade union**") 
            st.markdown("* **Efficiency wage theory**") 
            
            st.image("https://github.com/maixbach/python_project_mxbach_dseb_neu/blob/main/employment.jpg?raw=true", width = 1000)
            
            st.subheader("**3. Public Policy and Job Search**")
            st.write("Government programs can **affect the time** it takes unemployed workers to find new jobs:")
            st.markdown("* **Government-run employment agencies**: give out information about job vacancies in order to **match workers and jobs more quickly**.")
            st.markdown("* **Public training programs**: **ease the transition of workers** from declining to growing industries and to help disadvantaged groups escape poverty.")
            st.markdown("* **Unemployment insurance**: a government program that partially **protects workers’ incomes** when they become unemployed. ")

            st.subheader("**PROBLEM SOLVING: **")
            
            #Display the PROBLEM SOLVING section:
            if option_of_unemploy == "Unemployment & Labor-force participation rate":
               st.subheader("* Unemployment & Labor-force participation rate*")
               
               st.subheader("**Unemployment rate = (No of unemployed / Labor force) * 100 (%)**")
               st.subheader("**Labor-force participation rate = (Labor force / Adult population) * 100 (%)**")
               #image of employment flow
               st.image("https://github.com/maixbach/python_project_mxbach_dseb_neu/blob/main/LabourMarketFlows.png?raw=true", width = 300)
               info_of_employ_previousy = enter_info_employment_year("previous")
               
               if info_of_employ_previousy[-1]:
                   info_of_employ_previousy = list(info_of_employ_previousy)
                   for i in range(len(info_of_employ_previousy)):
                       info_of_employ_previousy[i] = int(info_of_employ_previousy[i])
                   labor_force = info_of_employ_previousy[0] + info_of_employ_previousy[1]
                   aldult_pop = sum(info_of_employ_previousy)
                   unemploy_rate = (info_of_employ_previousy[1] / labor_force) * 100
                   labor_force_part_rate = (labor_force / aldult_pop) * 100
                    
                   st.markdown("*ANSWER:*")
                   st.markdown(f"* ** Unemployment rate previous year: {unemploy_rate} % **")
                   st.markdown(f"* ** Labor-force participation rate previous year: {labor_force_part_rate} % **")

                   update_info_thisy = update_info_employment_this_year()
                   if update_info_thisy[-1]:
                       update_info_thisy = list(update_info_thisy)
                       for i in range(len(update_info_thisy)):
                           update_info_thisy[i] = int(update_info_thisy[i])
                       
                       new_employ = info_of_employ_previousy[0] + update_info_thisy[0] - (update_info_thisy[1] + update_info_thisy[2])
                       st.markdown(f"* ** New no of employed = {info_of_employ_previousy[0]} + {update_info_thisy[0]} - ({update_info_thisy[1]} + {update_info_thisy[2]}) = {new_employ} **")
                       new_labor_force = labor_force + update_info_thisy[3] - update_info_thisy[4]
                       st.markdown(f"* ** New labor force = {labor_force} + {update_info_thisy[3]} - {update_info_thisy[4]} = {new_labor_force} **")
                       new_unemploy = new_labor_force - new_employ
                       st.markdown(f"* ** New no of unemployed = {new_unemploy}**")
                       new_aldult_pop = aldult_pop + update_info_thisy[5]
                       st.markdown(f"* ** New no of aldult population = {new_aldult_pop}**")
                       
                       new_unemploy_rate = (new_unemploy / new_labor_force) * 100
                       new_labor_force_part_rate = (new_labor_force / new_aldult_pop) * 100
                       
                       st.markdown(f"* ** Unemployment rate THIS year: {new_unemploy_rate} % **")
                       st.markdown(f"* ** Labor-force participation rate THIS year: {new_labor_force_part_rate} % **")

###################################################################################################
####                                CHAPTER: MONEYTARY SYSTEM                             ####
#################################################################################################
        
        if option_of_solver == "Monetary system":
            option_of_money_system = st.sidebar.radio("Choose problem: ", ["Money supply calculator", "Monetary policy recommendation"])
            
            #Display the main contents of this chapter
            st.header("**Moneytary system**")
            
            st.subheader("**1. Money**")
            st.write("Money is **any items** that are **regularly used** in economic transactions or exchanges and **accepted by buyers and sellers.**")
            st.write('**Examples: **')
            money1, money2 = st.columns(2)
            with money1:
                st.image("https://github.com/maixbach/python_project_mxbach_dseb_neu/blob/main/cash_in_wallet.jpg?raw=true", width = 300)
                st.markdown("**Cash in wallet** is money.")
            with money2:
                st.image("https://github.com/maixbach/python_project_mxbach_dseb_neu/blob/main/shares_SHS.jpg?raw=true", width = 300)
                st.markdown("**Shares of SHS** is *not* money. ")
            
            st.subheader("**2. History of money**")
            barter, commodity, gold, fiat = st.columns(4)
            with barter:
                st.error("**Barter**: Exchange of one good or service for another.")
            with commodity:
                st.error("**Commodity money**: Actual money is a commodity: Shells, metal coins, gold, silver. ")
            with gold:
                st.error("**Gold standard**: Paper money is backed up by gold")
            with fiat:
                st.error("**Fiat money**: Money has no intrinsic value but is backed by governmentwith")
            st.image("https://github.com/maixbach/python_project_mxbach_dseb_neu/blob/main/jason-leung-SAYzxuS1O3M-unsplash.jpg?raw=true", width = 1000)
          
            st.subheader("**3. Three properties of money**")
            st.write("* **Medium of exchange**")
            st.write("* **Unit of account**")
            st.write("* **Store of value**")
            
            st.subheader("**4. Measurements of money supply**")
            st.write("* **M1**: sum of currency in the hands of the public **(Cu)**, demand deposits, other checkable deposits, and traveler’s check **(D)**")
            st.write("* **M2**: M1 plus other assets, including deposits in savings and loans account and money market mutual funds")
            
            st.subheader("**5. How banks create money?**")
            st.caption("Watch this video below from **mru.org** to fully understand")
            st_player("https://youtu.be/93_Va7I7Lgg")
            
            st.subheader("**PROBLEM SOLVING: **")
            
            #Display the PROBLEM SOLVING section:
            if option_of_money_system == "Money supply calculator":
               st.subheader("* Money supply calculator*")
               st.markdown("* **Reserve ratio**: the **fraction of deposits** that banks hold as **reserves**")
               st.markdown("* **Money multiplier**: The amount of money the banking system **generates** with each dollar of reserves")
               
               st.success("**Money supply = Monetary base * Money multiplier**".upper())
               st.success("**Money multiplier = 1 / Reserve ratio**".upper())
               
               info_of_base_rsratio = base_and_reserve_ratio_input()
               
               if info_of_base_rsratio[-1]:
                    info_of_base_rsratio = list(info_of_base_rsratio)
                    for i in range(len(info_of_base_rsratio)):
                        info_of_base_rsratio[i] = float(info_of_base_rsratio[i])
                    
                    money_supply_cal = info_of_base_rsratio[0] * (1 / info_of_base_rsratio[1])
                    st.markdown("*ANSWER:  *")
                    st.markdown(f"* **Money supply ($): {info_of_base_rsratio[0]} * (1 / {info_of_base_rsratio[1]}) = {money_supply_cal} **")
                   
            if option_of_money_system == "Monetary policy recommendation":
               st.subheader("* Tools of monetary control: **How to increase money supply?** *")
               st.markdown("* **Open-market operations** (most prefered): **buys government bonds (increase MS)** from or sells government bonds (decrease MS) to the public")
               st.markdown("* **Changing the reserve requirement**: regulations on the **minimum amount of reserves** that banks must hold against deposits. **The lower reserve requirements, the more money supply**")
               st.markdown("* **Changing the discount rate**: The discount rate is the interest rate the **Central Bank charges banks for loans**. **The lower Discount rate, the more money supply**")
               st.success("**Change in Money supply = Change in Monetary base * Money multiplier**".upper())
               st.markdown("*Answer:* ")
               option_of_change = st.sidebar.radio("Change money supply: ", ["Increase", "Decrease"])
               option_toolbox = st.sidebar.radio("Tool box: ", ["Open-market operations", "Changing the reserve requirement"])
               amount_change = st.sidebar.text_input("Amount of money supply to change")
               curr_reserve_require = st.sidebar.text_input("Current reserve requirement")
               
               if amount_change and curr_reserve_require:
                   amount_change = float(amount_change)
                   curr_reserve_require = float(curr_reserve_require)
                   
                   if option_toolbox == "Open-market operations":
                       delta_base = amount_change / (1 / curr_reserve_require)
                       if option_of_change == "Increase":
                           st.markdown(f"** Central Bank should *buy government bonds* worthing {delta_base} to {option_of_change} money supply. **")
                       else:
                           st.markdown(f"** Central Bank should *sell government bonds* worthing {delta_base} to {option_of_change} money supply. **")
                       
                   if option_toolbox == "Changing the reserve requirement":
                       current_base = st.sidebar.text_input("Current base money")
                       if current_base:
                           current_base = float(current_base)
                           current_MS = current_base * (1 / curr_reserve_require)
                           if option_of_change == "Increase":
                               new_MS = current_MS + amount_change
                               new_RR = 1 / (new_MS / current_base)
                               new_RR = new_RR * 100
                               st.markdown(f"** Central Bank should *lower reserve requirement* to {new_RR} % to {option_of_change} money supply. **")
                           else:
                               new_MS = current_MS - amount_change
                               new_RR = 1 / (new_MS / current_base)
                               new_RR = new_RR * 100
                               st.markdown(f"** Central Bank should *increase reserve requirement* to {new_RR} %  to {option_of_change} money supply. **")
                           







