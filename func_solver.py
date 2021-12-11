# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 11:38:31 2021

@author: Administrator
"""
import streamlit as st

def input_firm_info(firm):
    """Enter the information of revenue, inventory, wage, cost of any firm"""
    revenue_total = st.sidebar.text_input(f"Total revenue of firm {firm}")
    revenue_from_total = st.sidebar.text_input(f"Final goods of firm {firm}")
    revenue_to_the_other = st.sidebar.text_input(f"Intermediate goods to the other of firm {firm}")
    inventory = st.sidebar.text_input(f"Inventory of firm {firm}")
    wage = st.sidebar.text_input(f"Wage for employees of firm {firm}")
    material_cost = st.sidebar.text_input(f"Cost of firm {firm}")
    
    info_tup = (revenue_total, revenue_from_total, revenue_to_the_other, inventory, wage, material_cost)
    return info_tup

def enter_real_gdp(year):
    real_gdp = st.sidebar.text_input(f"Real GDP in {year}")
    return real_gdp
def enter_nominal_gdp(year):
    nominal_gdp = st.sidebar.text_input(f"Nominal GDP in {year}")
    return nominal_gdp

def enter_numb_basket_component(STT):
    STT = str(STT)
    component = st.sidebar.text_input(f"The number of each basket component {STT}")
    return component
def enter_price_basket(compo, year):
    compo = str(compo)
    price = st.sidebar.text_input(f"Price of component {compo} in {year} year")
    return price

def enter_info_employment_year(year):
    employ = st.sidebar.text_input(f"Number of employed in {year} year")
    unemploy = st.sidebar.text_input(f"Number of unemployed in {year} year")
    not_lbforce = st.sidebar.text_input(f"Number of people not in labor force in {year} year")
    return employ, unemploy, not_lbforce
def update_info_employment_this_year():
    hire_recalls = st.sidebar.text_input("Hire and recalls during this year")   
    job_losers = st.sidebar.text_input("Job losers during this year") 
    job_leavers = st.sidebar.text_input("Job leavers during this year") 
    entrants = st.sidebar.text_input("Entrants during this year") 
    withdrawals = st.sidebar.text_input("Withdrawals during this year") 
    delta_working_age_pop = st.sidebar.text_input("New change of working-age population during this year") 
    return (hire_recalls, job_losers, job_leavers, entrants, withdrawals, delta_working_age_pop)

def base_and_reserve_ratio_input():
    base_money = st.sidebar.text_input("Monetary base")
    reserve_ratio = st.sidebar.text_input("Reserve ratio")
    return base_money, reserve_ratio

def enter_no_of_rows_and_cols(mat):
    """Enter the number of rows and columns of a matrix"""
    row = st.sidebar.text_input(f"Enter number of rows in matrix {mat}")
    col = st.sidebar.text_input(f"Enter number of columns in matrix {mat}")
    return row, col