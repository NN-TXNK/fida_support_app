
import streamlit as st
import numpy as np

st.title('FIDA Support App')

col1, col2 = st.columns(2)

with col1:
    st.header('Capillary Dimensions')
    dc = st.text_input('Capillary Diameter (uM)', 75)
    dc = float(dc)*1e-6
    rc = dc*0.5

    L = st.text_input('Capillary Length (cm)', 100)
    L = float(L)*1e-2

    length_to_detector = st.text_input('Length to detector (cm)', 84)
    length_to_detector = float(length_to_detector)*1e-2


def lookup_viscosity(temp):
    #https://wiki.anton-paar.com/dk-en/water/
    #temp  : dynamic_viscosity [mPa.s],  density [g/cm³]
    water_dict = {2: [1.6735, 0.9999], 3: [1.619, 1.0], 4: [1.5673, 1.0], 5: [1.5182, 1.0], 6: [1.4715, 0.9999], 7: [1.4271, 0.9999], 8: [1.3847, 0.9999], 9: [1.3444, 0.9998], 10: [1.3059, 0.9997], 11: [1.2692, 0.9996], 12: [1.234, 0.9995], 13: [1.2005, 0.9994], 14: [1.1683, 0.9992], 15: [1.1375, 0.9991], 16: [1.1081, 0.9989], 17: [1.0798, 0.9988], 18: [1.0526, 0.9986], 19: [1.0266, 0.9984], 20: [1.0016, 0.9982], 21: [0.9775, 0.998], 22: [0.9544, 0.9978], 23: [0.9321, 0.9975], 24: [0.9107, 0.9973], 25: [0.89, 0.997], 26: [0.8701, 0.9968], 27: [0.8509, 0.9965], 28: [0.8324, 0.9962], 29: [0.8145, 0.9959], 30: [0.7972, 0.9956], 31: [0.7805, 0.9953], 32: [0.7644, 0.995], 33: [0.7488, 0.9947], 34: [0.7337, 0.9944], 35: [0.7191, 0.994], 36: [0.705, 0.9937], 37: [0.6913, 0.9933], 38: [0.678, 0.993], 39: [0.6652, 0.9926], 40: [0.6527, 0.9922], 45: [0.5958, 0.9902], 50: [0.5465, 0.988], 55: [0.5036, 0.9857], 60: [0.466, 0.9832], 65: [0.4329, 0.9806], 70: [0.4035, 0.9778], 75: [0.3774, 0.9748], 80: [0.354, 0.9718]}
    viscosity = water_dict[temp][0] * 1e-3        #from mPa.s to Pa.s
    density = water_dict[temp][1] * 1e3           #from g/cm3 to kg/m3
    return viscosity, density
with col2:

    st.header('Conditions')
    temp = st.slider('Select a temperature', 2, 39, 25, 1)
    viscosity_standard = st.radio('Can viscosity be assumed to be equal to that of water?', ['Yes', 'No'], 0, horizontal = True)
    if viscosity_standard == 'Yes':
        viscosity, density = lookup_viscosity(temp)
        st.write(' ')
        st.write(' ')
        st.write('Visocsity is set to: {0} (Pa.s)'.format(round(viscosity, ndigits=5)))
    if viscosity_standard == 'No':
        viscosity = st.text_input('Viscosity (Pa.s)', 0.00089)
        viscosity = float(viscosity)








### Flow rate


st.divider()
st.header(' ')
st.header('Method flow rates')

def cal_flow_rate(pressure, time, radius, viscosity, length):
    def HagenPoiseuille(pressure, radius, viscosity, length):
        #Volumetric flow rate
        Q = (pressure * 1e2 * np.pi * radius**4) / (8*viscosity* length) #1 mbar = 1e2 Pa
        return Q
        
    Q = HagenPoiseuille(pressure, radius, viscosity, length) #Volumetric flow rate (m^3/s      
    u = Q / (np.pi*radius**2) #Linear flow rate = volumetric flow rate / crossesctional area
    v = Q * time
    #self.reynolds = (self.density * u * self.rc*2) / self.viscosity

    return Q, u, v 

st.subheader('Flush NaOH:')
col1, col2 = st.columns(2)
with col1:
    p_flush_NaOH = st.text_input('Pressure (mbar)', 3500, key='1')
    p_flush_NaOH = float(p_flush_NaOH)
with col2:
    t_flush_NaOH = st.text_input('Time (s)', 45, key='2')
    t_flush_NaOH = float(t_flush_NaOH)
Q_flush_NaOH, u_flush_NaOH, v_flush_NaOH = cal_flow_rate(p_flush_NaOH, t_flush_NaOH, rc, viscosity, L)
col1, col2, col3 = st.columns(3)
with col1:
    st.write('Q = {0} nL/s'.format(round(Q_flush_NaOH*1e12,3)))
with col2:
    st.write('u = {0} mm/s'.format(round(u_flush_NaOH*1e3,3)))
with col3:
    st.write('v = {0} nL'.format(round(v_flush_NaOH*1e12,3)))


