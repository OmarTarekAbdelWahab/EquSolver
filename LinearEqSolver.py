import math
import time

def solve(method, a, b, n, precision, x=None, iterations=None, rel_error=None):

    time_i =  time.perf_counter_ns()
    result = ""

    if (method == "Gauss Elimination"):
        result = gauss(a, b, n, precision)
    elif(method == "Gauss-Jordan"):
        result = GaussJordan(a, b, n, precision)
    elif(method == "LU-Downlittle"):
        result = luDecomposition(a, b, n, precision)
    elif(method == "LU-Cholseky"):
        result = cholesky(a, b, n, precision)
    elif(method == "LU-Crout"):
        result = crout(a, b, n, precision)
    elif(method == "Gauss-Seidel Method"):
        #a, b, n, x, it,re
        if(x!=None and iterations!=None and rel_error!=None):
            result = seidel(a, b, n, precision, x, iterations, rel_error)
        else:
            return None
    elif(method == "Jacobi Iterations"):
        if(x!=None and iterations!=None and rel_error!=None):
            result = jacobi(a, b, n, precision, x, iterations, rel_error)
        else:
            return None
    elif(method == ""):
        result = "An operation is required"

    time_f = time.perf_counter_ns()
    delta = time_f-time_i

    print(delta)
    return result, delta


def gauss (a, b, n,precision):
    string_solution = ""
    for k in range(n):
        max = k
        for i in range(k+1, n):
            if abs(a[i][k]) > a[max][k]:
                max = i
        temp = a[k]
        a[k] = a[max]
        a[max] = temp
        t = b[k]
        b[k] = b[max]
        b[max] = t
        if a[k][k] == 0 :
            if b[k] == 0:
                string_solution += "infinite number of solutions!\n"
                a[k][k] = 1
            else:
                return "Not Possible with Gauss Elimination"
        for i in range(k+1, n):
            factor= round(float(a[i][k]) / a[k][k],precision)
            b[i] =round(b[i]- factor * b[k],precision)
            for j in range(k, n):
                a[i][j] =round(a[i][j]- factor*a[k][j],precision)
    #printRowEchelonForm(a, b, n)
    solution = [0]*n
    for i in range(n - 1, -1, -1):
        sum = 0
        for j in range(i+1, n):
            sum += a[i][j]*solution[j]
        solution[i] = round(float(b[i] - sum) / float(a[i][i]),precision)

    #printSolution(solution, n)
    string_solution += str(solution)
    return string_solution


def GaussJordan(a, b, n,precision):
    #getcontext().prec = 32
    string_solution = ""
    for i in range(n):
        a[i].append(b[i])
    x = []
    for i in range(n):
        if a[i][i] == 0.0:
            for q in range(i+1, n):
                if(a[q][i]) != 0:
                    a[i], a[q] = a[q], a[i]
                    break
            else:
                if a[i][n] == 0:
                    string_solution += "Infinite number of solutions!\n"
                    a[i][i] = 1
                else:
                    return "No solutions!"
        for j in range(n):
            if i != j:
                ratio = round(float(a[j][i] / a[i][i]),precision)

                for k in range(n + 1):
                    a[j][k] = round(a[j][k] - ratio * a[i][k],precision)
    #print (a)
    # Obtaining Solution

    for i in range(n):
        x.append( round(a[i][n] / a[i][i],precision))

    # Displaying solution
    string_solution += "Required solution is: \n"
    #print('Required solution is: \n')
    for i in range(n):
        #print('X%d = %0.2f' % (i, x[i])),
        #solution += 'X%d = %0.2f' % (i, x[i])
        string_solution += f"X{i} = {x[i]}\n"
        # print(solution)
    #print(solution)
    return string_solution


