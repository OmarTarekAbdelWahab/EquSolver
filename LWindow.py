import tkinter as tk
from tkinter import ttk
from ctypes import windll
from LinearEqSolver import solve
# from decimal import Decimal
# import sympy
# from sympy import *



windll.shcore.SetProcessDpiAwareness(1)



root = tk.Tk()
root.geometry("800x600")
root.resizable(width=False, height=False)
root.minsize(800, 600)
root.title("Equ Solver")
root.columnconfigure(0, weight=0)
root.columnconfigure(1, weight=1)


size = tk.IntVar(value=2)
fields_mat = []
textvars_mat = []
b_vec = []
b_textvars = []
solution = tk.StringVar()
guess_vec = []
guess_textvars = []
iterations_no = tk.StringVar(value="100")
sig_figs = tk.IntVar(value=1)
rel_error_var = tk.StringVar(value="0.1")
time = 0




        
def add_new_column(fields_mat, textvars_mat, mat_holder):
    for i in range(0, len(fields_mat)):
        textvar = tk.StringVar(value="0")
        textvars_mat[i].append(textvar)
        field = ttk.Entry(mat_holder, width=5, textvariable=textvar, justify="center")
        fields_mat[i].append(field)
        field.grid(row=i, column=len(fields_mat[0])-1, padx=15, pady=15, sticky="ew")

def pop_last_column(fields_mat, textvars_mat):
    for i in range(0, len(fields_mat)):
        fields_mat[i][-1].destroy()
        fields_mat[i].pop()
        textvars_mat[i].pop()

def add_new_row(fields_mat, textvars_mat, mat_holder):
    field_lst=[]
    textvar_lst = []
    for j in range(0, len(fields_mat[0])):
        textvar = tk.StringVar(value="0")
        textvar_lst.append(textvar)
        field = ttk.Entry(mat_holder, width=5, textvariable=textvar, justify="center")
        field_lst.append(field)
        field.grid(row=len(fields_mat), column=j, padx=15, pady=15, sticky="ew")
    fields_mat.append(field_lst)
    textvars_mat.append(textvar_lst)

def pop_last_row(fields_mat, textvars_mat):
    for j in range(0, len(fields_mat[0])):
        fields_mat[-1][j].destroy()
    fields_mat.pop()
    textvars_mat.pop()




def draw_field_matrix(mat_holder):
    global fields_mat
    global textvars_mat
    global size
    old_size= len(fields_mat)
    new_size = size.get()

    if (new_size == old_size): return
    elif (new_size > old_size):
        for i in range(old_size, new_size):
            add_new_column(fields_mat, textvars_mat, mat_holder)
        for i in range(old_size, new_size):
            add_new_row(fields_mat, textvars_mat, mat_holder)
        
    
    elif (new_size < old_size):
        for i in range(new_size, old_size):
            pop_last_column(fields_mat, textvars_mat)
        for i in range(new_size, old_size):
            pop_last_row(fields_mat, textvars_mat)

def draw_vec(b_vec, vec_holder, b_textvars):
    global size
    old_size = len(b_vec)
    new_size = size.get()

    if(new_size == old_size): return
    elif(new_size > old_size):
        for i in range(old_size, new_size):
            textvar = tk.StringVar(value="0")
            field = ttk.Entry(vec_holder, width=5, textvariable=textvar, justify="center")
            b_vec.append(field)
            b_textvars.append(textvar)
            field.grid(row=i, column=0, padx=15, pady=15, sticky="ew")
    elif(new_size < old_size):
        for i in range(new_size, old_size):
            b_vec[-1].destroy()
            b_vec.pop()
            b_textvars.pop()

    

def mat_init():
    global fields_mat
    global textvars_mat
    global mat_holder

    for i in range(0,2):
        field_lst=[]
        textvar_lst = []
        for j in range(0,2):
            textvar = tk.StringVar(value="0")
            textvar_lst.append(textvar)
            field = ttk.Entry(mat_holder, width=5, textvariable=textvar, justify="center")
            field_lst.append(field)
            field.grid(row=i, column=j, padx=15, pady=15, sticky="ew")
        fields_mat.append(field_lst)
        textvars_mat.append(textvar_lst)