st.subheader('Flush Buffer:')
col1, col2 = st.columns(2)
with col1:
    p_flush_buff = st.text_input('Pressure (mbar)', 3500, key='3')
    p_flush_buff = float(p_flush_buff)
with col2:
    t_flush_buff = st.text_input('Time (s)', 75, key='4')
    t_flush_buff = float(t_flush_buff)
Q_flush_buff, u_flush_buff, v_flush_buff = cal_flow_rate(p_flush_buff, t_flush_buff, rc, viscosity, L)
col1, col2, col3 = st.columns(3)
with col1:
    st.write('Q = {0} nL/s'.format(round(Q_flush_buff*1e12,3)))
with col2:
    st.write('u = {0} mm/s'.format(round(u_flush_buff*1e3,3)))
with col3:
    st.write('v = {0} nL'.format(round(v_flush_buff*1e12,3)))


st.subheader('Flush Analyte:')
col1, col2 = st.columns(2)
with col1:
    p_flush_anal = st.text_input('Pressure (mbar)', 3500, key='5')
    p_flush_anal = float(p_flush_anal)
with col2:
    t_flush_anal = st.text_input('Time (s)', 20, key='6')
    t_flush_anal = float(t_flush_anal)
Q_flush_anal, u_flush_anal, v_flush_anal = cal_flow_rate(p_flush_anal, t_flush_anal, rc, viscosity, L)
col1, col2, col3 = st.columns(3)
with col1:
    st.write('Q = {0} nL/s'.format(round(Q_flush_anal*1e12,3)))
with col2:
    st.write('u = {0} mm/s'.format(round(u_flush_anal*1e3,3)))
with col3:
    st.write('v = {0} nL'.format(round(v_flush_anal*1e12,3)))


st.subheader('Inject Indicator:')
col1, col2 = st.columns(2)
with col1:
    p_inj_indi = st.text_input('Pressure (mbar)', 50, key='7')
    p_inj_indi = float(p_inj_indi)
with col2:
    t_inj_indi = st.text_input('Time (s)', 10, key='8')
    t_inj_indi = float(t_inj_indi)
Q_inj_indi, u_inj_indi, v_inj_indi = cal_flow_rate(p_inj_indi, t_inj_indi, rc, viscosity, L)
col1, col2, col3 = st.columns(3)
with col1:
    st.write('Q = {0} nL/s'.format(round(Q_inj_indi*1e12,3)))
with col2:
    st.write('u = {0} mm/s'.format(round(u_inj_indi*1e3,3)))
with col3:
    st.write('v = {0} nL'.format(round(v_inj_indi*1e12,3)))


st.subheader('Mobilize Analyte:')
col1, col2 = st.columns(2)
with col1:
    p_mob_anal = st.text_input('Pressure (mbar)', 400, key='9')
    p_mob_anal = float(p_mob_anal)
with col2:
    t_mob_anal = st.text_input('Time (s)', 180, key='10')
    t_mob_anal = float(t_mob_anal)
Q_mob_anal, u_mob_anal, v_mob_anal = cal_flow_rate(p_mob_anal, t_mob_anal, rc, viscosity, L)
col1, col2, col3 = st.columns(3)
with col1:
    st.write('Q = {0} nL/s'.format(round(Q_mob_anal*1e12,3)))
with col2:
    st.write('u = {0} mm/s'.format(round(u_mob_anal*1e3,3)))
with col3:
    st.write('v = {0} nL'.format(round(v_mob_anal*1e12,3)))



col1, col2 = st.columns(2)
with col1:
    st.latex(r'Q = \frac{p  \pi  R_c^4}{8 \eta L}')
with col2:
    st.latex(r'u = \frac{Q}{\pi R_c^2}')







###Experiment summary
st.divider()
st.header(' ')
st.header('Experiment Summary')

st.subheader('Volume Usage')

col1, col2, col3 = st.columns(3)
with col1:
    steps = st.text_input('Experiment steps',1)
    steps = int(steps)
with col2:
    replica = st.text_input('Replicas',1)
    replica = int(replica)
with col3:
    runs = steps*replica
    st.text('')
    st.text('')
    st.write('Total Runs = {0}'.format(runs))

v_tot_NaOH = v_flush_NaOH*runs
v_tot_buff = v_flush_buff*runs
v_tot_anal = (v_flush_anal + v_mob_anal) * runs
v_tot_indi = v_inj_indi*runs

v_tot = v_tot_NaOH + v_tot_buff + v_tot_anal + v_tot_indi

st.markdown('**Total Volume** = {0} uL, {1} mL'.format(round(v_tot*1e9,3), round(v_tot*1e6,3)))

st.write('NaOH Volume = {0} uL, {1} mL'.format(round(v_tot_NaOH*1e9,3), round(v_tot_NaOH*1e6,3)))

st.write('Buffer Volume = {0} uL, {1} mL'.format(round(v_tot_buff*1e9,3), round(v_tot_buff*1e6,3)))

st.write('Analyte Volume = {0} uL, {1} mL'.format(round(v_tot_anal*1e9,3), round(v_tot_anal*1e6,3)))

