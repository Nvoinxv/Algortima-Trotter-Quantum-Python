from TrotterAlgorithm.core.pde import WignerPDE
import numpy as np

# Buat instance Wigner PDE
# Lu bisa atur x point dan p point nya
# Wajib integer bukan float
wigner = WignerPDE(x_points=2, p_points=2)  # grid kecil biar cepat

# Evolusi state beberapa langkah
wigner.evolve(dt=0.3, steps=3)

# Ambil state amplitudo setelah evolusi
state_amplitudes = wigner.get_state()

# Print amplitudo (bisa juga dipakai visualisasi)
print("Amplitudo state akhir:")
for amp in state_amplitudes:
    print(amp)

amplitudes_real = np.array([amp.real for amp in state_amplitudes])
amplitudes_reshaped = amplitudes_real.reshape((2**wigner.Nx, 2**wigner.Np))