def vec_init():
    global b_vec
    global b_textvars
    global vec_holder

    for i in range(0, 2):
        textvar = tk.StringVar(value="0")
        b_textvars.append(textvar)
        field = ttk.Entry(vec_holder, width=5, textvariable=textvar, justify="center")
        b_vec.append(field)
        field.grid(row=i, column=0, padx=15, pady=15, sticky="ew")

def guess_init(vec_holder):
    global guess_vec
    global guess_textvars
    global size

    #reset
    for field in guess_vec:
        field.destroy()
    guess_vec = []
    guess_textvars = []

    #redraw
    for i in range(0, size.get()):
        textvar = tk.StringVar(value="1")
        guess_textvars.append(textvar)
        field = ttk.Entry(vec_holder, width=5, textvariable=textvar, justify="center")
        guess_vec.append(field)
        field.grid(row=0, column=i, padx=15, pady=15, sticky="ew")
    

def get_system():
    global textvars_mat
    global b_textvars
    global guess_textvars
    mat = []
    vec = []
    try:
        mat = [[float(textvar.get()) for textvar in lst] for lst in textvars_mat]
        vec = [float(textvar.get()) for textvar in b_textvars]
        guess = [float(textvar.get()) for textvar in guess_textvars]
        
    except:
        print("Please enter valid input.")
        return None
    return  mat,vec,guess




#############################################################################################
#left side setup

op_frame = ttk.Frame(root, padding=(30, 15))
op_frame.grid(row=0, column=0, sticky="nsew")

main_options_frame = ttk.Frame(op_frame, padding=(30,15))
main_options_frame.pack(side="top")


opselect_label = ttk.Label(main_options_frame, text='Select an operation:',padding=(30, 15), font=("Helvetica", "10"))
opselect_label.grid(row=0, column=0)

ttk.Label(main_options_frame, text='Significant digits: ').grid(row=4, column=0)
sig_fig_spinner = ttk.Spinbox(main_options_frame, from_=1, to_=20, state='readonly', wrap="true", textvariable=sig_figs)
sig_fig_spinner.grid(row=4, column=1)



operation = tk.StringVar()

def draw_error_label(holder, sig_fig_var)->ttk.Label:
    return ttk.Label(holder, text=f"Relative error: {str(0.5 * (10 ** (2 - sig_fig_var.get())))}%")

def draw_guess_options(holder):
    global sig_figs
    global iterations_no

    #iter_options_holder = ttk.Frame(op_frame, padding=(30,15))
    holder.pack(side='top', expand="false")
    ttk.Label(holder, text="Initial guess" ).grid(row=0, column=0)
    guess_holder = ttk.Frame(holder)
    guess_holder.grid(row=0, column=1)
    guess_init(guess_holder)
    ttk.Label(holder, text="Stopping criteria").grid(row=1, column=0)
    ttk.Label(holder, text="Number of iterations").grid(row=2, column=0)
    iter_field = ttk.Entry(holder, justify='center', textvariable=iterations_no)
    iter_field.grid(row=2, column=1)
    ttk.Label(holder, text="Relative error").grid(row=3, column=0)

    error_field = ttk.Entry(holder, textvariable=rel_error_var, justify="center")
    error_field.grid(row=3, column=1)

    # label = draw_error_label(holder, sig_fig_var=sig_figs)
    # label.grid(row=5, column=0)

    
    



def hide_guess_options():
    global iter_options_holder
    iter_options_holder.pack_forget()


def on_choice(event):
    global operation
    global iter_options_holder
    choice = operation.get()
    if(choice == "Gauss-Seidel Method" or choice == "Jacobi Iterations"):

        draw_guess_options(iter_options_holder)
    else:
        hide_guess_options()

opselect = ttk.Combobox(main_options_frame, textvariable=operation, state="readonly", values=['Gauss Elimination', 
'Gauss-Jordan', 'LU-Downlittle', 'LU-Cholseky', 'LU-Crout', 'Gauss-Seidel Method', 'Jacobi Iterations'], )
opselect.grid(row=0, column=1)

