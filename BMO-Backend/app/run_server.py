import uvicorn
import sys
import traceback

def main():
    try:
        print("Starting FastAPI server...")
        uvicorn.run(
            "simple_main:app",
            host="0.0.0.0",
            port=8000,
            reload=False,  # Disable reload for stability
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Server failed to start: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
