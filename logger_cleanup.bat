@echo off
set LOG=g:\workAI\project_2nd_ai_agent_Anti\cleanup_log.txt
echo Cleanup Start > %LOG%

taskkill /F /IM python.exe >> %LOG% 2>&1

set OPT1=g:\workAI\project_2nd_ai_agent_Anti\option_1_smart_media_archive
del /F /Q "%OPT1%\automated_test.py" >> %LOG% 2>&1
del /F /Q "%OPT1%\run_server.bat" >> %LOG% 2>&1
del /F /Q "%OPT1%\run_streamlit.bat" >> %LOG% 2>&1
del /F /Q "%OPT1%\test_api.py" >> %LOG% 2>&1
del /F /Q "%OPT1%\test_fastapi.py" >> %LOG% 2>&1
del /F /Q "%OPT1%\server_log.txt" >> %LOG% 2>&1
del /F /Q "%OPT1%\streamlit_log.txt" >> %LOG% 2>&1
del /F /Q "%OPT1%\benchmark_results.json" >> %LOG% 2>&1
del /F /Q "%OPT1%\done.txt" >> %LOG% 2>&1

set ROOT=g:\workAI\project_2nd_ai_agent_Anti
del /F /Q "%ROOT%\final_benchmark.py" >> %LOG% 2>&1
del /F /Q "%ROOT%\test_opt1.json" >> %LOG% 2>&1
del /F /Q "%ROOT%\test_opt2.json" >> %LOG% 2>&1
del /F /Q "%ROOT%\error.txt" >> %LOG% 2>&1
del /F /Q "%ROOT%\bench_test.txt" >> %LOG% 2>&1
del /F /Q "%ROOT%\test_output.txt" >> %LOG% 2>&1
del /F /Q "%ROOT%\test_pwsh.txt" >> %LOG% 2>&1
del /F /Q "%ROOT%\test_final.txt" >> %LOG% 2>&1

echo Cleanup End >> %LOG%
