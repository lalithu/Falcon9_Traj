import numpy as np
from scipy.integrate import odeint

import plotly.graph_objects as go
from plotly.graph_objs import Scatter

# import chart_studio
# import chart_studio.plotly as py

# username = 'lalithuriti'
# api_key = 'WkltoYNWP7gEy8eWuRUI'
# chart_studio.tools.set_credentials_file(username=username, api_key=api_key)

# Constants
G = 6.67408 * 10 ** -11  # m^3 kg^-1 s^-2
M_Earth = 5.972 * 10 ** 24  # kg
R = 6378.137  # km

g = (G * M_Earth) / ((R * 1000) ** 2)  # m s^-2 | 9.797686073547649

m_c_dragon = 28184  # kg

m_s_2_dry = 3900  # kg
m_s_2_propellant = 105189  # kg
m_stage_2 = m_s_2_dry + m_s_2_propellant  # kg | 96570
isp_s_2 = 348  # s
ve_s_2 = isp_s_2 * g  # m s^-1 | 3409.5947535945816
t_burn_s_2 = 397  # s
thrust_s_2 = 934000  # N
m_dot_s_2 = thrust_s_2 / ve_s_2  # kg s^-1 | 273.93284759584

m_s_1_dry = 25600  # kg
m_s_1_propellant = 395700  # kg
m_stage_1 = m_s_1_dry + m_s_1_propellant  # kg | 421300
isp_s_1 = 282  # s
ve_s_1 = isp_s_1 * g  # m s^-1 | 2762.9474727404368
t_burn_s_1 = 162  # s
thrust_s_1 = 7607000  # N
m_dot_s_1 = thrust_s_1 / ve_s_1  # kg s^-1 | 2753.219188946425

t_coast = 1250  # s


def stage_1(state_var_launch, t):
    h, v = state_var_launch

    thrust = m_dot_s_1 * ve_s_1

    M = m_stage_1 + m_stage_2 + m_c_dragon
    m = t * m_dot_s_1

    thrust_acc = thrust / (M - m) / 1000
    g = - (G * M_Earth) / ((h * 1000) ** 2) / 1000 * np.sin(90)

    dvdt = thrust_acc + g  # - (.3 * 0.25 * 200) / (M - m)

    return [v, dvdt]


def stage_2(state_var_s_2_ignition, t):
    h, v = state_var_s_2_ignition

    thrust = m_dot_s_2 * ve_s_2

    M = m_stage_2 + m_c_dragon
    m = (t - t_burn_s_1) * m_dot_s_2

    thrust_acc = thrust / (M - m) / 1000
    g = - (G * M_Earth) / ((h * 1000) ** 2) / 1000

    dvdt = thrust_acc + g  # - (.3 * 0.25 * 200) / (M - m)

    return [v, dvdt]


def coast_traj(state_var_c_dragon_separation, t):
    h, v = state_var_c_dragon_separation

    g = - (G * M_Earth) / ((h * 1000) ** 2) / 1000

    dvdt = g  # - (.3 * 0.25 * 200) / (M - m)

    return [v, dvdt]


# Launch
state_var_launch = [6378.1, 0.0]  # [km, km h^-1]

t_s_1 = np.linspace(0, t_burn_s_1, 101)

stage_1 = odeint(stage_1, state_var_launch, t_s_1)

h_stage_1, v_stage_1 = stage_1.T
print(h_stage_1)


# Stage 2 Ignition
state_var_s_2_ignition = [h_stage_1[-1], v_stage_1[-1]]  # [km, km h^-1]

t_s_2 = np.linspace(t_s_1[-1], t_s_1[-1] + t_burn_s_2, 101)

stage_2 = odeint(stage_2, state_var_s_2_ignition, t_s_2)

h_stage_2, v_stage_2 = stage_2.T
print(h_stage_2)


# Crew Dragon Separation & ISS Approach
state_var_c_dragon_separation = [h_stage_2[-1], v_stage_2[-1]]  # [km, km h^-1]

t_coast_traj = np.linspace(t_s_2[-1], t_s_2[-1] + t_coast, 101)

coast_traj = odeint(coast_traj, state_var_c_dragon_separation, t_coast_traj)

h_coast_traj, v_coast_traj = coast_traj.T
print(h_coast_traj)