def GaussJordan_(a, b, n,precision):
    for i in range(n):
        a[i].append(b[i])
    x = []
    for i in range(n):
        if a[i][i] == 0.0:
            for q in range(i+1, n):
                if(a[q][i]) != 0:
                    a[i], a[q] = a[q], a[i]
                    break
            else:
                if a[i][n] == 0:
                    print ("Infinite number of solutions!")
                else:
                    print ("No solutions!")
                return
        for j in range(n):
            if i != j:
                ratio = round(float(a[j][i] / a[i][i]),precision)

                for k in range(n + 1):
                    a[j][k] =round( a[j][k] - ratio * a[i][k],precision)
    return a

def luDecomposition(a, b, n,precision):
    lower = [[0]*n for i in range(n)]
    upper = [[0]*n for i in range(n)]
    string_solution = ""
    for i in range(n):
        #Upper Triangular
        for k in range(i, n):
            sum = 0
            for j in range(i):
                sum =round(sum+ (lower[i][j] * upper[j][k]),precision)
            upper[i][k] = round(a[i][k] - sum,precision)

        #Lower Triangular
        for k in range(i, n):
            if i == k:
                lower[i][i] = 1
            else:
                # Summation of L(k, j) * U(j, i)
                sum = 0
                for j in range(i):
                    sum =round(sum+ (lower[k][j] * upper[j][i]),precision)
                try:
                    lower[k][i]= round((a[k][i] - sum) / upper[i][i],precision)
                except:
                    solution_string += "LU Decomposition not possible\n"
                    return 

    #setw is for displaying nicely
    print ("Triangles:")

    #Displaying the result :
    print ("Lower:")
    print (lower)

    print ("Upper:")
    print (upper)

    yarray = GaussJordan_(lower, b, n,precision)
    if not yarray:
        return
    y = []
    for i in range(n):
        y.append(round(yarray[i][n] / yarray[i][i],precision))
    print ("Y: ")
    print (y)
    resarray = GaussJordan_(upper, y, n,precision)
    if not resarray:
        return
    y = []
    res = []
    for i in range(n):
        res.append(round(resarray[i][n] / resarray[i][i],precision))
    print ("Result: ")
    return res

def isSymmetric(a, n):
    for i in range(n):
        for j in range(i+1, n):
            if(a[i][j] != a[j][i]):
                return False
    return True

def cholesky(a, b, n,precision):
    if not (isSymmetric(a, n)):
        return "Not Symmetric"
        
    l = [[0]*n for i in range(n)]
    print (l)
    for i in range(n):
        for j in range(i+1):
            sum = 0
            for k in range(j):
                sum =round(sum+ l[i][k]*l[j][k],precision)
            if i == j:
                if(a[i][i] - sum) < 0:
                    return "Not positive definite"
                l[i][j] = round(float(math.sqrt(a[i][i] - sum)),precision)
            else:
                if (l[j][j]) == 0:
                    return "Not positive definite"
                l[i][j] = round(float(1.0 / l[j][j]) * (a[i][j] - sum),precision)
    u = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(n):
            u[i][j] = l[j][i]
    print ("Lower:")
    print (l)
    print ("Upper:")
    print (u)
    yarray = GaussJordan_(l, b, n,precision)
    if not yarray:
        return
    y = []
    for i in range(n):
        y.append(round(yarray[i][n] / yarray[i][i],precision))
    print ("Y: ")
    print (y)
    resarray = GaussJordan_(u, y, n,precision)
    if not resarray:
        return
    res = []
    for i in range(n):
        res.append( round(resarray[i][n] / resarray[i][i],precision))
    print ("Result: ")
    return res


