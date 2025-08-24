from TrotterAlgorithm.core.ComplexNumber import ComplexNumbers
from TrotterAlgorithm.core.solver import SolverPDE
import numpy as np
from tqdm import tqdm

# Implementasi PDE Wigner dengan fungsi 2D
# Beda nya wignerPDE dan solverPDE?
# Kalau wigner itu lebih fokus nya persamaan fisik dan wigner itu mendifinisikan hal hal kompleks
# Sedangkan solverPDE itu lebih ke algoritma numerik evolusi qubit
#
# Inti nya solverPDE itu kek mesin perhitungan
# Kalau wignerPDE kek masukin dataset kalau di bidang AI
#
# gw pakai x_point dan p_point nya itu 2 karna balik lagi latop gw busuk bet

class WignerPDE:
    def __init__(self, x_points=16, p_points=16, mass=1.0):
        self.mass = mass
        
        # Bikin grid beneran dari jumlah titik
        self.x_grid = np.linspace(-1, 1, x_points)   # grid posisi
        self.p_grid = np.linspace(-1, 1, p_points)   # grid momentum
        self.Nx, self.Np = len(self.x_grid), len(self.p_grid)
        self.N = self.Nx * self.Np
        print(f"[Init] Grid posisi {self.Nx} titik, momentum {self.Np} titik, total {self.N} amplitudo")

        # Kondisi awal Wigner (Gaussian)
        self.f0_grid = self.initial_condition()   # <-- pakai fungsi baru
        print("[Init] Kondisi awal Wigner function dibuat")
        
        # Koefisien finite difference central 2nd order
        self.a_coeffs = {-1: -0.5, 0: 0.0, 1: 0.5}
        
        # List untuk tiap dimensi (2D: x & p)
        a_coeffs_list = [self.a_coeffs, self.a_coeffs]
        c_coeffs = [1.0, 1.0]  # PDE per dimensi
        
        # Step size pakai grid spacing
        delta_x = (self.x_grid[-1] - self.x_grid[0]) / (self.Nx - 1)

        # Buat solver
        self.solver = SolverPDE(
            f0_grid=self.f0_grid.flatten(),   # flatten baru dikasih ke solver
            delta_x=delta_x,
            a_coeffs_list=a_coeffs_list,
            c_coeffs=c_coeffs
        )
        print("[Init] SolverPDE siap digunakan")
    
    def initial_condition(self):
        """Kondisi awal Wigner function Gaussian di grid 2D (x,p)"""
        X, P = np.meshgrid(self.x_grid, self.p_grid, indexing="ij")
        f0 = np.exp(-(X**2 + P**2))  # Gaussian sederhana
        return f0   # biarkan tetap 2D, flatten baru pas dipakai solver
    
    def evolve(self, dt=0.1, steps=1):
        print(f"\n[Evolve] Mulai evolusi {steps} langkah...")
        for step in tqdm(range(steps), desc="Evolving", unit="step"):
            self.solver.time_evolve(dt)
        print("[Evolve] Evolusi selesai ✅")
    
    def get_state(self):
        return self.solver.state.amplitudes
