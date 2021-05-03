import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

'''
def firstorder(y, t):
    tau = 5.0
    K = -2.0
    u = 1.0

    dydt = (-y + K * u) / tau

    return dydt


y = odeint(firstorder, 0, [0, 10])
print(y)
'''

'''
# This is the Diffrential Equation Model, like where it solves for y(t)


def model(y, t):
    k = 0.3
    dydt = -k * y
    return dydt


# Initial Condition,
# When we're defining y0, we're really defining the value
# of the solution function y(t) at the first input
# value/moment t that the model is being integrated upon to be solved
y_of_0 = 5

# the time interval
t = np.linspace(0, 20, 20)
print(t)

y = odeint(model, y_of_0, t)
print(y)

plt.plot(t, y)
plt.xlabel('time')
plt.ylabel('y(t)')

plt.show()

'''
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

'''

# Constants
G = 6.67408 * 10 ** -11  # m^3 kg^-1 s^-2
M_Earth = 5.972 * 10 ** 24  # kg
# print(G * M_Earth)
R = 6378.137  # km

g = (G * M_Earth) / ((R * 1000) ** 2)  # m s^-2
# print(g)

m_stage_1 = 422000  # kg
m_dot_s_1 = 2312.5  # kg/s
ve_s_1 = 2943  # m/s
t_burn_s_1 = 160

m_stage_2 = 128000  # kg
m_dot_s_2 = 270  # kg/s
ve_s_2 = 3433.5  # m/s
t_burn_s_2 = 400

ISS_approach = 1000


def stage_1(state_var_launch, t):
    h, v = state_var_launch

    thrust = m_dot_s_1 * ve_s_1

    M = m_stage_1 + m_stage_2
    m = t * m_dot_s_1

    thrust_acc = thrust / (M - m) / 1000
    g = - (G * M_Earth) / ((h * 1000) ** 2) / 1000

    dvdt = thrust_acc + g  # - (.3 * 0.25 * 200) / (M - m)

    return [v, dvdt]


def stage_2(state_var_s_2_ignition, t):
    h, v = state_var_s_2_ignition

    thrust = m_dot_s_2 * ve_s_2

    M = m_stage_2
    m = (t - 160) * m_dot_s_2

    thrust_acc = thrust / (M - m) / 1000
    g = - (G * M_Earth) / ((h * 1000) ** 2) / 1000

    dvdt = thrust_acc + g  # - (.3 * 0.25 * 200) / (M - m)

    return [v, dvdt]


def leo_traj(state_var_c_dragon_separation, t):
    h, v = state_var_c_dragon_separation

    g = - (G * M_Earth) / ((h * 1000) ** 2) / 1000

    dvdt = g  # - (.3 * 0.25 * 200) / (M - m)

    return [v, dvdt]


# Launch
state_var_launch = [6378.1, 0.0]  # [km, m/s]

t_s_1 = np.linspace(0, t_burn_s_1)

stage_1 = odeint(stage_1, state_var_launch, t_s_1)

h_stage_1, v_stage_1 = stage_1.T
print(h_stage_1)


# Stage 2 Ignition
state_var_s_2_ignition = [h_stage_1[-1], v_stage_1[-1]]

t_s_2 = np.linspace(t_s_1[-1], t_s_1[-1] + t_burn_s_2)

stage_2 = odeint(stage_2, state_var_s_2_ignition, t_s_2)

h_stage_2, v_stage_2 = stage_2.T
print(h_stage_2)


# Crew Dragon Separation & ISS Approach
state_var_c_dragon_separation = [h_stage_2[-1], v_stage_2[-1]]

t_leo_traj = np.linspace(t_s_2[-1], t_s_2[-1] + ISS_approach)

leo_traj = odeint(leo_traj, state_var_c_dragon_separation, t_leo_traj)

h_leo_traj, v_leo_traj = leo_traj.T
print(h_leo_traj)


plt.figure()

plt.subplot(2, 1, 1)
plt.plot(t_s_1, h_stage_1 - R)
plt.plot(t_s_2, h_stage_2 - R)
plt.plot(t_leo_traj, h_leo_traj - R)
plt.xlabel('time')
plt.ylabel('h(t)')

plt.subplot(2, 1, 2)
plt.plot(t_s_1, v_stage_1 * 3600)
plt.plot(t_s_2, v_stage_2 * 3600)
plt.plot(t_leo_traj, v_leo_traj * 3600)
plt.xlabel('time')
plt.ylabel('v(t)')


plt.show()

'''
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