opselect.bind("<<ComboboxSelected>>", on_choice)


size_label = ttk.Label(main_options_frame, text="System size:")
size_label.grid(row=1, column=0)


#size_entry = ttk.Entry(op_frame, textvariable=size_str)
#size_entry.grid(row=2, column=0)
size_spinner = ttk.Spinbox(main_options_frame, from_=2, to_=10, state="readonly", wrap="true", textvariable=size)
size_spinner.grid(row=1, column=1)

def draw_system(mat_holder, b_vec, vec_holder, b_textvars):
    draw_field_matrix(mat_holder)
    draw_vec(b_vec, vec_holder, b_textvars)
    on_choice("")
    

button = ttk.Button(main_options_frame, text="Change matrix", command=lambda:draw_system(mat_holder, b_vec, vec_holder, b_textvars))
button.grid(row=3, column=0)

iter_options_holder = ttk.Frame(op_frame, padding=(30,15))
iter_options_holder.pack(side='top')


#draw_guess_options(iter_options_holder)


###################################################################################
#right side i/o

input_frame = ttk.Frame(root, padding=(30,15))
input_frame.grid(row=0, column=1, sticky="nsew")



mat_frame = ttk.Frame(input_frame, padding=(30,15))
mat_frame.pack(side='top', fill="both", expand="true")
mat_frame.columnconfigure(0, weight=1)
mat_frame.rowconfigure(0, weight=1)


mat_holder = ttk.Frame(mat_frame, padding=(30,15))
# mat_holder.grid(row=0, column=0, sticky="nsew")
mat_holder.pack(side="left", fill="both", expand="true")

ttk.Separator(mat_frame, orient="vertical").pack(side="left", fill="y", expand="true")

vec_holder = ttk.Frame(mat_frame, padding=(30,15))
vec_holder.pack(side="left", fill="both", expand="true")

solution_label = ttk.Label(input_frame, padding=(30, 15), textvariable=solution)
solution_label.pack(side="bottom")




def get_solution():
    global operation
    global size
    global solution
    global solution_label
    global iterations_no
    global sig_figs
    global time
    
    a = []
    b = []
    x = []

    # print(a)
    # print(b)
    # print(x)
    # print(size.get())
    # print(operation.get())

    
    # int(size.get())
    # int(iterations_no.get())
    # float(rel_error_var.get())
    system = get_system()
    a = system[0]
    b = system[1]
    x = system[2]

    temp = ""
    if(operation.get()=="Jacobi Iterations" or operation.get()=="Gauss-Seidel Method"):
        temp = solve(operation.get(), a, b, size.get(), sig_figs.get(), x, int(iterations_no.get()), float(rel_error_var.get()))
    else:
        temp = solve(operation.get(), a, b, size.get(), sig_figs.get())

    solution.set(temp[0])
    time = temp[1]

    solution.set("Please enter valid input")
    return

    
    #print(solve(operation.get(), a, b, size.get()))
    sol_str = solution.get()
    #print(sol_str)

    solution_label.destroy()
    solution_label = ttk.Label(input_frame, padding=(30, 15), text=sol_str)
    solution_label.pack(side="bottom")


    steps_screen.delete("1.0", tk.END)
    steps_screen.insert(tk.END,  f"Took {temp[1]} ns\n")



solve_button = ttk.Button(input_frame, text="Solve!", command=get_solution)
solve_button.pack()


mat_init()
vec_init()
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

# x,y,z = symbols('a,b,c')
# x2,y2,z2 = symbols('e,f,g')
# arr = [[x,y,z],[x2,y2,z2]]
# result = [[x,y,z],[]]
# for i in range(0,3):
#     #print(arr[1][i]-(arr[1][0]/arr[0][0])*arr[0][i])
#     exp = arr[1][i]-(arr[1][0]/arr[0][0])*arr[0][i]
#     #print(exp)
#     result[1].append(exp)
# for lst in result:
#     print([exp for exp in lst])