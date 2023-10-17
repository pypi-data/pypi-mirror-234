import numpy as np
import baccoemu as baccoemu
import time
import copy

try:
    import camb
except:
    raise ImportError("Please install camb to run this test. Execute 'pip install camb'")

#Calling baccoemu to compute the nonlinear power spectrum

params = {
    'omega_matter'  :  0.315,
    'A_s'           :  2e-9,
    'omega_baryon'  :  0.05,
    'ns'            :  0.96,
    'hubble'        :  0.67,
    'neutrino_mass' :  0.0,
    'w0'            : -1.0,
    'wa'            :  0.0,
    'expfactor'     :  1,

    'M_c'           :  14,
    'eta'           : -0.3,
    'beta'          : -0.22,
    'M1_z0_cen'     : 10.5,
    'theta_out'     : 0.25,
    'theta_inn'     : -0.86,
    'M_inn'         : 13.4
}


emulator = baccoemu.Matter_powerspectrum()
kk = np.logspace(-2,0,200)
k, pk = emulator.get_linear_pk(k=kk, **params)
t0 = time.time()
k, pk = emulator.get_linear_pk(k=kk, **params)
t1 = time.time()
k, Q = emulator.get_nonlinear_boost(k=kk, **params)
t2 = time.time()
k, S = emulator.get_baryonic_boost(k=kk, **params)
t3 = time.time()
k, pknl = emulator.get_nonlinear_pk(baryonic_boost=True, k=kk, **params)
t4 = time.time()
k, pk_camb = baccoemu.matter_powerspectrum.compute_camb_pk(params, k=kk, cold=True)
t5 = time.time()
sigma8 = emulator.get_sigma8(**params)
t6 = time.time()

print("Performances of the matter power spectrum emulator:")
print("---------------------")
print(f"Linear emulator: {t1-t0} (1 evaluation)")
print(f"Non-linear emulator: {t2-t1} (1 evaluation)")
print(f"Baryonic boost emulator: {t3-t2} (1 evaluation)")
print(f"Sigma8 emulator: {t6-t5} (1 evaluation)")
print(f"All contributions: {t4-t3} (1 evaluation)")
print("---------------------")
print(f"CAMB: {t5-t4} (1 evaluation)")
print("---------------------")

#test agreement between CAMB and linear emulators and sigma8
ratio = np.abs(pk/pk_camb-1.)
message = f'CAMB and linear cold  emulator in disagreement at more than 0.2% {np.amax(ratio)*100}%!'
assert np.all(ratio<=0.002), message

params_s8 = copy.deepcopy(params)
params_s8['sigma8_cold'] = sigma8
del params_s8['A_s']
k, pk_camb_sigma8 = baccoemu.matter_powerspectrum.compute_camb_pk(params_s8, k=kk, cold=True)
k, pk_sigma8 = emulator.get_linear_pk(k=kk, **params_s8)

ratio1 = np.abs(pk_camb_sigma8/pk_camb-1.)
ratio2 = np.abs(pk_camb_sigma8/pk-1.)
ratio3 = np.abs(pk_camb_sigma8/pk_sigma8-1.)

message1 = f'CAMB and linear/sigma8 emulators in disagreement at more than 0.2% {np.amax(ratio1)*100}%!'
message2 = f'CAMB and linear/sigma8 emulators in disagreement at more than 0.2% {np.amax(ratio2)*100}%!'
message3 = f'Linear A_s/sigma8 emulators in disagreement at more than 0.2% {np.amax(ratio3)*100}%!'

assert np.all(ratio1<=0.002), message1
assert np.all(ratio2<=0.002), message2
assert np.all(ratio3<=0.002), message3

k, pk = emulator.get_linear_pk(k=kk, cold=False, **params)
k, pk_camb = baccoemu.matter_powerspectrum.compute_camb_pk(params, k=kk, cold=False)
ratio = np.abs(pk/pk_camb-1.)
message = f'CAMB and linear total matter emulator in disagreement at more than 0.2% {np.amax(ratio)*100}%!'
assert np.all(ratio<=0.002), message

aa = np.linspace(0.5,1,100)
omm = np.linspace(0.3,0.35,100)
mcc = np.linspace(13,15,100)

par_arr = []
for i,a in enumerate(aa):
    pdict = copy.deepcopy(params)
    pdict['expfactor'] = a
    pdict['omega_matter'] = omm[i]
    pdict['M_c'] = mcc[i]
    par_arr.append(pdict)

t0 = time.time()
pk = np.array([emulator.get_linear_pk(k=kk, **par_arr[i])[1] for i,a in enumerate(aa)])
t1 = time.time()
Q = np.array([emulator.get_nonlinear_boost(k=kk, **par_arr[i])[1] for i,a in enumerate(aa)])
t2 = time.time()
S = np.array([emulator.get_baryonic_boost(k=kk, **par_arr[i])[1] for i,a in enumerate(aa)])
t3 = time.time()
pknl = np.array([emulator.get_nonlinear_pk(k=kk, **par_arr[i], baryonic_boost=True)[1] for i,a in enumerate(aa)])
t4 = time.time()

print("---------------------")
print(f"Linear emulator: {t1-t0} (100 evaluations)")
print(f"Non-linear emulator: {t2-t1} (100 evaluations)")
print(f"Baryonic boost emulator: {t3-t2} (100 evaluations)")
print(f"All contributions: {t4-t3} (100 evaluations)")
print("---------------------")

g_params = copy.deepcopy(params)
g_params['expfactor'] = aa
g_params['omega_matter'] = omm
g_params['M_c'] = mcc

t0 = time.time()
k, pk_grid = emulator.get_linear_pk(k=kk, **g_params)
t1 = time.time()
k, Q_grid = emulator.get_nonlinear_boost(k=kk, **g_params)
t2 = time.time()
k, S_grid = emulator.get_baryonic_boost(k=kk, **g_params)
t3 = time.time()
k, pknl_grid = emulator.get_nonlinear_pk(baryonic_boost=True, k=kk, **g_params)
t4 = time.time()

print("---------------------")
print("Using vectorization:")
print(f"Linear emulator: {t1-t0} (100 evaluations)")
print(f"Non-linear emulator: {t2-t1} (100 evaluations)")
print(f"Baryonic boost emulator: {t3-t2} (100 evaluations)")
print(f"All contributions: {t4-t3} (100 evaluations)")
print("---------------------")

ratios = np.abs(pk/pk_grid-1.)
message = f'Emulator with vectorization in disagreement at more than 0.001% ({np.amax(ratios)*100}%!)'
assert np.all(ratios<=1e-5), message

ratios = np.abs(Q/Q_grid-1.)
message = f'Emulator with vectorization in disagreement at more than 0.001% ({np.amax(ratios)*100}%!)'
assert np.all(ratios<=1e-5), message

ratios = np.abs(S/S_grid-1.)
message = f'Emulator with vectorization in disagreement at more than 0.001% ({np.amax(ratios)*100}%!)'
assert np.all(ratios<=1e-5), message

ratios = np.abs(pknl/pknl_grid-1.)
message = f'Emulator with vectorization in disagreement at more than 0.001% ({np.amax(ratios)*100}%!)'
assert np.all(ratios<=1e-5), message

print("All tests passed!")
