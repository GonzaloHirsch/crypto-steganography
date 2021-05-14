from pyfinite import ffield
# 355 is the given polynomial generator
# Lib link https://github.com/emin63/pyfinite
# Set useLUT to 0 because if not the operations give wrong values
F = ffield.FField(8, gen=355, useLUT=0)
print('The generator is', F.generator)
print('The polynomial is', F.ShowPolynomial(F.generator))
print('Sum and multiplication test')
a = 84
b = 13
print('The polynomial for a =', a, 'is', F.ShowPolynomial(a))
print('The polynomial for b =', b, 'is', F.ShowPolynomial(b))
print(a, '+', b, '=', F.Add(a,b))
print(a, 'x', b, '=', F.Multiply(a,b))
c = F.Multiply(a,b)
print('The polynomial for c =', c, 'is', F.ShowPolynomial(c))
print("Inverse Test")
print('Testing c * inverse(a) is', F.Multiply(c, F.Inverse(a)) == b)
print('Testing c * inverse(b) is', F.Multiply(c, F.Inverse(b)) == a)
print('Division Test')
print('Testing c/b =', F.Divide(c,b), 'should be', a)