def crout(a, b, n,precision):
    sum = 0
    u = []
    for i in range(n):
        lis = []
        for j in range(n):
            lis.append(0)
        u.append(lis)
    l = []
    for i in range(n):
        lis = []
        for j in range(n):
            lis.append(0)
        l.append(lis)
    for i in range(n):
        u[i][i] = 1
    for j in range(n):
        for i in range(j, n):
            sum = 0
            for k in range(j):
                sum =round(sum+ l[i][k]*u[k][j],precision)
            l[i][j] = round(a[i][j] - sum,precision)
        for i in range(j, n):
            sum = 0
            for k in range(j):
                sum =round(sum+ l[j][k]*u[k][i],precision)
            if l[j][j] == 0:
                print ("Crout not posspile")
                return
            u[j][i] = round((a[j][i] - sum) / float(l[j][j]),precision)
    print ("Upper:")
    print (u)
    print ("Lower:")
    print (l)
    yarray = GaussJordan_(l, b, n,precision)
    if not yarray:
        return
    y = []
    for i in range(n):
        y.append(round(yarray[i][n] / yarray[i][i],precision))
    print ("Y: ")
    print (y)
    resarray = GaussJordan_(u, y, n,precision)
    if not resarray:
        return
    y = []
    res = []
    for i in range(n):
        res.append(round(resarray[i][n] / resarray[i][i],precision))
    print ("Result: ")
    return res


def largest(arr, n):
    max = arr[0]

    for i in range(1, n):
        if arr[i] > max:
            max = arr[i]
    return max

def check_diagonal(arr, n):
    for i in range(0, n):
        if arr[i][i] == 0:
            return False
    return True


def determinant(matrix, mul):

    width = len(matrix)
    if width == 1:
        return mul * matrix[0][0]
    else:
        sign = -1
        answer = 0
        for i in range(width):
            m = []
            for j in range(1, width):
                buff = []
                for k in range(width):
                    if k != i:
                        buff.append(matrix[j][k])
                m.append(buff)
            sign *= -1
            answer = answer + mul * determinant(m, sign * matrix[0][i])
    return answer


def seidel(a, b, n, precision, x, it,re):
    count = it
    solution_str = ""
    print(re)
    if (not check_diagonal(a, n)):
        return "One or more diagonal entries are zero. Can't use this method."
    if(determinant(a, 1) == 0):
        print("zero matrix")
        solution_str += "WARNING: determinant of coefficient matrix is zero!!\n"
    while count > 0:
        y = [element for element in x]
        print("y before")
        print(y)
        for j in range(n):
            d = b[j]
            for i in range(n):
                if (i != j):
                    d =round(d- a[j][i] * x[i],precision)
            x[j] = round(d / float(a[j][j]),precision)
        for k in range(n):
            if (x[k] == 0):
                if(y[k] != 0):
                    y[k] = 100
                continue
            y[k] = round(abs((x[k] - y[k]) / float(x[k])) / 100.0,precision)
        error = largest(y, n)
        if error < re:
            print(error)
            print("Return from relative error")
            print(x)
            print("Iterations:")
            print(it - count + 1)
            solution_str += str(x)
            return solution_str
        print("relative errors:")

        print(y)
        count -= 1
    solution_str += str(x)
    return solution_str

def jacobi(a, b, n, precision, x, it,re):
    count = it
    solution_str = ""
    print(re)
    if (not check_diagonal(a, n)):
        return "One or more diagonal entries are zero. Can't use this method."
    if(determinant(a, 1) == 0):
        #print("zero matrix")
        solution_str += "WARNING: determinant of coefficient matrix is zero!!\n"
    while count > 0:
        y = [element for element in x]
        print("y before")
        print(y)
        oldx = [e for e in x]
        for j in range(n):
            d = b[j]
            for i in range(n):
                if (i != j):
                    d =round(d- a[j][i] * oldx[i],precision)
            x[j] = round(d / float(a[j][j]),precision)
        for k in range(n):
            if (x[k] == 0):
                if(y[k] != 0):
                    y[k] = 100
                continue
            y[k] = round(abs((x[k] - y[k]) / float(x[k])) / 100.0,precision)
        error = largest(y, n)
        if error < re:
            print(error)
            print("Return from relative error")
            print(x)
            print("Iterations:")
            print(it - count + 1)
            solution_str += str(x)

            return solution_str
        print("relative errors:")

        print(y)
        count -= 1
    solution_str += str(x)
    return solution_str