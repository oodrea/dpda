# STALGCM Case Study DPDA
Deterministic Pushdown Automata Implementation in Python

STALGCM S12 | AY 22-23
Case Study

- Lapuz, Mari Salvador
- Roco, Gwen Kathleen
- Tabadero, Audrea Arjaemi

## Machine Definition Format for DPDA:

### 1. Number of States
- This represents the total number of states in the DPDA.
  - Example: `3` (There are 3 states in the DPDA)

### 2. List of States
- This is a ***space-separated*** list of state names.
  - Example: 
    ```
    q0 q1 q2
    ```
    There are three states: `q0`, `q1`, and `q2`.

### 3. Number of Input Symbols
- Represents the total number of input symbols the DPDA recognizes.
  - Example: `2` (There are 2 input symbols)

### 4. List of Input Symbols
- A ***space-separated list*** of the input symbols.
  - Example: 
    ```
    a b
    ```
    The DPDA recognizes two symbols: `a` and `b`.

### 5. Transitions
- First, specify the total number of transitions.
- Each subsequent line represents one transition with 5 space-separated items:
  - Current state.
  - Next state.
  - Input symbol being read.
  - Symbol to be popped from stack.
  - Symbol(s) to push onto the stack.
  
  - Example:
    ```
    4
    q0 q0 a λ a
    q0 q1 b a λ
    q1 q1 b a λ
    q1 q2 λ Z λ
    ```
    - - The first transition means: From state `q0`, when the input symbol `a` is read and the symbol to be popped from the stack is `λ` (indicating it's empty), move to state `q0` and push the symbol `a` onto the stack.

### 6. Start State
- Specifies the initial state of the DPDA.
  - Example: 
    ```
    q0
    ```
    The DPDA starts in state `q0`.

### 7. Final/Accepting State(s)
- The state(s) where if the DPDA ends, the input string is accepted.
  - Example: 
    ```
    q2
    ```
    If the DPDA ends in state `q2`, the input string is accepted.

### Machine Definition Things to Take Note of

1. **Determinism**: The program assumes that the provided machine definition is deterministic. If non-deterministic behaviors are detected, the behavior of the program might be unpredictable.

2. **Lambda (λ) Representation**: In the machine definition, the symbol `λ` serves multiple purposes:
    - Indicating a transition that does not consume an input.
    - Representing the action of popping nothing from the stack.
    - Signifying the act of pushing nothing onto the stack.

3. **Input Validity**: Ensure that the machine definition strictly adheres to the aforementioned format. Any deviations might lead to unexpected errors or behaviors.

## Additional Guidelines
- Graphviz is needed for the creation of the diagram feature. [Download Graphviz](https://graphviz.org/download/)
- It is preferable to have the Machine Definition File in .txt format.



