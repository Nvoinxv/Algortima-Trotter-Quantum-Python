from TrotterAlgorithm.core.Gates import Matrix_Gates
from TrotterAlgorithm.core.ComplexNumber import ComplexNumbers
from TrotterAlgorithm.core.Qubit import MultiQubitState
from TrotterAlgorithm.core.utils import NumericalUtils
import numpy as np
import itertools
from tqdm import tqdm

# Kita bikin solver PDE versi kuantum
# Logikanya: kita pake Finite Difference Diskrit + Encoding ke Qubit
# Ruang diskrit [0,1] diubah jadi state qubit |f0⟩
# Turunan dihitung pakai central finite difference order 2p
# Operator turunan Hermitian D^j dibangun pake shift operator + faktor −i
# Evolusi PDE diubah jadi ODE di ruang kuantum

class SolverPDE:
    def __init__(self, f0_grid, delta_x, a_coeffs_list, c_coeffs):
        """
        f0_grid: grid awal fungsi f0 di ruang diskrit
        delta_x: step size grid
        a_coeffs_list: list dictionary {k: a_k} untuk tiap dimensi j
        c_coeffs: list koefisien PDE untuk tiap dimensi
        """
        self.f0_grid = f0_grid
        self.delta_x = delta_x
        self.a_coeffs_list = a_coeffs_list
        self.c_coeffs = c_coeffs
        self.mg = Matrix_Gates()
        
        # encode f0_grid ke state qubit |f0⟩
        self.state = self.encode_initial_condition(f0_grid)
        
        # hitung jumlah qubit dari f0_grid
        n_qubits_total = len(self.state.amplitudes).bit_length() - 1

        # buat operator D^j untuk tiap dimensi
        self.D_ops = [
                self.D_operator(
                                j, 
                                a_coeffs, 
                                delta_x, 
                                n_qubits_total
                            )
                        for j, a_coeffs in enumerate(a_coeffs_list)
                    ]
    
    def encode_initial_condition(self, f0_grid):
        """
        Encode f0_grid ke global multi-qubit state
        Memetakan setiap titik grid ke single qubit alpha/beta, lalu gabung
        jadi amplitudo global (produk tensor)
        """
        qubit_list = []

        print("[Encode] Mulai encoding kondisi awal...")
        for val in tqdm(f0_grid.flat, total=f0_grid.size, desc="Encoding progress"):
            alpha = ComplexNumbers(val, 0)
            beta = ComplexNumbers((1 - val**2)**0.5, 0)

            # Normalisasi amplitudo qubit dengan NumericalUtils
            alpha_arr = NumericalUtils.normalize(np.array([alpha.real]))
            beta_arr  = NumericalUtils.normalize(np.array([beta.real]))
            alpha = ComplexNumbers(alpha_arr[0], 0)
            beta  = ComplexNumbers(beta_arr[0], 0)

            qubit_list.append((alpha, beta))
            
        print("[Encode] Selesai encoding kondisi awal.")

        amplitudes = []
        for bits in itertools.product([0,1], repeat=len(qubit_list)):
            amp = ComplexNumbers(1,0)
            for i, b in enumerate(bits):
                alpha, beta = qubit_list[i]
                amp *= alpha if b == 0 else beta
            amplitudes.append(amp)

        return MultiQubitState(amplitudes)

    def D_operator(self, j, a_coeffs, delta_x, n_qubits_dim):
        """Bikin operator turunan Hermitian D^j untuk dimensi j"""
        # Buat identity matrix ukuran 2^n_qubits × 2^n_qubits
        mg = Matrix_Gates()
        D_j = mg.identitas_matrix(2**n_qubits_dim)  
        for k, a_k in a_coeffs.items():  # k=-p..p
            shift = mg.shift_operator(j, k, n_qubits_dim)  # S^j^k
            # scale shift matrix + -i * a_k/delta_x
            D_j = [[D_j[i][j] + shift[i][j] * ComplexNumbers(0, -a_k/delta_x) 
                for j in range(len(D_j))] 
                for i in range(len(D_j))]
        return D_j

    def time_evolve(self, dt):
        """Evolusi global state satu langkah waktu Δt"""
        n_qubits = self.state.n_qubits
        mg = Matrix_Gates()
        U = mg.identitas_matrix(2**n_qubits)

        print("=== Mulai evolusi ===")
        for j in range(len(self.D_ops)):
            print(f"\n-- Dimensi ke-{j} --")
            print("Matriks D^j dibuat...")
            scaled_D = self.mg.scale_matrix(self.D_ops[j], -1j * self.c_coeffs[j] * dt)
            print("D^j sudah di-scale.")
            U_j = self.mg.expm(scaled_D)
            print("Exponential matriks (U_j) selesai dihitung.")

            # Apply ke global unitary
            n = len(U)
            U_new = []
            print("Mengupdate global unitary U...")
            for i in range(n):
                row = []
                for jj in range(len(U_j[0])):
                    val = ComplexNumbers(0,0)
                    for k in range(len(U_j)):
                        val += U[i][k] * U_j[k][jj]
                    row.append(val)
                U_new.append(row)
                if i % max(1, n//4) == 0:  # log 4 step per batch
                    print(f"  Progress bar: baris {i+1}/{n} selesai")
            U = U_new
            print("Update global unitary untuk dimensi selesai.")

        # Apply ke MultiQubitState
        print("\nMenerapkan unitary ke state |f⟩ ...")
        self.state.apply_unitary(U)
        
        # Normalisasi amplitudo state setelah evolusi
        arr = np.array([amp.real for amp in self.state.amplitudes])
        normed = NumericalUtils.normalize(arr)
        for idx, amp in enumerate(normed):
            self.state.amplitudes[idx] = ComplexNumbers(amp, 0)

        print("Evolusi langkah waktu selesai.\n")
        return self.state

