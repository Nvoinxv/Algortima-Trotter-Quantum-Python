from TrotterAlgorithm.core.solver import SolverPDE
import numpy as np
import itertools

# Ini bagian testing agar saat ke main.py jadi lebih siap
# Sebenarnya gw buat ini juga biar lebih gampang buat testing
# Running nya akan lama karna perhitungan ini sangat kompleks
# Jadi perlu sabar untuk membuat ini!

# Buat grid awal f0
# Ini dimensi yang gw pakai 2D
# Makin tinggi dimensi nya, makin kompleks perhitungan dan memori yang di butuhkan
# Titik point nya juga di kurangi jika laptop tidak kuat

dims = 2

# Wajib range 0 - 1, lebih dari itu akan NaN
points_per_dim = [0.2, 0.23]
f0_grid_points = list(itertools.product(points_per_dim, repeat=dims))
# ambil misal sum dari koordinat untuk nilai f0_grid (boleh diganti sesuai fisik)
f0_grid = np.array([sum(p)/dims for p in f0_grid_points])

# Step size grid
delta_x = 1.0 / (len(f0_grid) - 1)
    
# Koefisien finite difference order 2p, misal central difference 2nd order
# K = {-1, 0, 1} dengan a_k = [-1/2, 0, 1/2]
# Ini gw buat list untuk tiap dimensi dan gw pakai 2d karna laptop gw gak kuat
a_coeffs = {-1: -0.5, 0: 0.0, 1: 0.5}
a_coeffs_list = [a_coeffs for _ in range(dims)] 
    
# Misal PDE 1 dimensi, c_coeff = [1.0] (kecepatan atau koefisien)
c_coeffs = [1.0 for _ in range(dims)]
    
# Buat solver
solver = SolverPDE(f0_grid=f0_grid,
                    delta_x=delta_x,
                    a_coeffs_list=a_coeffs_list,  # list karena tiap dimensi beda
                    c_coeffs=c_coeffs)
    
# Cek state awal
print("State awal |f0⟩ amplitudo:")
print([amp.real for amp in solver.state.amplitudes])
    
# Ketik angka si variabel dt
# ini bebas aja isi dt 0 - 1 range nya
# Cuma saran gw 0.1 - 0.9 saja
dt = 0.5
solver.time_evolve(dt)
    
# Cek state setelah evolusi
print(f"\nState setelah 1 langkah evolusi dt={dt}:")
print([amp.real for amp in solver.state.amplitudes])