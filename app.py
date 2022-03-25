from asyncio.windows_events import NULL
from email import message
from flask import Flask, appcontext_popped, render_template, url_for, request
import random

app = Flask(__name__)


import random
def calculateJacobiSymbol(a, n): 

    jacobi_number = 1
    
    # If the numerator is 1 the jacobi symbol gives (1/n) = 1
    if (a == 1): 
        return jacobi_number # (1/n) = 1 

    while (a):
        if (a < 0):
            # using the property of jacobi symbol (a/n) = (-a/n)*(-1/n) 
            a = -a
            if (n % 4 == 3):
                
                # using the proerty of jacobi symbol (-1/n) = -1 if n = 3 (mod 4) 
                jacobi_number = -jacobi_number 

        # extracting any even numerator using the property of jacobi symbol
        # (2a/n) = (2/n)(a/n) = -(a/n) if n = 3,5(mod 8)
        while (a % 2 == 0): 
            a = a // 2
            if (n % 8 == 3 or n % 8 == 5): 
                jacobi_number = -jacobi_number 

        # swaping the numerator and denominator using the law of reciprocity 
        a, n = n, a 
        
        # law of reciprocity: (m/n)(n/m) = (-1)^((m-1)/2, (n-1)/2) = -1 if n = a = 3 (mod 4)
        if (a % 4 == 3 and n % 4 == 3): 
            jacobi_number = -jacobi_number
        
        # reduce the numerator modulo the denominator  
        a = a % n 

        if (a > n // 2): 
            a = a - n

    if (n == 1): 
        return jacobi_number

    
    # If the numerator and denominator are not coprime the jacobi symbol is 0
    return 0

 
# The Solovay- Strassen Primality Test 
def solovayStrassen(p): 
    
    iterations = 90
    # there is no prime number below 2
    if (p < 2): 
        return False 
    
    # there is no prime number that is even except 2
    if (p != 2 and p % 2 == 0): 
        return False 

    # this loop runs 'i' iterations where iterations is specified by the user
    for i in range(iterations):
        
        # generate a random number for every iteration and calculate jacobi and euler nubmers
        # it should be in the range of 1 <= a <= p-1
        a = random.randint(1,p-1)

        # Jacobi value
        jacobi = (p + calculateJacobiSymbol(a, p)) % p 
        
        # Euler value
        mod = pow(a, (p - 1) // 2, p)

        #if jacobi symbol is not equal to euler nubmer then the tested number is composite
        if (jacobi == 0 or mod != jacobi):
            return False
    
    # if the number has equal jacobi and euler value after 'n' number of iterations of random number
    # then the number is prime with the probability of 1-(1/2^k) where 'k' is number of iterations
    return True
    

def checkPrime(form):
    checkNumber = request.form['input-number']
    resultMessage = ''
    isValidNumber = False
    isPrime = False
    if checkNumber:
        try:
            intNum = int(checkNumber)
            if len(str(intNum)) > 1000:
                resultMessage = 'Sorry the maximum length of a number can be upto 1000 digits'
            elif intNum < 0:
                resultMessage = 'Negative numbers are NOT PRIME'
            else:
                isValidNumber = True
                resultMessage = str(intNum)
                if(solovayStrassen(intNum)):
                    isPrime = True


        except ValueError:
            resultMessage = 'Sorry it is not a valid input, please enter a number'
    
    return (resultMessage, isValidNumber, isPrime)
        
        


@app.route('/', methods=['GET', 'POST'])
def index():
    finalResult = ('',False, False)
    if request.method == 'POST':
        form = request.form
        finalResult = checkPrime(form)
        if not (finalResult):
            finalResult[0] = 'Please enter a number to test'

    return render_template('index.html', finalResult=finalResult)


if __name__ == "__main__":
    app.run(debug=True)

