import os
from django.shortcuts import render
from django.http import JsonResponse
from google import genai  # Library mpya
from dotenv import load_dotenv

load_dotenv()

# Tengeneza Client mara moja nje ya function ili iweze kutumika tena
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

def chat_room(request):
    if request.method == "POST":
        user_message = request.POST.get('message')
        
        try:
            # Kutumia model ya gemini-2.5-flash kama tulivyoona kwenye list yako
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_message
            )
            
            # Kwenye SDK mpya, tunachukua text hivi:
            ai_reply = response.text
            
            return JsonResponse({"reply": ai_reply})
            
        except Exception as e:
            # Hii itakusaidia kuona kama kuna tatizo lolote jipya
            print(f"Error: {e}")
            return JsonResponse({"error": str(e)})
            
    return render(request, 'chat/index.html')
