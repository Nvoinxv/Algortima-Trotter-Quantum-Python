# Kita buat bilangan kompleks
# Ini berguna untuk perhitungan Qubit dan simulasi fisika nya
# Jadi kalau kalian belum paham, pelajari bilangan kompleks terlebih dahulu
# Sama seperti projek quantum komputer sebelum nya sih ini cuma beda nya ini simulasi fisika

import math

class ComplexNumbers:
    def __init__(self, real:float, imajiner:float):
        self.real = real
        self.imajiner = imajiner
    
    def __str__(self):
        return f"{self.real:.6f} + {self.imajiner:.6f} i"
    
    # Ini biar di debbug lebih mudah saja 
    def __repr__(self):
        return f"ComplexNumbers({self.real:.6f}, {self.imajiner:.6f})"
    
    # Disini kita buat fungsi perhitungan bilangan kompleks
    # Sebenarnya bisa langsung aja pakai numpy
    # Tapi gw pakai libary murni python saja biar tahu alur nya
    # Dan juga ini berguna buat kalian ngerti bagaimana alur kode tersebut

    def pertambahan(self, other):
        return ComplexNumbers(self.real + other.real, self.imajiner + other.imajiner)
    
    def pengurangan(self, other):
        return ComplexNumbers(self.real - other.real, self.imajiner - other.imajiner)
    
    def perkalian(self, other):
        bagian_real = self.real * other.real - self.imajiner * other.imajiner
        bagian_imajiner = self.real * other.imajiner + self.imajiner * other.real
        return ComplexNumbers(bagian_real, bagian_imajiner)
    
    def pembagian(self, other):
        if other.real == 0 and other.imajiner == 0:
            raise ValueError("Tidak bisa di bagi dengan nol!")
        
        bagian_real = self.real * other.real + self.imajiner * other.imajiner
        bagian_imajiner = self.imajiner * other.real - self.real * other.imajiner
        pembagi = other.real ** 2 + other.imajiner ** 2
        return ComplexNumbers(bagian_real / pembagi, bagian_imajiner / pembagi)
    
    # Untuk modulus Z nya 
    def Modulus(self):
        return math.sqrt(self.real ** 2 + self.imajiner ** 2)
    
    # Untuk konjugat nya
    def Konjugat(self):
        return ComplexNumbers(self.real, -self.imajiner)
    
    # Untuk bagian sudut nya
    def Sudut(self):
        return math.atan2(self.imajiner, self.real)
    
    # Buat copy object biar bisa dipakai di expm
    def copy(self):
        return ComplexNumbers(self.real, self.imajiner)

    
    # Bagian Equals
    def __eq__(self, other):
        return math.isclose(self.real, other.real, rel_tol=1e-9) and math.isclose(self.imajiner, other.imajiner, rel_tol=1e-9)
    
    # Operator overloading biar program bisa jalan
    def __add__(self, other):
        if not isinstance(other, ComplexNumbers):
            return NotImplemented
        return self.pertambahan(other)

    def __sub__(self, other):
        if not isinstance(other, ComplexNumbers):
            return NotImplemented
        return self.pengurangan(other)

    def __mul__(self, other):
        if not isinstance(other, ComplexNumbers):
            return NotImplemented
        return self.perkalian(other)

    def __truediv__(self, other):
        if not isinstance(other, ComplexNumbers):
            return NotImplemented
        return self.pembagian(other)
