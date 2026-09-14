import streamlit as st 

from src.zombie_carlo.model import ZombieSIR

st.title("Zombie Carlo Simulator")


model = ZombieSIR()

model.run_simulation()
results = model.run_monte_carlo()

st.write(results)