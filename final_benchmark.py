import requests
import json

def quick_test():
    try:
        # Option 1 Test
        res1 = requests.post("http://127.0.0.1:8000/ask", params={"query": "미디어 태깅 테스트"}, timeout=30)
        with open("test_opt1.json", "w", encoding="utf-8") as f:
            json.dump(res1.json(), f, ensure_ascii=False)
        
        # Option 2 Test
        res2 = requests.post("http://127.0.0.1:8001/ask", params={"query": "최신 AI 뉴스"}, timeout=30)
        with open("test_opt2.json", "w", encoding="utf-8") as f:
            json.dump(res2.json(), f, ensure_ascii=False)
    except Exception as e:
        with open("error.txt", "w") as f:
            f.write(str(e))

if __name__ == "__main__":
    quick_test()
