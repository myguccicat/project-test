from django.shortcuts import render, redirect
from django.http import HttpRequest

# Create your views here.

def index(request: HttpRequest):
    return render(request, 'app/index.html')


def streamlit_app_view(request: HttpRequest):
    keyword = request.GET.get('keyword', '')
    mode = request.GET.get('mode', 'ptt')  # 預設 ptt
    # 轉向嵌入 Streamlit 頁面 (你設定的嵌入URL，例如 /streamlit_app/)
    return render(request, 'app/streamlit_embed.html', {'keyword': keyword, 'mode': mode})