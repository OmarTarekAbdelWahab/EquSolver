import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from sympy import *
from sympy.plotting import plot
import matplotlib.pyplot as mpl
from numpy import linspace
import numpy as np
x= Symbol('x')


x = symbols('x')


def FixedPoint(x0,es,it,gx_str):
    global x
    xr = x0
    ans = ""
    gx = sympify(gx_str)
    if(abs(float(diff(gx, x).subs(x, x0).evalf()))>1):
        ans += "WARNING: might not converge\n"
    iter = 0
    gx =  lambdify(x,gx_str)
    ea = 0
    ea_old = 0
    while(iter<it):
        ea_old = ea
        xr_old = xr
        xr = gx(xr_old)
        print(xr)
        if(xr != 0):
            ea = (abs((xr-xr_old)/xr))*100
        print(ea)
        if(abs(ea)>abs(ea_old) and iter>5 and abs(xr) > abs(xr_old)):
            return "divergent"
        iter += 1
        if(ea<es):
            break
    ans += "iter: "+str(iter)+"\n"
    ans += f"error = {ea}\n"
    ans += str(xr)+"\n"
    return ans




# if __name__ == '__main__':
#     str =input("expression\n")
#     #f=  lambdify(x,str)
#     FixedPoint(2,0.000001,10,str)


def bisection(functionString,lowerBound,upperBound,error,maxIterations,sigfigures):
    global x
    expression =  lambdify(x,functionString,"numpy")
    if(expression(lowerBound)*expression(upperBound)>0):
        return "Even number of roots in the given interval. Please try another bounds."
    xrOld =0.0
    for i in range(1,maxIterations,1):
        # plotGraph(expression,lowerBound,upperBound)
        xr = round(((upperBound+lowerBound)/2.0),sigfigures)
        if(xr != 0):
            ea =abs((xr-xrOld)/xr)
        else:
            ea=1
        test =expression(lowerBound)*expression(xr)
        if(test<0):
            upperBound =xr
        elif(test ==0):
            ea =0
        else:
            lowerBound=xr
        if(ea<error):
            break
        xrOld =xr
        print(f"\nroot={xr} \nIterations={i} \nxl ={lowerBound}\nxu={upperBound}")
    print(f"error = {ea}")
    return xr
    
    




# if __name__ == "__main__" :
#     functionString =input("expression\n")
    
#     bisection(functionString,0,2,0.001,500,5)
#     #falsePosition(f,-10,10,0.00001,100,5)
#     print("hello")




def secant(function, initailGuess_1, initialGuess_2, sf, eps, iterations):
    x, y = symbols("x, y")
    expr = sympify(function)
    xi_1 = initailGuess_1
    xi_2 = initialGuess_2
    root = 0

    ea=0
    ea_old=0

    if sf == 0:
        sf = 10
    if eps == 0:
        eps = 0.00001
    if iterations == 0:
        iterations = 50
    for i in range(iterations):
        try:
            root = xi_2 - float(expr.subs(x, xi_2))*(xi_2 - xi_1) / (float(expr.subs(x, xi_2)) - float(expr.subs(x, xi_1)))
        except:
            return "Please try another guesses."
        print(i, ":", root)
        if(root != 0):
            ea=abs((root - xi_2) / root * 100 )
        if ea < eps:
            print("Bound of relative error is met!!")
            print(f"error = {ea}")
            return root
        if abs(ea)>abs(ea_old) and i>5 and abs(root) > abs(xi_2):
            return "divergent"
        if(root == 0 and xi_2 == 0):
            return 0
        xi_1 = xi_2
        xi_2 = root
        ea_old=ea
    print(f"error = {ea}")
    return root



# if __name__ == '__main__':
#     '''x, y = symbols("x, y")
#     expr = exp(x)
#     #expr = diff(expr)

#     print(expr.subs(x, 2).evalf())'''
#     function = input('Enter the function: ')
#     xi_2 = float(input('Enter initial guess x(i-1): '))
#     xi_1 = float(input('Enter initial guess x(i): '))
#     sf = int(input('Enter number of SFs: '))
#     iterations = int(input('Enter number of iterations: '))
#     eps = float(input('Enter bound of relative error: '))
#     print("Result: ", secant(function, xi_1, xi_2, sf, eps, iterations))




def newtonRaphson(function, initailGuess, sf, eps, iterations):
    x, y = symbols("x, y")
    expr = sympify(function)
    diffFunc = diff(expr)
    oldRoot = initailGuess
    ea=0
    ea_old = 0

    if sf == 0:
        sf = 10
    if eps == 0:
        eps = 0.00001
    if iterations == 0:
        iterations = 50
    for i in range(iterations):
        try:
            root = round(oldRoot - float((expr.subs(x, oldRoot).evalf())) / float((diffFunc.subs(x, oldRoot).evalf())), sf)
        except:
            return "Please try another guess"
            
        print(i, ": ", root)
        if(root != 0):
            ea=abs((root - oldRoot) / root * 100 )
        if ea< eps:
            print("Bound of relative error is met!!")
            print(f"error = {ea}")
            return root
        if abs(ea)>abs(ea_old) and i>5 and abs(root) > abs(oldRoot):
            return "divergent"
        if(root == 0 and oldRoot == 0):
            return 0
        oldRoot = root
        ea_old=ea
    print(f"error = {ea}")
    return oldRoot



