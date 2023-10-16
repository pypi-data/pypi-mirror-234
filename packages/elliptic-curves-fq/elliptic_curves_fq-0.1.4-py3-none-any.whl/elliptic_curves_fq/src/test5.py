from .find_irreducible_polynomial import get_irreductible_polynomial
p= 131
b= 0
c=0
while True:
    tot = get_irreductible_polynomial(p,51)
    a = tot[1]
    c+= a
    b+=1
    if b%10 ==0:
        print(c/b)
