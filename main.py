"""
Main Program

STALGCM S12 | AY 22-23
Case Study Implementation | Deterministic Pushdown Automata (DPDA)

Lapuz, Mari Salvador
Roco, Gwen Kathleen
Tabadero, Audrea Arjaemi

"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, Label, Entry, Button, Text, StringVar, Radiobutton
from graphviz import Digraph, ExecutableNotFound
from datetime import datetime

# Stack Class used in DPDA
class Stack:

    def __init__(self):
        self.data = ['Z']

    def isEmpty(self):
        return len(self.data) == 0

    def pop(self):
        if not self.isEmpty():
            elem = self.data[0]
            del self.data[0]
            return elem
        else:
            return None
    
    def push(self, elem):
        for char in elem:
            if (char != "λ"):
                  self.data.insert(0, char)

    def peek(self):
        if not self.isEmpty():
            return self.data[0]
        return -1
    
    def getReverse(self):
        reverse = self.data[:]
        reverse.reverse()
        return ''.join(reverse)

    def __str__(self):
        return str(self.data[::-1])

# PDAConfiguration Class used in Trace
class PDAConfiguration:
    def __init__(self, state, currinput, stack, remaining_input, status=None):
        self.state = state
        self.currinput = currinput
        self.stack = stack
        self.remaining_input = remaining_input
        self.status = status 

# Main DPDA Class
class PDA:

    def __init__(self, states, start, accept, statesLst, input_symbols, acceptance):
        self.statesLst = statesLst
        self.states = states 
        self.stack = Stack()
        self.start = start
        self.accept = accept
        self.configsList =[]
        self.input_symbols = input_symbols
        self.acceptance=acceptance

    # Used in Trace
    def add_configuration(self, state, currinput, stack, remaining_input, status):
        config = PDAConfiguration(state, currinput, stack, remaining_input, status)
        self.configsList.append(config)
    
    # Used in Trace
    def config_generator(self):
        for config in self.configsList:
            yield config

    # Transition Checker
    def _isDefinedTransition(self, state, c, stackTop):
        for transition in state:
            if c == transition['READ'] and (stackTop == transition['POP'] or transition['POP'] == 'λ'):
                return True, transition
        return False, None

    # Gets state name
    def get_state_name(self, state):
        return self.statesLst[state]

    # Main function for DPDA
    def test(self, inputString):
        string = inputString + 'λ'
        initialState = self.start
        currState = initialState
        stackTop = self.stack.peek()
        status=""

        if len(string) == 0:
            return False
        self.add_configuration(self.get_state_name(currState), None, self.stack.__str__(), inputString, None)

        # If acceptance mode is by Final State
        if(self.acceptance=="final_state"):
            for i in range(len(string)):
                result, transition = self._isDefinedTransition(self.states[currState], string[i], stackTop)
                remainingStr = inputString[i+1:]
                currinput=string[i]
                
                if result:
                    if transition["POP"] != 'λ' and transition["POP"] == stackTop:
                        self.stack.pop()
                        self.add_configuration(self.get_state_name(currState), currinput, self.stack.__str__(), remainingStr, None)
                    if transition["PUSH"] != 'λ':
                        self.stack.push(transition["PUSH"])
                        self.add_configuration(self.get_state_name(currState), currinput, self.stack.__str__(), remainingStr, None)
                    
                    stackTop = self.stack.peek()
                    currState = transition['TO']
                    
                    if i == len(string) - 1 and currState in self.accept:
                        status = f"Input Accepted: Reached a Final State({self.get_state_name(currState)})."
                        self.add_configuration(self.get_state_name(currState), currinput, self.stack.__str__(), remainingStr, status)
                        return True
                else:
                    return False
        
        # If acceptance mode is by Empty Stack
        elif self.acceptance == "empty_stack":
            for i in range(len(string)):
                result, transition = self._isDefinedTransition(self.states[currState], string[i], stackTop)
                remainingStr = inputString[i+1:]
                currinput = string[i]
                
                if result:
                    if transition["POP"] != 'λ' and transition["POP"] == stackTop:
                        self.stack.pop()
                        self.add_configuration(self.get_state_name(currState), currinput, self.stack.__str__(), remainingStr, None)
                        if self.stack.isEmpty(): 
                            self.add_configuration(self.get_state_name(currState), currinput, self.stack.__str__(), remainingStr, "Input Accepted: Resulting Stack is Empty.")
                            return True
                    if transition["PUSH"] != 'λ':
                        self.stack.push(transition["PUSH"])
                        self.add_configuration(self.get_state_name(currState), currinput, self.stack.__str__(), remainingStr, None)
                    
                    stackTop = self.stack.peek()
                    currState = transition['TO']
                else:
                    return False
            return False  
        
        # Acceptance mode is by Both Final State and Empty Stack
        elif(self.acceptance=="both"):
            for i in range(len(string)):
                result, transition = self._isDefinedTransition(self.states[currState], string[i], stackTop)
                remainingStr = inputString[i+1:]
                currinput=string[i]
                
                if result:
                    if transition["POP"] != 'λ' and transition["POP"] == stackTop:
                        self.stack.pop()
                        self.add_configuration(self.get_state_name(currState), currinput, self.stack.__str__(), remainingStr, None)
                    if transition["PUSH"] != 'λ':
                        self.stack.push(transition["PUSH"])
                        self.add_configuration(self.get_state_name(currState), currinput, self.stack.__str__(), remainingStr, None)
                    
                    stackTop = self.stack.peek()
                    currState = transition['TO']
                    
                    if i == len(string) - 1 and self.stack.isEmpty() and currState in self.accept:
                        self.add_configuration(self.get_state_name(currState), currinput, self.stack.__str__(), remainingStr, "Input Accepted.")
                        return True
                else:
                    return False
        
        return False

# Conversion to Internal Representation
def read_npda_from_file(file_path, acceptance_mode):
    with open(file_path, 'r', encoding='utf-8') as file:
        N = int(file.readline().strip())  # number of states
        states_list = list(map(str, file.readline().strip().split()))  # list of states
        T = int(file.readline().strip())  # number of input symbols
        input_symbols = file.readline().strip().split()  # list of input symbols
        num_transitions = int(file.readline().strip())  # number of transitions

        states = [ [] for _ in range(N) ]
        for _ in range(num_transitions):
            #FROM state Q to O, reading A, popping E and pushing D
            Q, O, A, E, D = file.readline().strip().split()
            intQ = states_list.index(Q)
            intO = states_list.index(O)
            Q, O = map(int, (intQ, intO))
            transition = {"FROM":Q, "TO":O, "READ":A, "POP":E, "PUSH":D}
            states[Q].append(transition)

        S = (file.readline().strip())  # initial state
        C_str = file.readline().strip().split()
        C = [states_list.index(state) for state in C_str] # final/accepting states
        intS = states_list.index(S)

    dpda = PDA(states, intS, C, states_list, input_symbols, acceptance_mode)
    return dpda


# GUI
class PDA_GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("STALGCM | Case Study DPDA Implementation")
        self.dpda = None 
        self.filename = None  
        self.verdict = None
        self.create_widgets()
        self.generator_obj=None

    # Displays Initial Info of DPDA
    def display_info(self):
        self.output_text.insert(tk.END, f"List of States: {', '.join(str(state) for state in self.dpda.statesLst)}\n")
        self.output_text.insert(tk.END, f"Initial State: {self.dpda.statesLst[self.dpda.start]}\n")
        self.output_text.insert(tk.END, f"Final State/s: {', '.join(str(self.dpda.statesLst[i]) for i in self.dpda.accept)}\n")
        self.output_text.insert(tk.END, "-----------------------\n")
    
    # Load DPDA Machine Definition File
    def load_dpda_file(self):
        self.filename = filedialog.askopenfilename()
        if self.filename:  # Check if a file has been selected
            self.set_dpda()
            self.reset_button.grid_remove()
            PDA_GUI.display_info(self)
            self.generate_diag_button.grid(row=2, column=0, sticky="WE")
            self.file_name_label.grid(row=1, column=0, sticky="W")
            self.file_name_label.config(text=f"Loaded file: {os.path.basename(self.filename)}", fg="green")
        else:
            messagebox.showerror("No File Selected", "Please select a file.")

    # Set DPDA
    def set_dpda(self):
        if self.filename is not None:
            acceptance_mode = self.acceptance.get()
            self.dpda = read_npda_from_file(self.filename, acceptance_mode)
            # Reset the generator_obj
            self.generator_obj = None
            # Reset the button to Trace
            self.trace_step_button.config(text="Trace", command=self.trace)
            # Clear the output_text
            self.output_text.delete(1.0, tk.END)
    
    # Run DPDA
    def run_dpda(self):
        # Check if DPDA is loaded
        if self.dpda is None:
            messagebox.showerror("Error", "No valid DPDA loaded.")
            return
        
        self.set_dpda()  # Reset the DPDA before running it
        self.output_text.delete('1.0', tk.END)
        PDA_GUI.display_info(self)
        input_string = self.input_entry.get()

        # Run the DPDA and get the result
        self.verdict = self.dpda.test(input_string)
        self.output_text.insert(tk.END, f"Input String: {input_string}\n")
        self.output_text.insert(tk.END, f"Accept By: {'Final State' if self.dpda.acceptance == 'final_state' else 'Empty Stack' if self.dpda.acceptance == 'empty_stack' else 'Both'}\n")
        self.output_text.insert(tk.END, f"Verdict: {'Accepted' if self.verdict else 'Rejected'}\n")
        self.output_text.insert(tk.END, "-----------------------\n")    
        
    # Reset DPDA
    def reset(self):
        self.generator_obj = None
        self.trace_step_button.config(text="Trace", command=self.trace)
        self.reset_button.grid_forget()  
        self.output_text.delete("1.0", tk.END) 
        PDA_GUI.display_info(self)

        self.output_text.insert(tk.END, f"Input String: {self.input_entry.get()}\n")
        self.output_text.insert(tk.END, f"Accept By: {'Final State' if self.dpda.acceptance == 'final_state' else 'Empty Stack' if self.dpda.acceptance == 'empty_stack' else 'Both'}\n")
        self.output_text.insert(tk.END, f"Verdict: {'Accepted' if self.verdict else 'Rejected'}\n")
        self.output_text.insert(tk.END, "-----------------------\n")    


    # Trace DPDA
    def trace(self):
        # Check if DPDA is loaded and has valid transitions
        if self.dpda is None:
            messagebox.showerror("Error", "No valid DPDA loaded.")
            return
        self.generator_obj = self.dpda.config_generator()
        self.next_step()
        
        # Change button to 'Next Step'
        self.trace_step_button.config(text="Next Step", command=self.next_step)
        self.reset_button.grid(row=12, column=0, columnspan=2, sticky="WE")


    # Next Step in Trace
    def next_step(self):
        try:
            config = next(self.generator_obj)
                        
            output_str = ""
            output_str += f"Current State: {config.state}\n"
            output_str += f"Current Symbol: {config.currinput}\n"
            output_str += f"Unprocessed Input: {config.remaining_input}\n"
            output_str += f"Stack: {config.stack}\n" 
            output_str += "-----------------------\n"

            self.output_text.insert(tk.END, output_str)
            if config.status:
                self.output_text.insert(tk.END, f"{config.status}\n")

        except StopIteration:
            # No more configurations, the DPDA has finished running
            self.output_text.insert(tk.END, f"End of DPDA run.\n")
            messagebox.showinfo("stop da car", "Reached End of DPDA Run.")

        self.output_text.see(tk.END)


    # Create DPDA Diagram; Graphiz needed.
    def create_graph(self):
        def is_tool(name):
            from shutil import which
            return which(name) is not None

        try:
            if not is_tool("dot"):
                messagebox.showerror("Error", "Graphviz is not installed on this system. Please install it to make use of generate diagram feature.")
                raise Exception("Graphiz not found.")
            dot = Digraph()

            dot.node('pseudo_start', '', width='0', shape='none')
            dot.edge('pseudo_start', self.dpda.statesLst[self.dpda.start], color='black', len='0.05')

            for state in self.dpda.statesLst:
                if self.dpda.statesLst.index(state) == self.dpda.start:
                    dot.node(state, shape='circle', color='black')
                elif self.dpda.statesLst.index(state) in self.dpda.accept:
                    dot.node(state, shape='doublecircle', color='black')
                else:
                    dot.node(state, shape='circle', color='black')

            for state_transitions in self.dpda.states:
                for transition in state_transitions:
                    state = self.dpda.statesLst[transition['FROM']]
                    next_state = self.dpda.statesLst[transition['TO']]
                    input_symbol = transition['READ']
                    pop = transition['POP']
                    push = transition['PUSH']
                    dot.edge(str(state), str(next_state), label=f"   {input_symbol}, {pop} ; {push}")
    
            now = datetime.now()
            timestamp_str = now.strftime("%y%m%H%M%S")

            file_name = os.path.splitext(self.filename)[0]
            file_name+= timestamp_str
            file_name+="_diagram"
            dot.render(file_name, view=True)
            os.remove(f"{file_name}")
            self.diag_file.grid(row=3, column=0, sticky="W")
            self.diag_file.config(text=f"Generated File: {os.path.basename(file_name)}.pdf", fg="green")

        except ExecutableNotFound as e:
            messagebox.showerror("Error", "Graphviz is not installed on this system. Please install it to make use of generate diagram feature.")
    

    # Widgets for GUI
    def create_widgets(self):
        # Select Machine Definition File
        self.file_select_button = Button(self.window, text="Select DPDA Machine Definition File", command=self.load_dpda_file)
        self.file_select_button.grid(row=0, column=0, sticky="WE")
        self.file_name_label = Label(self.window, text="")
        self.file_name_label.grid(row=1, column=0, sticky="W")
        self.file_name_label.grid_remove()  

        # Generate DPDA Diagram
        self.generate_diag_button = Button(self.window, text="Generate DPDA Diagram", command=self.create_graph)
        self.generate_diag_button.grid(row=2, column=0, sticky="WE")
        self.generate_diag_button.grid_remove()  
        self.diag_file = Label(self.window, text="")
        self.diag_file.grid(row=3, column=0, sticky="W")
        self.diag_file.grid_remove()  

        # Input String
        self.input_label = Label(self.window, text="Enter Input String:")
        self.input_label.grid(row=4, column=0, sticky="WE")
        self.input_entry = Entry(self.window)
        self.input_entry.grid(row=5, column=0, sticky="WE")

        # Acceptance Mode of DPDA; final state, empty stack, both
        self.acceptance = StringVar()
        self.acceptance.set('final_state')
        self.final_state_button = Radiobutton(self.window, text="Accept by Final State/s", variable=self.acceptance, value='final_state')
        self.empty_stack_button = Radiobutton(self.window, text="Accept by Empty Stack", variable=self.acceptance, value='empty_stack')
        self.both_button = Radiobutton(self.window, text="Both", variable=self.acceptance, value='both')
        self.final_state_button.grid(row=6, column=0, sticky="WE")
        self.empty_stack_button.grid(row=7, column=0, sticky="WE")
        self.both_button.grid(row=8, column=0, sticky="WE")

        # Run button
        self.run_button = Button(self.window, text="Run", command=self.run_dpda)
        self.run_button.grid(row=9, column=0, sticky="WE")

        # Output
        self.output_text = Text(self.window, state='normal')
        self.output_text.grid(row=10, column=0, sticky="WE")

        # Trace DPDA
        self.trace_step_button = Button(self.window, text="Trace", command=self.trace)
        self.trace_step_button.grid(row=11, column=0, sticky="WE")

        # Reset
        self.reset_button = Button(self.window, text="Reset", command=self.reset)
        self.reset_button.grid(row=12, column=0, sticky="WE")
        self.reset_button.grid_remove()  # This will hide the button by default

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    gui = PDA_GUI()
    gui.run()
