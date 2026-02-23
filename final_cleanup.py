import os
import shutil

def cleanup():
    # Option 1 files
    opt1_dir = r"g:\workAI\project_2nd_ai_agent_Anti\option_1_smart_media_archive"
    files_to_del = [
        "automated_test.py", "run_server.bat", "run_streamlit.bat", 
        "test_api.py", "test_fastapi.py", "server_log.txt", 
        "streamlit_log.txt", "benchmark_results.json", "done.txt"
    ]
    
    for f in files_to_del:
        path = os.path.join(opt1_dir, f)
        try:
            if os.path.exists(path):
                os.remove(path)
                print(f"Deleted: {path}")
        except Exception as e:
            print(f"Failed to delete {path}: {e}")

    # Root files
    root_dir = r"g:\workAI\project_2nd_ai_agent_Anti"
    root_files = [
        "final_benchmark.py", "test_opt1.json", "test_opt2.json", 
        "error.txt", "bench_test.txt", "test_output.txt", 
        "test_pwsh.txt", "test_final.txt"
    ]
    
    for f in root_files:
        path = os.path.join(root_dir, f)
        try:
            if os.path.exists(path):
                os.remove(path)
                print(f"Deleted: {path}")
        except Exception as e:
            print(f"Failed to delete {path}: {e}")

if __name__ == "__main__":
    cleanup()
