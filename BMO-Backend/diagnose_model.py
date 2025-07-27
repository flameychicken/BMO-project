# diagnose_model.py
import os
import sys
from pathlib import Path

def check_model_files():
    """Check for model files in various locations"""
    print("=== MODEL FILE DIAGNOSTIC ===")
    
    # Check current directory structure
    print(f"Current directory: {os.getcwd()}")
    
    # List of potential model locations
    model_locations = [
        "models/",
        "./models/",
        "../models/",
        ".",
    ]
    
    model_files_found = []
    
    for location in model_locations:
        if os.path.exists(location):
            print(f"\nChecking {location}:")
            try:
                files = os.listdir(location)
                gguf_files = [f for f in files if f.endswith('.gguf')]
                
                if gguf_files:
                    print(f"  Found GGUF files:")
                    for f in gguf_files:
                        full_path = os.path.join(location, f)
                        size_gb = os.path.getsize(full_path) / (1024**3)
                        print(f"    - {f} ({size_gb:.2f} GB)")
                        model_files_found.append(full_path)
                else:
                    print(f"  No .gguf files found")
                    if files:
                        print(f"    Other files: {files[:5]}...")  # Show first 5 files
                    else:
                        print(f"    Directory is empty")
                        
            except PermissionError:
                print(f"  Permission denied accessing {location}")
        else:
            print(f"{location} does not exist")
    
    return model_files_found

def test_model_loading():
    """Test loading a model with llama-cpp-python"""
    print("\n=== MODEL LOADING TEST ===")
    
    model_files = check_model_files()
    
    if not model_files:
        print("No GGUF model files found!")
        print("\nTo fix this:")
        print("1. Download a model file (e.g., mistral-7b-v0.1.Q4_K_M.gguf)")
        print("2. Place it in the models/ directory")
        print("3. Make sure the file is completely downloaded (not partial)")
        return False
    
    # Try to import llama-cpp-python
    try:
        from llama_cpp import Llama
        print("llama-cpp-python imported successfully")
    except ImportError as e:
        print(f"Failed to import llama-cpp-python: {e}")
        print("Try: pip install llama-cpp-python")
        return False
    
    # Try to load the first model file found
    model_path = model_files[0]
    print(f"\nAttempting to load: {model_path}")
    
    try:
        # Very basic loading test
        llm = Llama(
            model_path=model_path,
            n_ctx=512,  # Small context for testing
            n_threads=2,  # Limited threads for testing
            verbose=True,
            n_batch=128,
        )
        print("Model loaded successfully!")
        
        # Try a simple inference
        print("Testing inference...")
        result = llm("Hello", max_tokens=5, temperature=0.1)
        response = result["choices"][0]["text"]
        print(f"Inference test successful: '{response.strip()}'")
        
        return True
        
    except Exception as e:
        print(f"Model loading failed: {e}")
        print("\nPossible issues:")
        print("- Model file is corrupted or incomplete")
        print("- Insufficient RAM (need ~8GB+ free)")
        print("- Model format not supported")
        return False

def check_system_resources():
    """Check system resources"""
    print("\n=== SYSTEM RESOURCES ===")
    
    try:
        import psutil
        memory = psutil.virtual_memory()
        print(f"Total RAM: {memory.total / (1024**3):.2f} GB")
        print(f"Available RAM: {memory.available / (1024**3):.2f} GB")
        print(f"CPU cores: {psutil.cpu_count()}")
        
        if memory.available < 6 * (1024**3):  # Less than 6GB
            print("Warning: You may not have enough RAM for a 7B model")
            print("   Consider using a smaller model (Q2_K or Q3_K)")
            
    except ImportError:
        print("psutil not available, install with: pip install psutil")

if __name__ == "__main__":
    print("Model Loading Diagnostic Tool")
    print("=" * 50)
    
    check_system_resources()
    model_files = check_model_files()
    
    if model_files:
        test_model_loading()
    else:
        print("\nNo model files found. Please download a model first.")
        
    print("\n" + "=" * 50)
    print("If you need help, share the output above!")
