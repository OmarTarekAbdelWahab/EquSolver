import tkinter as tk
from tkinter import ttk
from ctypes import windll
from sympy import *
import RootFinder as rf
import time


windll.shcore.SetProcessDpiAwareness(1)



root = tk.Tk()
root.geometry("800x600")
root.resizable(width=False, height=False)
root.minsize(800, 600)
root.title("Equ Solver")
root.columnconfigure(0, weight=0)
root.columnconfigure(1, weight=1)





solution = tk.StringVar()
equation_var = tk.StringVar()
iterations_no_var = tk.StringVar(value="50")
sig_figs = tk.IntVar(value=10)
rel_error_var = tk.StringVar(value="0.00001")
operation = tk.StringVar()
xl_var = tk.StringVar()
xu_var =tk.StringVar()
xg_var = tk.StringVar()
func_fixed_var = tk.StringVar()


############################################################################################
#functions
def on_choice(event):
    op = operation.get()
    if(op == 'Newton-Raphson'):
        hide_holder(bounds_holder)
        draw_holder(guess_holder)
        hide_holder(func_fixed_holder)
    elif(op == "Fixed Point"):
        hide_holder(bounds_holder)
        draw_holder(guess_holder)
        draw_holder(func_fixed_holder)
    else:
        hide_holder(guess_holder)
        draw_holder(bounds_holder)
        hide_holder(func_fixed_holder)

def graph():
    try:
        op = operation.get()
        
        functionString = equation_var.get()
        gx_str = func_fixed_var.get()
        

        if(op == "Bisection" or op == "False-Position"):
            xl = float(xl_var.get())
            xu = float(xu_var.get())
            rf.graph_function(functionString, xl, xu, False)
        elif(op == "Fixed Point"):
            guess =  float(xg_var.get())
            rf.graph_function(gx_str, guess, None, True)
        elif(op == "Newton-Raphson"):
            guess =  float(xg_var.get())
            f = diff(sympify(functionString))
            rf.graph_function(functionString, guess, None, False)
            rf.graph_function(str(f), guess, None, False)
        elif(op == "Secant Method"):
            xl = float(xl_var.get())
            xu = float(xu_var.get())
            f = diff(sympify(functionString))
            rf.graph_function(functionString, xl, xu, False)
            rf.graph_function(str(f), xl, xu, False)
    except:
        print("Check your input")

def draw_holder(holder):
    #holder.grid(row=row, column=column)
    holder.pack()


def hide_holder(holder):
    #holder.grid_forget()
    holder.pack_forget()

def show_result(result):
    steps_screen.delete("1.0", tk.END)
    steps_screen.insert(tk.END,  result)

def get_solution():
    ns_time = time.perf_counter_ns()
    x = symbols('x')
    op = operation.get()
    equation = ''
    guess = ""
    xl = ""
    xu = ""
    iter_no = 0
    epsilon = 0
    result = ""
    
    if(op == ''):
        return "Please choose an operation"
    # try:
    #     equation = parse_expr(equation_var.get())
    #     print(equation.subs(x, 3).evalf())
    #     print(equation)
    # except:
    #     return
    #     print("Please enter a valid equation")
    try:
        if(op == 'Newton-Raphson' or op == 'Fixed Point'):
            guess = float(xg_var.get())
        else:
            xl = float(xl_var.get())
            xu = float(xu_var.get())
    except:
        return "Please enter valid numbers"
    try:
        iter_no = int(iterations_no_var.get())
    except:
        return "Please input a valid number of iterations"
    try:
        epsilon = float(rel_error_var.get())
    except:
        return "Please enter a valid epsilon value"
    #functions
    ans = ""
    try:
        functionString = equation_var.get()
        if(op == "Bisection"):
            ans = rf.bisection(functionString, xl, xu, epsilon, iter_no, sig_figs.get()) 
        elif(op == "False-Position"):
            ans = rf.falsePosition(functionString, xl, xu, epsilon, iter_no, sig_figs.get())
        elif(op == "Fixed Point"):
            gx = func_fixed_var.get()
            ans = rf.FixedPoint(guess, epsilon, iter_no, gx)
        elif(op == "Newton-Raphson"):
            ans = rf.newtonRaphson(functionString, guess, sig_figs.get(), epsilon, iter_no)
        elif(op == "Secant Method"):
            ans = rf.secant(functionString, xl, xu, sig_figs.get(), epsilon, iter_no)

        final_time = time.perf_counter_ns()
        rf.graph_function(functionString, ans, None, False)
        ans = str(ans)
        ans += f"\n Took {final_time-ns_time} ns"
        return ans
    except:
        return "Please check your function"

    

