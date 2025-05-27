from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

import openai
import os
from dotenv import load_dotenv

import requests
from bs4 import BeautifulSoup
from . import views

# .env 불러오기
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
load_dotenv(dotenv_path)
openai.api_key = os.getenv('OPENAI_API_KEY')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chatbot(request):
    message = request.data.get('message')
    role = "You are a chatbot that provides up-to-date financial data.Your users are young adults who are new to society and may not be familiar with basic financial concepts or the characteristics of financial products.You must explain your answers in a way that is easy for people in their twenties to early thirties to understand.All explanations should reflect the financial characteristics specific to South Korea.Your responses should be well-organized in clear sentences and paragraphs so that they are visually easy for users to read.Since your users are Korean, you must respond in Korean.Format your answers with appropriate line breaks for readability.Keep your responses concise — ideally under 100 characters — in a summarized style.Provide more detailed explanations only when the user explicitly asks for them."
    # GPT 호출하는 방법 
    gpt_answer = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            # 금융 전문가라는 역할 부여하기
             {
                "role": "system",
                 "content": role
            },
            # 사용자가 보낸 질문
            {
                "role": "user",
                "content": message
             }
        ]
    )

    # 응답을 Vue에 전달하는 코드
    answer = gpt_answer.choices[0].message['content']
    return Response({'response': answer}, status=status.HTTP_200_OK)