# if __name__ == '__main__':
#     '''x, y = symbols("x, y")
#     expr = exp(x)
#     #expr = diff(expr)

#     print(expr.subs(x, 2).evalf())'''
#     function = input('Enter the function: ')
#     x = float(input('Enter initial guess: '))
#     sf = int(input('Enter number of SFs: '))
#     iterations = int(input('Enter number of iterations: '))
#     eps = float(input('Enter bound of relative error: '))
#     print("Result: ", newtonRaphson(function, x, sf, eps, iterations))


def falsePosition(functionString, lowerBound,upperBound,es,maxIterations,sigFigures):
    global x
    function =  lambdify(x,functionString,"numpy")
    a =[]
    b =[]
    ya =[]
    yb =[]
    x_arr =[]
    y =[]
    
    a.insert(0,lowerBound)
    b.insert(0,upperBound)
    ya.insert(0,function(a[0]))
    yb.insert(0,function(b[0])) 
    if ((ya[0]*yb[0])>0.0):
        return "function has same sign at end points"
    print("step             xl          xu          xr          f(xr)")
    for i in range(0,maxIterations):
        try:
            x_arr.insert(i,round((b[i] -yb[i] *(b[i]-a[i])/(yb[i]-ya[i])),sigFigures))
        except:
            return "Please try another bounds"
        y.insert(i,function(x_arr[i]))
        if(y[i]==0.0):
            print("exact zero found")
            return x_arr[i]
        elif((y[i]*ya[i])<0):
            a.insert(i+1,a[i])
            ya.insert(i+1,ya[i])
            b.insert(i+1,x_arr[i])
            yb.insert(i+1,y[i])
        else:
            a.insert(i+1,x_arr[i])
            ya.insert(i+1,y[i])
            b.insert(i+1,b[i])
            yb.insert(i+1,yb[i])
        if((i>1) and ((abs((x_arr[i]-x_arr[i-1])/x_arr[i]))<es)):
            print("false position method has converged")
            print(f"error = {(abs((x_arr[-1]-x_arr[-2])/x_arr[-1]))}")
            return x_arr[i]
        iter =i
        print(f"{iter}          {a[i]}          {b[i]}          {x_arr[i]}          {y[i]}")
    if(iter>= maxIterations):
        print("zero not found to desired tolerance")
    print(f"error = {(abs((x_arr[-1]-x_arr[-2])/x_arr[-1]))}")
    return x_arr[-1]
    
    




# if __name__ == "__main__" :
#     functionString =input("expression\n")
    
#     # bisection(f,0.0,0.11,0.001,500,5)
#     falsePosition(functionString,5,10,0.00000001,100,5)
#     print("hello")

# if __name__ == '__main__':
#     '''x, y = symbols("x, y")
#     expr = exp(x)
#     #expr = diff(expr)

#     print(expr.subs(x, 2).evalf())'''
#     function = input('Enter the function: ')
#     initialGuess = float(input('Enter initial guess: '))
#     sf = int(input('Enter number of SFs: '))
#     iterations = int(input('Enter number of iterations: '))
#     eps = float(input('Enter bound of relative error: '))
#     root = newtonRaphson(function, initialGuess, sf, eps, iterations)
#     print("Result: ", root)

def graph_function(functionString, lower, upper, is_fixed_pt):
    x = symbols("x")
    y = sympify(functionString)
    #z = 3 * x
    lam_y = lambdify(x, y, modules=['numpy'])
    fig = mpl.figure()
    a1 = fig.add_axes([0,0,1,1])
    a1.set_ylim(-100,100)
    ax = mpl.gca()
    ax.spines['top'].set_color('none')
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    start, end = ax.get_xlim()
    x_vals = np.linspace(-10, 10, 100)
    y_vals = lam_y(x_vals)
    if(is_fixed_pt):
        z = x
        lam_z = lambdify(x, z, modules=['numpy'])
        z_vals = lam_z(x_vals)
        mpl.plot(x_vals, z_vals, "g")

    mpl.plot(x_vals, y_vals, "r")
    #mpl.plot(x_vals, z_vals, "y")
    if(lower != None):
        plt.axvline(x=lower, color="b")
    if(upper != None):
        plt.axvline(x=upper, color="y")
    # loc = plticker.MultipleLocator(base=1.0)
    # ax.xaxis.set_major_locator(loc)

    mpl.show()






