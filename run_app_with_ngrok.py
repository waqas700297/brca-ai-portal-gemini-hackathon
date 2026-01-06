import os
import subprocess
import time
import sys
from pyngrok import ngrok
from dotenv import load_dotenv

def run_app():
    # Load environment variables
    load_dotenv()
    
    auth_token = os.getenv("NGROK_AUTH_TOKEN")
    if not auth_token or auth_token == "your_ngrok_auth_token_here":
        print("Error: NGROK_AUTH_TOKEN not found or is set to default in .env file.")
        print("Please visit https://dashboard.ngrok.com/get-started/your-authtoken to get your token.")
        return

    # Set ngrok auth token
    ngrok.set_auth_token(auth_token)

    try:
        # 1. Start backend tunnel (port 8000)
        print("Starting backend tunnel on port 8000...")
        backend_tunnel = ngrok.connect(8000)
        backend_url = backend_tunnel.public_url
        print(f"Backend public URL: {backend_url}")

        # 2. Start frontend tunnel (port 5173 - default Vite port)
        print("Starting frontend tunnel on port 5173...")
        # Vite projects often need the 'host-header' to be set correctly for HMR or routing
        frontend_tunnel = ngrok.connect(5173)
        frontend_url = frontend_tunnel.public_url
        print(f"Frontend public URL: {frontend_url}")

        # Write URLs to a file for easy retrieval
        with open("ngrok_urls.txt", "w") as f:
            f.write(f"Frontend: {frontend_url}\n")
            f.write(f"Backend: {backend_url}\n")

        # 3. Start the FastAPI backend
        print("\nLaunching FastAPI backend...")
        backend_process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
            env=os.environ.copy()
        )

        # 4. Start the Vite frontend with environmental backend URL
        print("Launching Vite frontend...")
        frontend_env = os.environ.copy()
        frontend_env["VITE_API_BASE"] = backend_url
        
        # Navigate to frontend directory and run npm dev
        frontend_dir = os.path.join(os.getcwd(), "frontend")
        frontend_process = subprocess.Popen(
            ["npm", "run", "dev", "--", "--host"],
            cwd=frontend_dir,
            env=frontend_env,
            shell=True
        )

        print("-" * 50)
        print("APPLICATION IS RUNNING WITH NGROK")
        print(f"Access the app at: {frontend_url}")
        print(f"Backend API (for debugging): {backend_url}")
        print("-" * 50)
        print("Press Ctrl+C to stop all processes and tunnels.")

        # Keep the script running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")
            frontend_process.terminate()
            backend_process.terminate()
            ngrok.disconnect(backend_url)
            ngrok.disconnect(frontend_url)
            print("Processes and tunnels stopped.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_app()