st.write('Indicator Volume = {0} uL, {1} mL'.format(round(v_tot_indi*1e9,3), round(v_tot_indi*1e6,3)))






st.subheader('Runtime estimation')

t_tot = (t_flush_NaOH + t_flush_buff + t_flush_anal + t_inj_indi + t_mob_anal)*runs
st.write('Runtime (ignoring movment and pressure build) = {0} mins, {1} hours'.format(round(t_tot/60,3), round(t_tot/3600,2)))

st.subheader('Resident time estimation')
tr = length_to_detector / u_mob_anal
string = r't_r = \frac{L_{detector}}{u_{mobilize}} = ' + str(round(tr,2)) + 's'
st.latex(string)





st.divider()
st.header(' ')
st.header('Stokes Einstein Conversion')
def stokes_einstein(temp, visc, d = None, rh = None):
    kB = 1.380649e-23   #J/K
    if d is not None and rh is not None:
        raise ValueError('Only d or rh should be provided, not both')
    
    if d is not None:
        rh = (kB * (temp+273.15)) / (6 * np.pi * visc * d)
        return rh
    elif rh is not None:
        d = (kB * (temp+273.15)) / (6 * np.pi * visc * rh)
        return d
    else:
        raise ValueError('Either d or rh should be provided')
col1, col2 = st.columns(2)
with col1:
    rh_or_d = st.radio('Known Parameter', ['rh','D'], 0)
    if rh_or_d == 'rh':
        rh = st.text_input('Hydrodynamic radius (nm)', 5)
        rh = float(rh)*1e-9
        d = stokes_einstein(temp, viscosity, rh=rh)
    if rh_or_d == 'D':
        default_d = stokes_einstein(temp, viscosity, rh=5*1e-9)
        d = st.text_input('Diffusion Coefficient (m^2/s)', default_d)
        d = float(d)
        rh = stokes_einstein(temp, viscosity, d=d)

with col2:
    if rh_or_d == 'rh':
        st.write(' ')
        string = 'D =' + str(round(d*1e9,3)) + r'\times 10^{-9} m^2/s'
        st.latex(string)
    if rh_or_d == 'D':
        st.write(' ')
        string = 'R_h =' + str(round(rh*1e9,3)) + r' nm'
        st.latex(string)






### Taylor Conditions
st.divider()
st.header('')
st.header('Taylor Conditions')


st.subheader('Tau condition:')
st.caption('The retention time is much greater than the time required for particles to fully diffuse radially')
rh = st.text_input('Expected Hydrodynamic radius (nm)', 5)
rh = float(rh)*1e-9
d = stokes_einstein(temp, viscosity, rh=rh)
use_tr_est = st.radio('Use theoretical resident time ({0})?'.format(str(round(tr,2)) + 's'), ['Yes', 'No'], 0, horizontal=True)
if use_tr_est == 'Yes':
    tr = tr
if use_tr_est == 'No':
    tr = st.text_input('Resident Time (s)')
    try:
        tr = float(tr)
    except:
        tr = 0


st.latex(r'\tau = \frac{Dt_r}{R_c^2}>1.4')
tau = d * tr / rc**2
st.write('tau = {0}'.format(round(tau,2)))
if tau>1.4:
    st.markdown(':white_check_mark: **Condition :rainbow[satisfied]**')
else:
    st.markdown(':negative_squared_cross_mark: **Condition NOT satisfied**')







st.subheader('Peclet number condition')
st.caption('Longitudinal diffusion effect on dispersion is negligible')
st.latex(r'Pe = \frac{uR_c}{D} > 70')
pe = (u_mob_anal * rc) / d

st.write('pe = {0}'.format(round(pe,2)))
if pe>70:
    st.markdown(':white_check_mark: **Condition :rainbow[satisfied]**')
else:
    st.markdown(':negative_squared_cross_mark: **Condition NOT satisfied**')



st.subheader('Band Width')
st.caption('Initial band-width can be treated as infinitesimally small')
st.latex(r'\frac{Vol_{inj}}{Vol_{total}} < 1\%')
vol_per = (v_inj_indi/(np.pi*rc**2*L))*100
st.write('Vol_inj/Vol_tot = {0}%'.format(round(vol_per,3)))
if vol_per<1:
    st.markdown(':white_check_mark: **Condition :rainbow[satisfied]**')
else:
    st.markdown(':negative_squared_cross_mark: **Condition NOT satisfied**')



st.subheader('Laminar Conditions')
st.caption('Mobilization liquid has low reynolds number such that it is under Laminar flow')
st.latex(r'R_e = \frac{\rho \times u_{mob} \times 2R_c}{\eta} < 2300')
st.write('Where rho is fluid density')
re = (density*u_mob_anal*2*rc)/viscosity
st.write('Re = {0}'.format(re))
if re<2300:
    st.markdown(':white_check_mark: **Condition :rainbow[satisfied]**')
else:
    st.markdown(':negative_squared_cross_mark: **Condition NOT satisfied**')