# Altitude(t)
alt_plot_objects = []

alt_s_1 = go.Scatter(
    x=t_s_1,
    y=h_stage_1 - R,
    name="Stage 1")

alt_plot_objects.append(alt_s_1)

alt_s_2 = go.Scatter(
    x=t_s_2,
    y=h_stage_2 - R,
    name="Stage 2")

alt_plot_objects.append(alt_s_2)

alt_coast = go.Scatter(
    x=t_coast_traj,
    y=h_coast_traj - R,
    name="Coast")

alt_plot_objects.append(alt_coast)

alt_layout = go.Layout(
    title='Falcon 9 Altitude by Time',
    xaxis=dict(title='Time (s)'),
    yaxis=dict(title='Altitude (km)'))

alt_Falcon9_Traj = go.Figure(data=alt_plot_objects, layout=alt_layout)

alt_Falcon9_Traj.update_layout(height=400)

alt_Falcon9_Traj.show()


# Velocity(t)
v_plot_objects = []

v_s_1 = go.Scatter(
    x=t_s_1,
    y=v_stage_1 * 3600,
    name="Stage 1")

v_plot_objects.append(v_s_1)

v_s_2 = go.Scatter(
    x=t_s_2,
    y=v_stage_2 * 3600,
    name="Stage 2")

v_plot_objects.append(v_s_2)

v_coast = go.Scatter(
    x=t_coast_traj,
    y=v_coast_traj * 3600,
    name="Coast")

v_plot_objects.append(v_coast)

v_layout = go.Layout(
    title='Falcon 9 Velocity by Time',
    xaxis=dict(title='Time (s)'),
    yaxis=dict(title='Velocity (km/h)'))

v_Falcon9_Traj = go.Figure(data=v_plot_objects, layout=v_layout)

v_Falcon9_Traj.update_layout(height=400)

v_Falcon9_Traj.show()


# Mass(t)
m_plot_objects = []

m_s_1 = go.Scatter(
    x=t_s_1,
    y=m_stage_1 + m_stage_2 + m_c_dragon - t_s_1 * m_dot_s_1,
    name="Stage 1")

m_plot_objects.append(m_s_1)

m_s_2 = go.Scatter(
    x=t_s_2,
    y=m_stage_2 + m_c_dragon - (t_s_2 - t_burn_s_1) * m_dot_s_2,
    name="Stage 2")

m_plot_objects.append(m_s_2)

m_coast = go.Scatter(
    x=t_coast_traj,
    y=m_c_dragon - t_coast_traj * 0,
    name="Coast")

m_plot_objects.append(m_coast)

m_layout = go.Layout(
    title='Falcon 9 Mass by Time',
    xaxis=dict(title='Time (s)'),
    yaxis=dict(title='Mass (kg)'))

m_Falcon9_Traj = go.Figure(data=m_plot_objects, layout=m_layout)

m_Falcon9_Traj.update_layout(height=400)

m_Falcon9_Traj.show()


'''
Falcon 9 v1.2 Full Thrust

Stage 1
- Thrust(Sea Level): 7,607 kN
- Thrust(Vacuum): 8,227 kN
- Specific Impulse: 282 s
- Dry Mass: 25,600 kg
- Propellant Mass: 395,700 kg

- Initial Mass: 421,300 kg
- Final Mass: 25,600 kg

- ISP = Ve / g
- Ve = ISP · g
- Ve = 282 · 9.807 = 2,765.574 m/s = 2.765574 km/s

Falcon9 v1.2 Stage 1 (7.75, 16.46)

- ∆V Stage 1 =  7.75 km/s = 27,900 km/h = 17,336.256 m/h
- Mass Ratio = 16.46

Stage 2
- Thrust: 934 kN
- Specific Impulse: 348 s
- Dry Mass: 3, 900 kg
- Propellant Mass: 92, 670 kg

- Initial Mass: 96, 570 kg
- Final Mass: 3, 900 kg

- ISP = Ve / g
- Ve = ISP · g
- Ve = 348 · 9.807 = 3, 412.836 m/s = 3.412836 km/s

Falcon9 v1.2 Stage 2 (10.95, 24.76)

- ∆V Stage 2 = 10.95 km/s = 39, 420 km/h = 24, 494.452 m/h
- Mass Ratio = 24.76

'''
