import streamlit as st
from streamlit_ace import st_ace
import io
import sys
import google.generativeai as genai
import ast
from dotenv import load_dotenv
import os

load_dotenv()
gemini_api_key = os.getenv("API_KEY")


# Title of the Streamlit App
st.title("Python Code Runner")

code = st_ace(
        placeholder="Write your Python code here...",
        language="python",
        font_size=14,
        show_gutter=True,
        key="ace-editor",
        height=550,  # Adjust height as needed  
        auto_update=False  # Disable automatic updates
    )

genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

def is_python_code(code1):
    try:
        ast.parse(code1)
        return True  # Code is valid Python syntax
    except SyntaxError:
        return False  # Code is not valid Python syntax
    except Exception as e:
        # Handle any unexpected exceptions
        print(f"Unexpected error: {e}")
        return False
    
py_check = is_python_code(code)     

if st.button("Run Code"):
    if code:  # Check if there's code to run
        # Redirect stdout to capture print statements
        old_stdout = sys.stdout
        redirected_output = io.StringIO()
        sys.stdout = redirected_output
        
        try:
            # Execute the code in a controlled environment
            exec_globals = {}
            exec(code, exec_globals)

            # Capture the print statement outputs
            sys.stdout = old_stdout
            output = redirected_output.getvalue()
            
            # Display print statement outputs, if any
            if output:
                st.subheader("Output:")
                st.text(output)
            else:
                st.write("No output produced.")
                    
        except Exception as e:
            # Restore stdout in case of error and display the error
            sys.stdout = old_stdout
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter some code to run.")

# Button for AI Code Completion
if st.button("Complete Code Logic"):
        prompt = code + "Complete my code and give only python code without comments"
        response = model.generate_content(prompt)
        st.write(response.text)
    

# Button for AI Explaination
if st.button("AI Explaination"):
    if py_check:
        prompt = code + "Explain my code with comments, Improvements possible and a short overall description."
        response = model.generate_content(prompt)
        st.write(response.text)
    else:    
        st.warning("Please Check Your Code")

#Button for Optimization    
if st.button('Optimize Code'):
    if py_check:
        prompt = code + "Optimize my code with comments and give short description about optimization."
        response = model.generate_content(prompt)
        st.write(response.text)
    else:    
        st.warning("Please Check Your Code")    



    