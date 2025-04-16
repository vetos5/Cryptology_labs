import random
import math

def jacobi_symbol(a, n):
    """
    Calculate the Jacobi symbol (a/n)
    
    Args:
        a (int): Integer value
        n (int): Odd positive integer
        
    Returns:
        int: Jacobi symbol value (1, -1, or 0)
    """
    if n <= 0 or n % 2 == 0:
        raise ValueError("n must be an odd positive integer")
    
    if a == 0:
        return 0
    
    if a == 1:
        return 1
    
    a1, e = a, 0
    while a1 % 2 == 0:
        a1 = a1 // 2
        e += 1
    
    s = 1
    if e % 2 == 1 and (n % 8 == 3 or n % 8 == 5):
        s = -1
    
    if a1 == 1:
        return s
    
    if n % 4 == 3 and a1 % 4 == 3:
        s = -s
    
    return s * jacobi_symbol(n % a1, a1)

def modular_exponentiation(base, exponent, modulus):
    """
    Calculate (base^exponent) % modulus efficiently
    
    Args:
        base (int): Base
        exponent (int): Exponent
        modulus (int): Modulus
        
    Returns:
        int: Result of modular exponentiation
    """
    if modulus == 1:
        return 0
    
    result = 1
    base = base % modulus
    
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    
    return result

def solovay_strassen_test(n, iterations=10):
    """
    Perform Solovay-Strassen primality test
    
    Args:
        n (int): Number to test for primality
        iterations (int, optional): Number of test iterations. Default is 10.
        
    Returns:
        tuple: (is_probable_prime, details)
            - is_probable_prime (bool): True if n is probably prime
            - details (list): List of test details for each iteration
    """
    if n <= 1:
        return False, ["Error: Number must be greater than 1"]
    
    if n == 2 or n == 3:
        return True, ["Number is prime (special case)"]
        
    if n % 2 == 0:
        return False, ["Number is even and greater than 2, so it's composite"]
    
    details = []
    
    for i in range(iterations):
        a = random.randint(2, n-1)
        
        # Calculate Jacobi symbol (a/n)
        j = jacobi_symbol(a, n)
        
        # Calculate modular exponentiation
        exp = (n-1) // 2
        mod_exp = modular_exponentiation(a, exp, n)
        
        # Adjust result to match Jacobi symbol range
        if mod_exp == n-1:
            mod_exp = -1
        
        # Check if congruence holds
        result = (j % n == mod_exp % n)
        
        detail = {
            "iteration": i+1,
            "a": a,
            "jacobi": j,
            "mod_exp": mod_exp if mod_exp != -1 else n-1,
            "congruent": result
        }
        details.append(detail)
        
        if not result:
            return False, details
    
    return True, details

def is_prime_deterministic(n):
    """
    Check if number is prime using deterministic method (for smaller numbers)
    
    Args:
        n (int): Number to check for primality
        
    Returns:
        bool: True if n is prime
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    
    return True

def analyze_number(n, ss_iterations=10):
    """
    Analyze a number with both deterministic check and probabilistic test
    
    Args:
        n (int): Number to analyze
        ss_iterations (int): Number of Solovay-Strassen iterations
        
    Returns:
        dict: Analysis results containing primality information and test details
    """
    try:
        n = int(n)
        
        # For small numbers, use deterministic test
        if n < 10**9:
            is_prime = is_prime_deterministic(n)
            deterministic_result = "prime" if is_prime else "composite"
            
            # Run Solovay-Strassen anyway for educational purposes
            ss_result, ss_details = solovay_strassen_test(n, ss_iterations)
            
            return {
                "number": n,
                "deterministic_check": deterministic_result,
                "deterministic_possible": True,
                "solovay_strassen_result": "probably prime" if ss_result else "composite",
                "solovay_strassen_details": ss_details,
                "error": None
            }
        else:
            # Use only Solovay-Strassen for larger numbers
            ss_result, ss_details = solovay_strassen_test(n, ss_iterations)
            
            return {
                "number": n,
                "deterministic_check": "number too large",
                "deterministic_possible": False,
                "solovay_strassen_result": "probably prime" if ss_result else "composite",
                "solovay_strassen_details": ss_details,
                "error": None
            }
    
    except Exception as e:
        return {
            "number": n,
            "error": str(e),
            "deterministic_possible": False,
            "solovay_strassen_details": []
        } 