def solve_button_onclick():
    show_result(get_solution())
    

    
    


    
#############################################################################################
#left side setup/input

op_frame = ttk.Frame(root, padding=(30, 15))
op_frame.grid(row=0, column=0, sticky="nsew")

#holder for main input
main_options_frame = ttk.Frame(op_frame, padding=(30,15))
main_options_frame.pack(side="top")

#operation select
ttk.Label(
    main_options_frame, 
    text='Select an operation:',
    padding=(30, 15), 
    font=("Helvetica", "10")
).grid(row=0, column=0)

opselect = ttk.Combobox(main_options_frame, textvariable=operation, state="readonly", values=['Bisection', 
'False-Position', 'Fixed Point', 'Newton-Raphson', 'Secant Method'], )
opselect.grid(row=0, column=1)

opselect.bind("<<ComboboxSelected>>", on_choice)



#Equation input
ttk.Label(main_options_frame, text='Equation: ').grid(row=1, column=0)
equ_input = ttk.Entry(main_options_frame, textvariable=equation_var)
equ_input.grid(row=1, column=1, padx=30, pady=15)



#upper-lower bounds

bounds_holder = ttk.Frame(op_frame)
#bounds_holder.grid(row=2, column=0)


ttk.Label(bounds_holder, text='Lower bound: ').grid(row=0, column=0)
xl_input = ttk.Entry(bounds_holder, textvariable=xl_var)
xl_input.grid(row=0, column=1, padx=30, pady=15)

ttk.Label(bounds_holder, text='Upper bound: ').grid(row=1, column=0)
xu_input = ttk.Entry(bounds_holder, textvariable=xu_var)
xu_input.grid(row=1, column=1, padx=30, pady=15)


#guess
guess_holder = ttk.Frame(op_frame)
#bounds_holder.grid(row=3, column=0)

ttk.Label(guess_holder, text='Initial guess: ').grid(row=0, column=0)
xg_input = ttk.Entry(guess_holder, textvariable=xg_var)
xg_input.grid(row=0, column=1, padx=30, pady=15)



#g(x)
func_fixed_holder = ttk.Frame(op_frame)

ttk.Label(func_fixed_holder, text="g(x): ").grid(row=0, column=0)
func_fixed_input = ttk.Entry(func_fixed_holder, textvariable=func_fixed_var)
func_fixed_input.grid(row=0, column=1)



#sig fig input
ttk.Label(main_options_frame, text='Significant digits: ').grid(row=5, column=0)
sig_fig_spinner = ttk.Spinbox(main_options_frame, from_=1, to_=20, state='readonly', wrap="true", textvariable=sig_figs)
sig_fig_spinner.grid(row=5, column=1)

#iterations input
ttk.Label(main_options_frame, text='Max. iterations: ').grid(row=6, column=0)
iterations_input = ttk.Entry(main_options_frame, textvariable=iterations_no_var)
iterations_input.grid(row=6, column=1, padx=30, pady=15)

#epsilon/rel-error input
ttk.Label(main_options_frame, text='EPS: ').grid(row=7, column=0)
eps_input = ttk.Entry(main_options_frame, textvariable=rel_error_var)
eps_input.grid(row=7, column=1, padx=30, pady=15)

#graph command button
graph_button = ttk.Button(op_frame, command=graph, text="Plot the function")
graph_button.pack()





def draw_error_label(holder, sig_fig_var)->ttk.Label:
    return ttk.Label(holder, text=f"Relative error: {str(0.5 * (10 ** (2 - sig_fig_var.get())))}%")











###################################################################################
#right side i/o

input_frame = ttk.Frame(root, padding=(30,15))
input_frame.grid(row=0, column=1, sticky="nsew")





solve_button = ttk.Button(input_frame, text="Solve!", command=solve_button_onclick)
solve_button.pack()


###############################################################################

#steps

steps_holder = ttk.Frame(input_frame, padding=(30,15))
steps_holder.pack(side="bottom")

steps_screen = tk.Text(steps_holder,height=10, width=50)
steps_screen.pack(side="left")

scrollbar = ttk.Scrollbar(steps_holder, orient="vertical", command= steps_screen.yview)
scrollbar.pack(side="left", fill="y")
steps_screen["yscrollcommand"] = scrollbar.set




###############################################################################

#to update size automatically
root.geometry("")

root.mainloop()
