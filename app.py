import streamlit as st

st.set_page_config(
    page_title="Free ODE Solver Online - Solve Differential Equations",
    page_icon="📐",
    layout="centered",
    menu_items={
        'About': "Free online tool to solve ordinary differential equations. Supports separable, linear, Bernoulli, exact, and second order ODEs."
    }
)

st.title("Free ODE Solver")
st.markdown("**Solve differential equations instantly.** Enter your ODE below:")
st.markdown("---")
from sympy import *
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

st.set_page_config(page_title="ODE Solver", layout="centered")
st.title("ODE Solver")

x = symbols('x')
y = Function('y')  # This is correct - no (x) here
C1 = symbols('C1')

transformations = (standard_transformations + (implicit_multiplication_application,))

st.write("Examples: `dy/dx - y*tan(x) = -y**2*sec(x)` or `y' + y = sin(x)`")
eq_input = st.text_input("Enter ODE:", "dy/dx - y*tan(x) = -y**2*sec(x)")

if st.button("Solve", type="primary"):
    try:
        eq_str = eq_input.strip()
        eq_str = eq_str.replace("^", "**")
        
        # Step 1: Handle derivatives first
        eq_str = eq_str.replace("dy/dx", "Derivative(y(x), x)")
        eq_str = eq_str.replace("y'", "Derivative(y(x), x)")
        
        # Step 2: Replace standalone y with y(x) 
        # Use word boundaries so we don't replace y in 'dy/dx' which we already handled
        import re
        eq_str = re.sub(r'\by\b', 'y(x)', eq_str)
        
        if "=" in eq_str:
            left, right = eq_str.split("=", 1)
        else:
            left, right = eq_str, "0"
        
        local_dict = {"x": x, "y": y, "Derivative": Derivative, "sec": sec, "tan": tan, "sin": sin, "cos": cos}
        
        left_expr = parse_expr(left, local_dict=local_dict, transformations=transformations)
        right_expr = parse_expr(right, local_dict=local_dict, transformations=transformations)
        
        eq = Eq(left_expr, right_expr)
        sol = dsolve(eq, y(x))
        
        st.success("Solution found:")
        st.latex(latex(sol))
        
        if "**2" in eq_input or "^2" in eq_input:
            st.info("Bernoulli equation detected. Method: Substitute v = 1/y to get linear ODE")
            
    except Exception as e:
        st.error("Couldn’t solve that. Check your syntax")
        with st.expander("See technical error"):
            st.code(str(e))
