import os
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Tafuta path kamili ya file la .env
env_path = os.path.join(settings.BASE_DIR, '.env')

# 2. Iambie load_dotenv isome kutokea kwenye hiyo path
load_dotenv(env_path)

# 3. Sasa itaweza kusoma key bila shida
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

def chat_room(request):
    # Tengeneza session kama haipo
    if 'chat_history' not in request.session:
        request.session['chat_history'] = []

    if request.method == "POST":
        user_message = request.POST.get('message')

        try:
            # Tengeneza format ya historia inayoendana na SDK mpya
            history = []
            for chat in request.session['chat_history']:
                history.append(types.Content(role="user", parts=[types.Part.from_text(text=chat['user'])]))
                history.append(types.Content(role="model", parts=[types.Part.from_text(text=chat['ai'])]))

            # MAREKEBISHO: history inawekwa moja kwa moja, sio kwenye config
            chat_session = client.chats.create(
                model='gemini-3-flash-preview',
                history=history
            )

            # Tuma meseji mpya
            response = chat_session.send_message(user_message)
            ai_reply = response.text

            # Hifadhi kwenye session
            updated_history = request.session['chat_history']
            updated_history.append({'user': user_message, 'ai': ai_reply})
            request.session['chat_history'] = updated_history[-10:] # Tunatunza 10 za mwisho
            request.session.modified = True

            return JsonResponse({"reply": ai_reply})

        except Exception as e:
            error_string = str(e)

            if "503" in error_string or "Service Unavailable" in error_string:
                ujumbe = "Mtandao wa AI umezidiwa kwa sasa (Service Unavailable). Tafadhali jaribu tena baada ya sekunde chache."
                return JsonResponse({"reply": ujumbe})

            # Angalia kama kosa ni la kufika kikomo (429)
            if "429" in error_string or "RESOURCE_EXHAUSTED" in error_string:
                ujumbe_wa_kikomo = "Samahani, umefika kikomo cha messages kwa sasa. Tafadhali jaribu tena baada ya muda mfupi au kesho."
                return JsonResponse({"reply": ujumbe_wa_kikomo})

            # Kama ni kosa lingine lolote, linaonyesha hapa kwenye terminal kwa ajili yako
            print(f"Chat Error: {error_string}")
            return JsonResponse({"error": "Kuna tatizo la kiufundi limetokea. Jaribu tena."})

    return render(request, 'chat/indexog.html')
