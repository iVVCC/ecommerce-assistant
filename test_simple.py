print("Testing basic Python functionality...")
print("Python version:")
import sys
print(sys.version)
print("\nTesting module imports...")
try:
    import fastapi
    print("fastapi imported successfully")
except Exception as e:
    print(f"Error importing fastapi: {e}")
try:
    import uvicorn
    print("uvicorn imported successfully")
except Exception as e:
    print(f"Error importing uvicorn: {e}")
try:
    import streamlit
    print("streamlit imported successfully")
except Exception as e:
    print(f"Error importing streamlit: {e}")
try:
    import openai
    print("openai imported successfully")
except Exception as e:
    print(f"Error importing openai: {e}")
print("\nTest completed!")
