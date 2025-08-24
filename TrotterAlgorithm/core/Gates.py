from TrotterAlgorithm.core.ComplexNumber import ComplexNumbers
import math

# Kita buat kelas untuk mendefinisikan quantum matrix
# Dari Identity (I), Pauli (X, Y, Z), Hadamard (H), dan CNOT.
class Matrix_Gates:
    def __init__(self):  
        self.I = self.identitas_matrix(2)
        self.X = self.pauli_x()
        self.Y = self.pauli_y()
        self.Z = self.pauli_z()
        self.H = self.hadamard()
        self.CNOT = self.cnot()
        self.CNOT_3 = self.cnot_3_qubit()

    # Kita membuat identity matrix 
    # Disini buat menyesuaikan D_operator
    def identitas_matrix(self, n):
        return [[ComplexNumbers(1,0) if i==j else ComplexNumbers(0,0) for j in range(n)] for i in range(n)]
    
    def expm(self, mat):
        """
        Matrix exponential e^(mat) pakai Taylor series.
        mat: list of list ComplexNumbers
        terms: jumlah suku Taylor
        """
        # Inisialisasi result = I
        n = len(mat)
        mg = Matrix_Gates()
        result = mg.identitas_matrix(n)
        # Inisialisasi power = mat
        power = [[mat[i][j].copy() for j in range(n)] for i in range(n)]
        # Jumlah suku Taylor default
        terms = 20
        for k in range(1, terms):
            factor = ComplexNumbers(1/math.factorial(k), 0)
            # result += power / k!
            for i in range(n):
                for j in range(n):
                    result[i][j] += power[i][j] * factor
            # update power = power * mat
            power_new = [[ComplexNumbers(0,0) for _ in range(n)] for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    s = ComplexNumbers(0,0)
                    for l in range(n):
                        s += power[i][l] * mat[l][j]
                    power_new[i][j] = s
            power = power_new
        return result


    # Dummy shift operator untuk D_operator
    def shift_operator(self, j, k, n_qubits_dim):
        """
        Shift operator sederhana ukuran 2^n_qubits_dim × 2^n_qubits_dim
        j: dimensi yang di-shift
        k: step shift
        """
        size = 2**n_qubits_dim
        mat = [[ComplexNumbers(0,0) for _ in range(size)] for _ in range(size)]
        for i in range(size):
            # shift modulo size
            target = (i + k) % size
            mat[i][target] = ComplexNumbers(1,0)
        return mat
    
    # Kita membuat Pauli-X (NOT gate), tugasnya flip state |0> <-> |1>
    def pauli_x(self):
        return [
            [ComplexNumbers(0, 0), ComplexNumbers(1, 0)],
            [ComplexNumbers(1, 0), ComplexNumbers(0, 0)]
        ]

    # Kita membuat Pauli-Y, mirip X tapi kasih faktor imajiner
    def pauli_y(self):
        return [
            [ComplexNumbers(0, 0), ComplexNumbers(0, -1)],
            [ComplexNumbers(0, 1), ComplexNumbers(0, 0)]
        ]

    # Kita membuat Pauli-Z, kasih fase negatif ke state |1>
    def pauli_z(self):
        return [
            [ComplexNumbers(1, 0), ComplexNumbers(0, 0)],
            [ComplexNumbers(0, 0), ComplexNumbers(-1, 0)]
        ]
    
    # Kita membuat Hadamard (H), fungsinya bikin superposisi
    def hadamard(self):
        sqrt2_inv = 1 / math.sqrt(2)
        return [
            [ComplexNumbers(sqrt2_inv, 0), ComplexNumbers(sqrt2_inv, 0)],
            [ComplexNumbers(sqrt2_inv, 0), ComplexNumbers(-sqrt2_inv, 0)]
        ]
    
    def scale_matrix(self, mat, factor):
        n = len(mat)
        return [[mat[i][j] * ComplexNumbers(factor.real, factor.imag) for j in range(n)] for i in range(n)]

    
    # Kita membuat CNOT (2-qubit gate), kalau control = 1, target di-flip
    def cnot(self):
        return [
            [ComplexNumbers(1, 0), ComplexNumbers(0, 0), ComplexNumbers(0, 0), ComplexNumbers(0, 0)],
            [ComplexNumbers(0, 0), ComplexNumbers(1, 0), ComplexNumbers(0, 0), ComplexNumbers(0, 0)],
            [ComplexNumbers(0, 0), ComplexNumbers(0, 0), ComplexNumbers(0, 0), ComplexNumbers(1, 0)],
            [ComplexNumbers(0, 0), ComplexNumbers(0, 0), ComplexNumbers(1, 0), ComplexNumbers(0, 0)]
        ]
    
    def cnot_3_qubit(self):
        """
        CNOT 3-qubit: control = qubit ke-2 (Alice), target = qubit ke-3 (Bob)
        Matrix 8x8 → format 3D untuk simulasi teleportasi
        """
        zero = ComplexNumbers(0,0)
        one  = ComplexNumbers(1,0)
        return [
            [one, zero, zero, zero, zero, zero, zero, zero],
            [zero, one, zero, zero, zero, zero, zero, zero],
            [zero, zero, one, zero, zero, zero, zero, zero],
            [zero, zero, zero, one, zero, zero, zero, zero],
            [zero, zero, zero, zero, zero, zero, one, zero],
            [zero, zero, zero, zero, zero, zero, zero, one],
            [zero, zero, zero, zero, one, zero, zero, zero],
            [zero, zero, zero, zero, zero, one, zero, zero],
        ]