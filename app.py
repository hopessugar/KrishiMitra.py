# -*- coding: utf-8 -*-
# app.py — KrishiMitra Streamlit UI (fixed & hardened)

import streamlit as st
import requests
import pandas as pd
from io import BytesIO

# --- Page Configuration ---
st.set_page_config(
    page_title="KrishiMitra - AI Farming Assistant",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Backend API URL ---
BACKEND_URL = "http://127.0.0.1:8000"

# --- Translations ---
# Notes:
# 1) Added the missing key "enter_city" in ALL languages so Tab 5 won't crash.
# 2) Keep keys consistent across languages.
# 3) Use tr("key") everywhere to avoid KeyErrors if a key is ever missing.
translations = {
    "en": {
        "header": "KrishiMitra",
        "subheader": "Your AI-powered assistant for smart farming decisions in India.",
        "bhashabuddy_header": "BhashaBuddy",
        "choose_language": "Choose Language:",
        "sidebar_info": "Select a language for a fully translated experience.",
        "tab_expert_diagnosis": "👩‍⚕️ Expert Diagnosis",
        "tab_mandi": "📈 Mandi Prices",
        "tab_health": "🌿 Crop Health",
        "tab_schemes": "📜 Govt. Schemes",
        "tab_recommendations": "🌍 Crop Recommendations",

        "expert_header": "🧠 Expert Diagnosis & Productivity Plan",
        "expert_desc": "Describe your crop's situation to get a detailed action plan from our AI agronomist.",

        "enter_crop": "1. Enter Your Crop:",
        "crop_stage": "2. Select Crop Stage:",
        "problem_desc": "3. Describe the Problem (e.g., 'yellow spots on lower leaves'):",
        "goal": "4. What is your primary goal?",

        "get_plan_button": "Generate Expert Plan",
        "ai_spinner": "🤖 KrishiNet AI is analyzing your situation...",
        "expert_plan_header": "Your Custom Action Plan:",
        "listen_plan": "Listen to this Plan",
        "audio_spinner": "Generating audio...",
        "audio_error": "Sorry, could not generate audio.",

        "chatbot_header": "💬 Quick Chat",
        "chat_input_placeholder": "Ask a quick question...",

        "mandi_header": "📈 Live Mandi Price Tracker",
        "mandi_desc": "Get the latest crop prices from government-verified markets (mandis).",
        "select_state": "Select State:",
        "select_commodity": "Select Commodity:",
        "get_prices_button": "Get Latest Prices & Trend",
        "prices_spinner": "Fetching prices...",
        "price_trend_header": "📊 Price Trend (Last 7 Days)",

        "health_header": "🌿 Crop Disease Detection",
        "health_desc": "Upload an image of a crop leaf to detect diseases.",
        "upload_image": "Choose an image...",
        "uploaded_image_caption": "Uploaded Leaf Image.",
        "detect_disease_button": "Detect Disease",
        "disease_spinner": "Analyzing image...",
        "detected_disease": "Detected Disease: {disease}",
        "confidence_score": "Confidence Score: {score:.2f}%",
        "organic_remedies": "Organic Remedies:",
        "chemical_solutions": "Chemical Solutions:",

        "schemes_header": "📜 Personalized Government Schemes",
        "schemes_desc": "Find out which government schemes you are eligible for.",
        "gender": "Gender:",
        "land_holding": "Land Holding (in acres):",
        "has_loan": "Have you taken a bank loan?",
        "find_schemes_button": "Find My Schemes",
        "schemes_spinner": "Finding eligible schemes...",
        "eligible_schemes_header": "Eligible Schemes For You:",
        "learn_more": "Learn More",
        "no_schemes_found": "No specific schemes found for your profile.",

        "recommendations_header": "🌍 Crop Recommendations",
        "recommendations_desc": "Get crop recommendations based on your location's Agro-Climatic Zone.",
        "get_recommendations_button": "Get Recommendations",
        "recommendations_spinner": "Finding recommendations...",
        "recommendations_for": "Recommendations for {city}:",
        "acz": "Agro-Climatic Zone:",
        "suitable_crops": "Suitable Crops:",
        "enter_city": "Enter City:"
    },
    "hi": {
        "header": "कृषि मित्र",
        "subheader": "भारत में स्मार्ट खेती के फैसलों के लिए आपका एआई-संचालित सहायक।",
        "bhashabuddy_header": "भाषाबडी",
        "choose_language": "भाषा चुनें:",
        "sidebar_info": "पूरी तरह से अनुवादित अनुभव के लिए एक भाषा चुनें।",
        "tab_expert_diagnosis": "👩‍⚕️ विशेषज्ञ निदान",
        "tab_mandi": "📈 मंडी कीमतें",
        "tab_health": "🌿 फसल स्वास्थ्य",
        "tab_schemes": "📜 सरकारी योजनाएं",
        "tab_recommendations": "🌍 फसल सिफारिशें",

        "expert_header": "🧠 विशेषज्ञ निदान और उत्पादकता योजना",
        "expert_desc": "हमारे एआई कृषि विज्ञानी से विस्तृत कार्य योजना प्राप्त करने के लिए अपनी फसल की स्थिति का वर्णन करें।",

        "enter_crop": "1. अपनी फसल दर्ज करें:",
        "crop_stage": "2. फसल की अवस्था चुनें:",
        "problem_desc": "3. समस्या का वर्णन करें (जैसे, 'निचली पत्तियों पर पीले धब्बे'):",
        "goal": "4. आपका प्राथमिक लक्ष्य क्या है?",

        "get_plan_button": "विशेषज्ञ योजना बनाएं",
        "ai_spinner": "🤖 कृषिनेत्र एआई आपकी स्थिति का विश्लेषण कर रहा है...",
        "expert_plan_header": "आपकी कस्टम कार्य योजना:",
        "listen_plan": "इस योजना को सुनें",
        "audio_spinner": "ऑडियो बना रहा है...",
        "audio_error": "क्षमा करें, ऑडियो नहीं बन सका।",

        "chatbot_header": "💬 त्वरित चैट",
        "chat_input_placeholder": "एक त्वरित प्रश्न पूछें...",

        "mandi_header": "📈 लाइव मंडी मूल्य ट्रैकर",
        "mandi_desc": "सरकार द्वारा सत्यापित बाजारों (मंडियों) से नवीनतम फसल की कीमतें प्राप्त करें।",
        "select_state": "राज्य चुनें:",
        "select_commodity": "वस्तु चुनें:",
        "get_prices_button": "नवीनतम मूल्य और ट्रेंड प्राप्त करें",
        "prices_spinner": "कीमतें लाई जा रही हैं...",
        "price_trend_header": "📊 मूल्य ट्रेंड (पिछले 7 दिन)",

        "health_header": "🌿 फसल रोग का पता लगाना",
        "health_desc": "रोगों का पता लगाने के लिए फसल के पत्ते की एक छवि अपलोड करें।",
        "upload_image": "एक छवि चुनें...",
        "uploaded_image_caption": "अपलोड की गई पत्ती की छवि।",
        "detect_disease_button": "रोग का पता लगाएं",
        "disease_spinner": "छवि का विश्लेषण किया जा रहा है...",
        "detected_disease": "पता चला रोग: {disease}",
        "confidence_score": "आत्मविश्वास स्कोर: {score:.2f}%",
        "organic_remedies": "जैविक उपचार:",
        "chemical_solutions": "रासायनिक समाधान:",

        "schemes_header": "📜 व्यक्तिगत सरकारी योजनाएं",
        "schemes_desc": "पता करें कि आप किन सरकारी योजनाओं के लिए पात्र हैं।",
        "gender": "लिंग:",
        "land_holding": "भूमि जोत (एकड़ में):",
        "has_loan": "क्या आपने बैंक ऋण लिया है?",
        "find_schemes_button": "मेरी योजनाएं खोजें",
        "schemes_spinner": "पात्र योजनाएं खोजी जा रही हैं...",
        "eligible_schemes_header": "आपके लिए पात्र योजनाएं:",
        "learn_more": "और जानें",
        "no_schemes_found": "आपकी प्रोफ़ाइल के लिए कोई विशिष्ट योजना नहीं मिली।",

        "recommendations_header": "🌍 फसल सिफारिशें",
        "recommendations_desc": "अपने स्थान के कृषि-जलवायु क्षेत्र के आधार पर फसल सिफारिशें प्राप्त करें।",
        "get_recommendations_button": "सिफारिशें प्राप्त करें",
        "recommendations_spinner": "सिफारिशें खोजी जा रही हैं...",
        "recommendations_for": "{city} के लिए सिफारिशें:",
        "acz": "कृषि-जलवायु क्षेत्र:",
        "suitable_crops": "उपयुक्त फसलें:",
        "enter_city": "शहर दर्ज करें:"
    },
    "mr": {
        "header": "कृषीमित्र",
        "subheader": "भारतातील स्मार्ट शेतीच्या निर्णयांसाठी तुमचा एआय-शक्ती असलेला सहाय्यक.",
        "bhashabuddy_header": "भाषाबडी",
        "choose_language": "भाषा निवडा:",
        "sidebar_info": "पूर्णपणे अनुवादित अनुभवासाठी एक भाषा निवडा.",
        "tab_expert_diagnosis": "👩‍⚕️ विशेषज्ञ निदान",
        "tab_mandi": "📈 मंडी भाव",
        "tab_health": "🌿 पीक आरोग्य",
        "tab_schemes": "📜 सरकारी योजना",
        "tab_recommendations": "🌍 पीक शिफारसी",

        "expert_header": "🧠 विशेषज्ञ निदान आणि उत्पादकता योजना",
        "expert_desc": "आमच्या एआय कृषीशास्त्रज्ञाकडून तपशीलवार कृती योजना मिळवण्यासाठी तुमच्या पिकाची परिस्थिती सांगा.",

        "enter_crop": "१. तुमचे पीक प्रविष्ट करा:",
        "crop_stage": "२. पिकाचा टप्पा निवडा:",
        "problem_desc": "३. समस्येचे वर्णन करा (उदा. 'खालच्या पानांवर पिवळे डाग'):",
        "goal": "४. तुमचे प्राथमिक ध्येय काय आहे?",

        "get_plan_button": "विशेषज्ञ योजना तयार करा",
        "ai_spinner": "🤖 कृषीनेट एआय तुमच्या परिस्थितीचे विश्लेषण करत आहे...",
        "expert_plan_header": "तुमची सानुकूल कृती योजना:",
        "listen_plan": "ही योजना ऐका",
        "audio_spinner": "ऑडिओ तयार होत आहे...",
        "audio_error": "क्षमस्व, ऑडिओ तयार करता आला नाही.",

        "chatbot_header": "💬 त्वरित गप्पा",
        "chat_input_placeholder": "एक त्वरित प्रश्न विचारा...",

        "mandi_header": "📈 थेट मंडी भाव ट्रॅकर",
        "mandi_desc": "सरकार-प्रमाणित बाजारांमधून (मंड्यांमधून) नवीनतम पीक भाव मिळवा.",
        "select_state": "राज्य निवडा:",
        "select_commodity": "वस्तू निवडा:",
        "get_prices_button": "नवीनतम भाव आणि ट्रेंड मिळवा",
        "prices_spinner": "भाव आणत आहे...",
        "price_trend_header": "📊 भाव ट्रेंड (गेले ७ दिवस)",

        "health_header": "🌿 पीक रोग ओळख",
        "health_desc": "रोग ओळखण्यासाठी पिकाच्या पानाचे चित्र अपलोड करा.",
        "upload_image": "एक चित्र निवडा...",
        "uploaded_image_caption": "अपलोड केलेले पानाचे चित्र.",
        "detect_disease_button": "रोग ओळखा",
        "disease_spinner": "चित्राचे विश्लेषण करत आहे...",
        "detected_disease": "ओळखलेला रोग: {disease}",
        "confidence_score": "आत्मविश्वास गुण: {score:.2f}%",
        "organic_remedies": "सेंद्रिय उपाय:",
        "chemical_solutions": "रासायनिक उपाय:",

        "schemes_header": "📜 वैयक्तिकृत सरकारी योजना",
        "schemes_desc": "तुम्ही कोणत्या सरकारी योजनांसाठी पात्र आहात ते शोधा.",
        "gender": "लिंग:",
        "land_holding": "जमीन धारणा (एकर मध्ये):",
        "has_loan": "तुम्ही बँक कर्ज घेतले आहे का?",
        "find_schemes_button": "माझ्या योजना शोधा",
        "schemes_spinner": "पात्र योजना शोधत आहे...",
        "eligible_schemes_header": "तुमच्यासाठी पात्र योजना:",
        "learn_more": "अधिक जाणून घ्या",
        "no_schemes_found": "तुमच्या प्रोफाइलसाठी कोणतीही विशिष्ट योजना आढळली नाही.",

        "recommendations_header": "🌍 पीक शिफारसी",
        "recommendations_desc": "तुमच्या स्थानाच्या कृषी-हवामान क्षेत्रावर आधारित पीक शिफारसी मिळवा.",
        "get_recommendations_button": "शिफारसी मिळवा",
        "recommendations_spinner": "शिफारसी शोधत आहे...",
        "recommendations_for": "{city} साठी शिफारसी:",
        "acz": "कृषी-हवामान क्षेत्र:",
        "suitable_crops": "योग्य पिके:",
        "enter_city": "शहर प्रविष्ट करा:"
    },
    "gu": {
        "header": "કૃષિમિત્ર",
        "subheader": "ભારતમાં સ્માર્ટ ખેતીના નિર્ણયો માટે તમારા એઆઈ-સંચાલિત સહાયક.",
        "bhashabuddy_header": "ભાષાબડી",
        "choose_language": "ભાષા પસંદ કરો:",
        "sidebar_info": "સંપૂર્ણ અનુવાદિત અનુભવ માટે ભાષા પસંદ કરો.",
        "tab_expert_diagnosis": "👩‍⚕️ નિષ્ણાત નિદાન",
        "tab_mandi": "📈 મંડીના ભાવ",
        "tab_health": "🌿 પાકનું આરોગ્ય",
        "tab_schemes": "📜 સરકારી યોજનાઓ",
        "tab_recommendations": "🌍 પાકની ભલામણો",

        "expert_header": "🧠 નિષ્ણાત નિદાન અને ઉત્પાદકતા યોજના",
        "expert_desc": "અમારા એઆઈ કૃષિવિજ્ઞાની પાસેથી વિગતવાર કાર્ય યોજના મેળવવા માટે તમારા પાકની પરિસ્થિતિનું વર્ણન કરો.",

        "enter_crop": "૧. તમારો પાક દાખલ કરો:",
        "crop_stage": "૨. પાકનો તબક્કો પસંદ કરો:",
        "problem_desc": "૩. સમસ્યાનું વર્ણન કરો (દા.ત., 'નીચલા પાંદડા પર પીળા ડાઘ'):",
        "goal": "૪. તમારું પ્રાથમિક લક્ષ્ય શું છે?",

        "get_plan_button": "નિષ્ણાત યોજના બનાવો",
        "ai_spinner": "🤖 કૃષિનેટ એઆઈ તમારી પરિસ્થિતિનું વિશ્લેષણ કરી રહ્યું છે...",
        "expert_plan_header": "તમારી કસ્ટમ કાર્ય યોજના:",
        "listen_plan": "આ યોજના સાંભળો",
        "audio_spinner": "ઓડિયો જનરેટ કરી રહ્યું છે...",
        "audio_error": "માફ કરશો, ઓડિયો જનરેટ કરી શકાયો નથી.",

        "chatbot_header": "💬 ઝડપી ચેટ",
        "chat_input_placeholder": "એક ઝડપી પ્રશ્ન પૂછો...",

        "mandi_header": "📈 લાઇવ મંડી ભાવ ટ્રેકર",
        "mandi_desc": "સરકાર દ્વારા ચકાસાયેલ બજારો (મંડીઓ) માંથી નવીનતમ પાકના ભાવ મેળવો.",
        "select_state": "રાજ્ય પસંદ કરો:",
        "select_commodity": "કોમોડિટી પસંદ કરો:",
        "get_prices_button": "નવીનતમ ભાવ અને ટ્રેન્ડ મેળવો",
        "prices_spinner": "ભાવો મેળવી રહ્યા છીએ...",
        "price_trend_header": "📊 ભાવ ટ્રેન્ડ (છેલ્લા 7 દિવસ)",

        "health_header": "🌿 પાક રોગ શોધ",
        "health_desc": "રોગો શોધવા માટે પાકના પાંદડાની છબી અપલોડ કરો.",
        "upload_image": "એક છબી પસંદ કરો...",
        "uploaded_image_caption": "અપલોડ કરેલી પાંદડાની છબી.",
        "detect_disease_button": "રોગ શોધો",
        "disease_spinner": "છબીનું વિશ્લેષણ કરી રહ્યું છે...",
        "detected_disease": "શોધાયેલ રોગ: {દisease}",
        "confidence_score": "આત્મવિશ્વાસ સ્કોર: {score:.2f}%",
        "organic_remedies": "ઓર્ગેનિક ઉપાયો:",
        "chemical_solutions": "રાસાયણિક ઉકેલો:",

        "schemes_header": "📜 વ્યક્તિગત સરકારી યોજનાઓ",
        "schemes_desc": "તમે કઈ સરકારી યોજનાઓ માટે પાત્ર છો તે શોધો.",
        "gender": "જાતિ:",
        "land_holding": "જમીન ધારણ (એકરમાં):",
        "has_loan": "શું તમે બેંક લોન લીધી છે?",
        "find_schemes_button": "મારી યોજનાઓ શોધો",
        "schemes_spinner": "પાત્ર યોજનાઓ શોધી રહ્યા છીએ...",
        "eligible_schemes_header": "તમારા માટે પાત્ર યોજનાઓ:",
        "learn_more": "વધુ શીખો",
        "no_schemes_found": "તમારી પ્રોફાઇલ માટે કોઈ વિશિષ્ટ યોજનાઓ મળી નથી.",

        "recommendations_header": "🌍 પાકની ભલામણો",
        "recommendations_desc": "તમારા સ્થાનના કૃષિ-આબોહવા ઝોનના આધારે પાકની ભલામણો મેળવો.",
        "get_recommendations_button": "ભલામણો મેળવો",
        "recommendations_spinner": "ભલામણો શોધી રહ્યા છીએ...",
        "recommendations_for": "{city} માટે ભલામણો:",
        "acz": "કૃષિ-આબોહવા ઝોન:",
        "suitable_crops": "યોગ્ય પાક:",
        "enter_city": "શહેર દાખલ કરો:"
    },
    "bn": {
        "header": "কৃষিমিত্র",
        "subheader": "ভারতে স্মার্ট কৃষি সিদ্ধান্তের জন্য আপনার এআই-চালিত সহকারী।",
        "bhashabuddy_header": "ভাষাসাথী",
        "choose_language": "ভাষা নির্বাচন করুন:",
        "sidebar_info": "একটি সম্পূর্ণ অনূদিত অভিজ্ঞতার জন্য একটি ভাষা নির্বাচন করুন।",
        "tab_expert_diagnosis": "👩‍⚕️ বিশেষজ্ঞ নির্ণয়",
        "tab_mandi": "📈 মন্ডি দর",
        "tab_health": "🌿 ফসল স্বাস্থ্য",
        "tab_schemes": "📜 সরকারি প্রকল্প",
        "tab_recommendations": "🌍 ফসল সুপারিশ",

        "expert_header": "🧠 বিশেষজ্ঞ নির্ণয় ও উৎপাদনশীলতা পরিকল্পনা",
        "expert_desc": "আমাদের এআই কৃষিবিদের কাছ থেকে একটি বিস্তারিত কর্ম পরিকল্পনা পেতে আপনার ফসলের পরিস্থিতি বর্ণনা করুন।",

        "enter_crop": "১. আপনার ফসল লিখুন:",
        "crop_stage": "২. ফসলের পর্যায় নির্বাচন করুন:",
        "problem_desc": "৩. সমস্যা বর্ণনা করুন (যেমন, 'নিচের পাতায় হলুদ দাগ'):",
        "goal": "৪. আপনার প্রাথমিক লক্ষ্য কি?",

        "get_plan_button": "বিশেষজ্ঞ পরিকল্পনা তৈরি করুন",
        "ai_spinner": "🤖 কৃষিনেট এআই আপনার পরিস্থিতি বিশ্লেষণ করছে...",
        "expert_plan_header": "আপনার কাস্টম কর্ম পরিকল্পনা:",
        "listen_plan": "এই পরিকল্পনাটি শুনুন",
        "audio_spinner": "অডিও তৈরি হচ্ছে...",
        "audio_error": "দুঃখিত, অডিও তৈরি করা যায়নি।",

        "chatbot_header": "💬 দ্রুত চ্যাট",
        "chat_input_placeholder": "একটি দ্রুত প্রশ্ন জিজ্ঞাসা করুন...",

        "mandi_header": "📈 লাইভ মন্ডি মূল্য ট্র্যাকার",
        "mandi_desc": "সরকার-যাচাইকৃত বাজার (মন্ডি) থেকে সর্বশেষ ফসলের দাম পান।",
        "select_state": "রাজ্য নির্বাচন করুন:",
        "select_commodity": "পণ্য নির্বাচন করুন:",
        "get_prices_button": "সর্বশেষ দাম ও ট্রেন্ড পান",
        "prices_spinner": "দাম আনা হচ্ছে...",
        "price_trend_header": "📊 মূল্য ট্রেন্ড (গত ৭ দিন)",

        "health_header": "🌿 ফসল রোগ সনাক্তকরণ",
        "health_desc": "রোগ সনাক্ত করতে ফসলের পাতার একটি ছবি আপলোড করুন।",
        "upload_image": "একটি ছবি বাছুন...",
        "uploaded_image_caption": "আপলোড করা পাতার ছবি।",
        "detect_disease_button": "রোগ সনাক্ত করুন",
        "disease_spinner": "ছবি বিশ্লেষণ করা হচ্ছে...",
        "detected_disease": "শনাক্ত করা রোগ: {disease}",
        "confidence_score": "আত্মবিশ্বাস স্কোর: {score:.2f}%",
        "organic_remedies": "জৈব প্রতিকার:",
        "chemical_solutions": "রাসায়নিক সমাধান:",

        "schemes_header": "📜 ব্যক্তিগতকৃত সরকারি প্রকল্প",
        "schemes_desc": "আপনি কোন সরকারি প্রকল্পের জন্য যোগ্য তা খুঁজে বের করুন।",
        "gender": "লিঙ্গ:",
        "land_holding": "জমির পরিমাণ (একরে):",
        "has_loan": "আপনি কি ব্যাংক ঋণ নিয়েছেন?",
        "find_schemes_button": "আমার প্রকল্পগুলি খুঁজুন",
        "schemes_spinner": "যোগ্য প্রকল্পগুলি খোঁজা হচ্ছে...",
        "eligible_schemes_header": "আপনার জন্য যোগ্য প্রকল্প:",
        "learn_more": "আরও জানুন",
        "no_schemes_found": "আপনার প্রোফাইলের জন্য কোনো নির্দিষ্ট প্রকল্প পাওয়া যায়নি।",

        "recommendations_header": "🌍 ফসল সুপারিশ",
        "recommendations_desc": "আপনার এলাকার কৃষি-জলবায়ু অঞ্চলের উপর ভিত্তি করে ফসলের সুপারিশ পান।",
        "get_recommendations_button": "সুপারিশ পান",
        "recommendations_spinner": "সুপারিশ খোঁজা হচ্ছে...",
        "recommendations_for": "{city}-এর জন্য সুপারিশ:",
        "acz": "কৃষি-জলবায়ু অঞ্চল:",
        "suitable_crops": "উপযুক্ত ফসল:",
        "enter_city": "শহর লিখুন:"
    },
    "ta": {
        "header": "கிருஷிமித்ரா",
        "subheader": "இந்தியாவில் ஸ்மார்ட் விவசாய முடிவுகளுக்கு உங்கள் AI-இயங்கும் உதவியாளர்.",
        "bhashabuddy_header": "பாஷாபட்டி",
        "choose_language": "மொழியைத் தேர்ந்தெடுக்கவும்:",
        "sidebar_info": "முழுமையாக மொழிபெயர்க்கப்பட்ட அனுபவத்திற்கு ஒரு மொழியைத் தேர்ந்தெடுக்கவும்.",
        "tab_expert_diagnosis": "👩‍⚕️ நிபுணர் கண்டறிதல்",
        "tab_mandi": "📈 மண்டி விலைகள்",
        "tab_health": "🌿 பயிர் ஆரோக்கியம்",
        "tab_schemes": "📜 அரசாங்க திட்டங்கள்",
        "tab_recommendations": "🌍 பயிர் பரிந்துரைகள்",

        "expert_header": "🧠 நிபுணர் கண்டறிதல் மற்றும் உற்பத்தித்திறன் திட்டம்",
        "expert_desc": "எங்கள் AI விவசாய விஞ்ஞானியிடமிருந்து விரிவான செயல் திட்டத்தைப் பெற உங்கள் பயிர் நிலையை விவரிக்கவும்.",

        "enter_crop": "1. உங்கள் பயிரை உள்ளிடவும்:",
        "crop_stage": "2. பயிர் நிலையைத் தேர்ந்தெடுக்கவும்:",
        "problem_desc": "3. சிக்கலை விவரிக்கவும் (எ.கா., 'கீழ் இலைகளில் மஞ்சள் புள்ளிகள்'):",
        "goal": "4. உங்கள் முதன்மை இலக்கு என்ன?",

        "get_plan_button": "நிபுணர் திட்டத்தை உருவாக்கவும்",
        "ai_spinner": "🤖 கிருஷிநெட் AI உங்கள் நிலையை பகுப்பாய்வு செய்கிறது...",
        "expert_plan_header": "உங்கள் தனிப்பயன் செயல் திட்டம்:",
        "listen_plan": "இந்தத் திட்டத்தைக் கேட்கவும்",
        "audio_spinner": "ஆடியோ உருவாக்கப்படுகிறது...",
        "audio_error": "மன்னிக்கவும், ஆடியோவை உருவாக்க முடியவில்லை.",

        "chatbot_header": "💬 விரைவான அரட்டை",
        "chat_input_placeholder": "ஒரு விரைவான கேள்வியைக் கேட்கவும்...",

        "mandi_header": "📈 நேரடி மண்டி விலை டிராக்கர்",
        "mandi_desc": "அரசாங்கத்தால் சரிபார்க்கப்பட்ட சந்தைகளிலிருந்து (மண்டிகள்) சமீபத்திய பயிர் விலைகளைப் பெறுங்கள்.",
        "select_state": "மாநிலத்தைத் தேர்ந்தெடுக்கவும்:",
        "select_commodity": "பொருளைத் தேர்ந்தெடுக்கவும்:",
        "get_prices_button": "சமீபத்திய விலைகள் மற்றும் போக்கைப் பெறுங்கள்",
        "prices_spinner": "விலைகளைப் பெறுகிறது...",
        "price_trend_header": "📊 விலை போக்கு (கடந்த 7 நாட்கள்)",

        "health_header": "🌿 பயிர் நோய் கண்டறிதல்",
        "health_desc": "நோய்களைக் கண்டறிய பயிர் இலையின் படத்தைப் பதிவேற்றவும்.",
        "upload_image": "ஒரு படத்தைத் தேர்ந்தெடுக்கவும்...",
        "uploaded_image_caption": "பதிவேற்றப்பட்ட இலை படம்.",
        "detect_disease_button": "நோயைக் கண்டறியவும்",
        "disease_spinner": "படத்தை பகுப்பாய்வு செய்கிறது...",
        "detected_disease": "கண்டறியப்பட்ட நோய்: {disease}",
        "confidence_score": "நம்பிக்கை மதிப்பெண்: {score:.2f}%",
        "organic_remedies": "இயற்கை வைத்தியம்:",
        "chemical_solutions": "இரசாயன தீர்வுகள்:",

        "schemes_header": "📜 தனிப்பயனாக்கப்பட்ட அரசாங்க திட்டங்கள்",
        "schemes_desc": "நீங்கள் எந்த அரசாங்க திட்டங்களுக்கு தகுதியானவர் என்பதைக் கண்டறியவும்.",
        "gender": "பாலினம்:",
        "land_holding": "நில உடைமை (ஏக்கரில்):",
        "has_loan": "நீங்கள் வங்கிக் கடன் வாங்கியுள்ளீர்களா?",
        "find_schemes_button": "எனது திட்டங்களைக் கண்டறியவும்",
        "schemes_spinner": "தகுதியான திட்டங்களைக் கண்டறிகிறது...",
        "eligible_schemes_header": "உங்களுக்கான தகுதியான திட்டங்கள்:",
        "learn_more": "மேலும் அறிக",
        "no_schemes_found": "உங்கள் சுயவிவரத்திற்கு குறிப்பிட்ட திட்டங்கள் எதுவும் இல்லை.",

        "recommendations_header": "🌍 பயிர் பரிந்துரைகள்",
        "recommendations_desc": "உங்கள் இருப்பிடத்தின் வேளாண்-காலநிலை மண்டலத்தின் அடிப்படையில் பயிர் பரிந்துரைகளைப் பெறுங்கள்.",
        "get_recommendations_button": "பரிந்துரைகளைப் பெறுங்கள்",
        "recommendations_spinner": "பரிந்துரைகளைக் கண்டறிகிறது...",
        "recommendations_for": "{city} க்கான பரிந்துரைகள்:",
        "acz": "வேளாண்-காலநிலை மண்டலம்:",
        "suitable_crops": "பொருத்தமான பயிர்கள்:",
        "enter_city": "நகரத்தை உள்ளிடவும்:"
    },
    "te": {
        "header": "కృషిమిత్ర",
        "subheader": "భారతదేశంలో స్మార్ట్ వ్యవసాయ నిర్ణయాల కోసం మీ AI-ఆధారిత సహాయకుడు.",
        "bhashabuddy_header": "భాషాబడ్డీ",
        "choose_language": "భాషను ఎంచుకోండి:",
        "sidebar_info": "పూర్తిగా అనువదించబడిన అనుభవం కోసం ఒక భాషను ఎంచుకోండి.",
        "tab_expert_diagnosis": "👩‍⚕️ నిపుణుల నిర్ధారణ",
        "tab_mandi": "📈 మండి ధరలు",
        "tab_health": "🌿 పంట ఆరోగ్యం",
        "tab_schemes": "📜 ప్రభుత్వ పథకాలు",
        "tab_recommendations": "🌍 పంట సిఫార్సులు",

        "expert_header": "🧠 నిపుణుల నిర్ధారణ మరియు ఉత్పాదకత ప్రణాళిక",
        "expert_desc": "మా AI వ్యవసాయ శాస్త్రవేత్త నుండి వివరణాత్మక కార్యాచరణ ప్రణాళికను పొందడానికి మీ పంట పరిస్థితిని వివరించండి.",

        "enter_crop": "1. మీ పంటను నమోదు చేయండి:",
        "crop_stage": "2. పంట దశను ఎంచుకోండి:",
        "problem_desc": "3. సమస్యను వివరించండి (ఉదా., 'దిగువ ఆకులపై పసుపు మచ్చలు'):",
        "goal": "4. మీ ప్రాథమిక లక్ష్యం ఏమిటి?",

        "get_plan_button": "నిపుణుల ప్రణాళికను రూపొందించండి",
        "ai_spinner": "🤖 కృషి నెట్ AI మీ పరిస్థితిని విశ్లేషిస్తోంది...",
        "expert_plan_header": "మీ కస్టమ్ కార్యాచరణ ప్రణాళిక:",
        "listen_plan": "ఈ ప్రణాళికను వినండి",
        "audio_spinner": "ఆడియో సృష్టించబడుతోంది...",
        "audio_error": "క్షమించండి, ఆడియోను సృష్టించడం సాధ్యం కాలేదు.",

        "chatbot_header": "💬 త్వరిత చాట్",
        "chat_input_placeholder": "ఒక శీఘ్ర ప్రశ్న అడగండి...",

        "mandi_header": "📈 లైవ్ మండి ధరల ట్రాకర్",
        "mandi_desc": "ప్రభుత్వ-ధృవీకరించబడిన మార్కెట్ల (మండిల) నుండి తాజా పంట ధరలను పొందండి.",
        "select_state": "రాష్ట్రాన్ని ఎంచుకోండి:",
        "select_commodity": "వస్తువును ఎంచుకోండి:",
        "get_prices_button": "తాజా ధరలు & ట్రెండ్ పొందండి",
        "prices_spinner": "ధరలను పొందుతోంది...",
        "price_trend_header": "📊 ధరల ట్రెండ్ (గత 7 రోజులు)",

        "health_header": "🌿 పంట వ్యాధి నిర్ధారణ",
        "health_desc": "వ్యాధులను గుర్తించడానికి పంట ఆకు యొక్క చిత్రాన్ని అప్‌లోడ్ చేయండి.",
        "upload_image": "ఒక చిత్రాన్ని ఎంచుకోండి...",
        "uploaded_image_caption": "అప్‌లోడ్ చేయబడిన ఆకు చిత్రం.",
        "detect_disease_button": "వ్యాధిని గుర్తించండి",
        "disease_spinner": "చిత్రాన్ని విశ్లేషిస్తోంది...",
        "detected_disease": "గుర్తించబడిన వ్యాధి: {disease}",
        "confidence_score": "విశ్వాస స్కోరు: {score:.2f}%",
        "organic_remedies": "సేంద్రీయ నివారణలు:",
        "chemical_solutions": "రసాయన పరిష్కారాలు:",

        "schemes_header": "📜 వ్యక్తిగతీకరించిన ప్రభుత్వ పథకాలు",
        "schemes_desc": "మీరు ఏ ప్రభుత్వ పథకాలకు అర్హులో కనుగొనండి.",
        "gender": "లింగం:",
        "land_holding": "భూమి హోల్డింగ్ (ఎకరాలలో):",
        "has_loan": "మీరు బ్యాంకు రుణం తీసుకున్నారా?",
        "find_schemes_button": "నా పథకాలను కనుగొనండి",
        "schemes_spinner": "అర్హత ఉన్న పథకాలను కనుగొంటోంది...",
        "eligible_schemes_header": "మీ కోసం అర్హత ఉన్న పథకాలు:",
        "learn_more": "మరింత తెలుసుకోండి",
        "no_schemes_found": "మీ ప్రొఫైల్ కోసం నిర్దిష్ట పథకాలు ఏవీ కనుగొనబడలేదు.",

        "recommendations_header": "🌍 పంట సిఫార్సులు",
        "recommendations_desc": "మీ ప్రాంతం యొక్క వ్యవసాయ-వాతావరణ మండలం ఆధారంగా పంట సిఫార్సులను పొందండి.",
        "get_recommendations_button": "సిఫార్సులను పొందండి",
        "recommendations_spinner": "సిఫార్సులను కనుగొంటోంది...",
        "recommendations_for": "{city} కోసం సిఫార్సులు:",
        "acz": "వ్యవసాయ-వాతావరణ మండలం:",
        "suitable_crops": "అనువైన పంటలు:",
        "enter_city": "నగరం నమోదు చేయండి:"
    },
    "kn": {
        "header": "ಕೃಷಿಮಿತ್ರ",
        "subheader": "ಭಾರತದಲ್ಲಿ ಸ್ಮಾರ್ಟ್ ಕೃಷಿ ನಿರ್ಧಾರಗಳಿಗಾಗಿ ನಿಮ್ಮ AI-ಚಾಲಿತ ಸಹಾಯಕ.",
        "bhashabuddy_header": "ಭಾಷಾಬಡ್ಡಿ",
        "choose_language": "ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ:",
        "sidebar_info": "ಸಂಪೂರ್ಣ ಅನುವಾದಿತ ಅನುಭವಕ್ಕಾಗಿ ಒಂದು ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ.",
        "tab_expert_diagnosis": "👩‍⚕️ ತಜ್ಞರ ರೋಗನಿರ್ಣಯ",
        "tab_mandi": "📈 ಮಂಡಿ ಬೆಲೆಗಳು",
        "tab_health": "🌿 ಬೆಳೆ ಆರೋಗ್ಯ",
        "tab_schemes": "📜 ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು",
        "tab_recommendations": "🌍 ಬೆಳೆ ಶಿಫಾರಸುಗಳು",

        "expert_header": "🧠 ತಜ್ಞರ ರೋಗನಿರ್ಣಯ ಮತ್ತು ಉತ್ಪಾದಕತೆ ಯೋಜನೆ",
        "expert_desc": "ನಮ್ಮ AI ಕೃಷಿ ವಿಜ್ಞಾನಿಯಿಂದ ವಿವರವಾದ ಕ್ರಿಯಾ ಯೋಜನೆಯನ್ನು ಪಡೆಯಲು ನಿಮ್ಮ ಬೆಳೆ ಪರಿಸ್ಥಿತಿಯನ್ನು ವಿವರಿಸಿ.",

        "enter_crop": "1. ನಿಮ್ಮ ಬೆಳೆಯನ್ನು ನಮೂದಿಸಿ:",
        "crop_stage": "2. ಬೆಳೆ ಹಂತವನ್ನು ಆಯ್ಕೆಮಾಡಿ:",
        "problem_desc": "3. ಸಮಸ್ಯೆಯನ್ನು ವಿವರಿಸಿ (ಉದಾ., 'ಕೆಳಗಿನ ಎಲೆಗಳ ಮೇಲೆ ಹಳದಿ ಚುಕ್ಕೆಗಳು'):",
        "goal": "4. ನಿಮ್ಮ ಪ್ರಾಥಮಿಕ ಗುರಿ ಏನು?",

        "get_plan_button": "ತಜ್ಞರ ಯೋಜನೆಯನ್ನು ರಚಿಸಿ",
        "ai_spinner": "🤖 ಕೃಷಿನೆಟ್ AI ನಿಮ್ಮ ಪರಿಸ್ಥಿತಿಯನ್ನು ವಿಶ್ಲೇಷಿಸುತ್ತಿದೆ...",
        "expert_plan_header": "ನಿಮ್ಮ ಕಸ್ಟಮ್ ಕ್ರಿಯಾ ಯೋಜನೆ:",
        "listen_plan": "ಈ ಯೋಜನೆಯನ್ನು ಕೇಳಿ",
        "audio_spinner": "ಆಡಿಯೋ ರಚಿಸಲಾಗುತ್ತಿದೆ...",
        "audio_error": "ಕ್ಷಮಿಸಿ, ಆಡಿಯೋ ರಚಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ.",

        "chatbot_header": "💬 ತ್ವರಿತ ಚಾಟ್",
        "chat_input_placeholder": "ಒಂದು ತ್ವರಿತ ಪ್ರಶ್ನೆ ಕೇಳಿ...",

        "mandi_header": "📈 ಲೈವ್ ಮಂಡಿ ಬೆಲೆ ಟ್ರ್ಯಾಕರ್",
        "mandi_desc": "ಸರ್ಕಾರ-ಪರಿಶೀಲಿಸಿದ ಮಾರುಕಟ್ಟೆಗಳಿಂದ (ಮಂಡಿಗಳಿಂದ) ಇತ್ತೀಚಿನ ಬೆಳೆ ಬೆಲೆಗಳನ್ನು ಪಡೆಯಿರಿ.",
        "select_state": "ರಾಜ್ಯವನ್ನು ಆಯ್ಕೆಮಾಡಿ:",
        "select_commodity": "ಸರಕು ಆಯ್ಕೆಮಾಡಿ:",
        "get_prices_button": "ಇತ್ತೀಚಿನ ಬೆಲೆಗಳು ಮತ್ತು ಟ್ರೆಂಡ್ ಪಡೆಯಿರಿ",
        "prices_spinner": "ಬೆಲೆಗಳನ್ನು ತರಲಾಗುತ್ತಿದೆ...",
        "price_trend_header": "📊 ಬೆಲೆ ಟ್ರೆಂಡ್ (ಕಳೆದ 7 ದಿನಗಳು)",

        "health_header": "🌿 ಬೆಳೆ ರೋಗ ಪತ್ತೆ",
        "health_desc": "ರೋಗಗಳನ್ನು ಪತ್ತೆಹಚ್ಚಲು ಬೆಳೆ ಎಲೆಯ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.",
        "upload_image": "ಒಂದು ಚಿತ್ರವನ್ನು ಆಯ್ಕೆಮಾಡಿ...",
        "uploaded_image_caption": "ಅಪ್‌ಲೋಡ್ ಮಾಡಿದ ಎಲೆ ಚಿತ್ರ.",
        "detect_disease_button": "ರೋಗವನ್ನು ಪತ್ತೆ ಮಾಡಿ",
        "disease_spinner": "ಚಿತ್ರವನ್ನು ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ...",
        "detected_disease": "ಪತ್ತೆಯಾದ ರೋಗ: {disease}",
        "confidence_score": "ವಿಶ್ವಾಸಾರ್ಹತೆಯ ಅಂಕ: {score:.2f}%",
        "organic_remedies": "ಸಾವಯವ ಪರಿಹಾರಗಳು:",
        "chemical_solutions": "ರಾಸಾಯನಿಕ ಪರಿಹಾರಗಳು:",

        "schemes_header": "📜 ವೈಯಕ್ತಿಕಗೊಳಿಸಿದ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು",
        "schemes_desc": "ನೀವು ಯಾವ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳಿಗೆ ಅರ್ಹರಾಗಿದ್ದೀರಿ ಎಂಬುದನ್ನು ಕಂಡುಹಿಡಿಯಿರಿ.",
        "gender": "ಲಿಂಗ:",
        "land_holding": "ಭೂ ಹಿಡುವಳಿ (ಎಕರೆಗಳಲ್ಲಿ):",
        "has_loan": "ನೀವು ಬ್ಯಾಂಕ್ ಸಾಲ ತೆಗೆದುಕೊಂಡಿದ್ದೀರಾ?",
        "find_schemes_button": "ನನ್ನ ಯೋಜನೆಗಳನ್ನು ಹುಡುಕಿ",
        "schemes_spinner": "ಅರ್ಹ ಯೋಜನೆಗಳನ್ನು ಹುಡುಕಲಾಗುತ್ತಿದೆ...",
        "eligible_schemes_header": "ನಿಮಗಾಗಿ ಅರ್ಹ ಯೋಜನೆಗಳು:",
        "learn_more": "ಇನ್ನಷ್ಟು ತಿಳಿಯಿರಿ",
        "no_schemes_found": "ನಿಮ್ಮ ಪ್ರೊಫೈಲ್‌ಗೆ ಯಾವುದೇ ನಿರ್ದಿಷ್ಟ ಯೋಜನೆಗಳು ಕಂಡುಬಂದಿಲ್ಲ.",

        "recommendations_header": "🌍 ಬೆಳೆ ಶಿಫಾರಸುಗಳು",
        "recommendations_desc": "ನಿಮ್ಮ ಸ್ಥಳದ ಕೃಷಿ-ಹವಾಮಾನ ವಲಯದ ಆಧಾರದ ಮೇಲೆ ಬೆಳೆ ಶಿಫಾರಸುಗಳನ್ನು ಪಡೆಯಿರಿ.",
        "get_recommendations_button": "ಶಿಫಾರಸುಗಳನ್ನು ಪಡೆಯಿರಿ",
        "recommendations_spinner": "ಶಿಫಾರಸುಗಳನ್ನು ಹುಡುಕಲಾಗುತ್ತಿದೆ...",
        "recommendations_for": "{city} ಗಾಗಿ ಶಿಫಾರಸುಗಳು:",
        "acz": "ಕೃಷಿ-ಹವಾಮಾನ ವಲಯ:",
        "suitable_crops": "ಸೂಕ್ತ ಬೆಳೆಗಳು:",
        "enter_city": "ನಗರವನ್ನು ನಮೂದಿಸಿ:"
    },
    "pa": {
        "header": "ਕ੍ਰਿਸ਼ੀਮਿੱਤਰ",
        "subheader": "ਭਾਰਤ ਵਿੱਚ ਸਮਾਰਟ ਖੇਤੀ ਦੇ ਫੈਸਲਿਆਂ ਲਈ ਤੁਹਾਡਾ AI-ਸੰਚਾਲਿਤ ਸਹਾਇਕ।",
        "bhashabuddy_header": "ਭਾਸ਼ਾਬੱਡੀ",
        "choose_language": "ਭਾਸ਼ਾ ਚੁਣੋ:",
        "sidebar_info": "ਪੂਰੀ ਤਰ੍ਹਾਂ ਅਨੁਵਾਦ ਕੀਤੇ ਅਨੁਭਵ ਲਈ ਇੱਕ ਭਾਸ਼ਾ ਚੁਣੋ।",
        "tab_expert_diagnosis": "👩‍⚕️ ਮਾਹਰ ਨਿਦਾਨ",
        "tab_mandi": "📈 ਮੰਡੀ ਦੀਆਂ ਕੀਮਤਾਂ",
        "tab_health": "🌿 ਫਸਲ ਦੀ ਸਿਹਤ",
        "tab_schemes": "📜 ਸਰਕਾਰੀ ਯੋਜਨਾਵਾਂ",
        "tab_recommendations": "🌍 ਫਸਲ ਦੀਆਂ ਸਿਫਾਰਸ਼ਾਂ",

        "expert_header": "🧠 ਮਾਹਰ ਨਿਦਾਨ ਅਤੇ ਉਤਪਾਦਕਤਾ ਯੋਜਨਾ",
        "expert_desc": "ਸਾਡੇ AI ਖੇਤੀ ਵਿਗਿਆਨੀ ਤੋਂ ਵਿਸਤ੍ਰਿਤ ਕਾਰਜ ਯੋਜਨਾ ਪ੍ਰਾਪਤ ਕਰਨ ਲਈ ਆਪਣੀ ਫਸਲ ਦੀ ਸਥਿਤੀ ਦਾ ਵਰਣਨ ਕਰੋ।",

        "enter_crop": "1. ਆਪਣੀ ਫਸਲ ਦਾਖਲ ਕਰੋ:",
        "crop_stage": "2. ਫਸਲ ਦਾ ਪੜਾਅ ਚੁਣੋ:",
        "problem_desc": "3. ਸਮੱਸਿਆ ਦਾ ਵਰਣਨ ਕਰੋ (ਜਿਵੇਂ, 'ਹੇਠਲੇ ਪੱਤਿਆਂ 'ਤੇ ਪੀਲੇ ਧੱਬੇ'):",
        "goal": "4. ਤੁਹਾਡਾ ਮੁੱਖ ਟੀਚਾ ਕੀ ਹੈ?",

        "get_plan_button": "ਮਾਹਰ ਯੋਜਨਾ ਬਣਾਓ",
        "ai_spinner": "🤖 ਕ੍ਰਿਸ਼ੀਨੈੱਟ AI ਤੁਹਾਡੀ ਸਥਿਤੀ ਦਾ ਵਿਸ਼ਲੇਸ਼ਣ ਕਰ ਰਿਹਾ ਹੈ...",
        "expert_plan_header": "ਤੁਹਾਡੀ ਕਸਟਮ ਕਾਰਜ ਯੋਜਨਾ:",
        "listen_plan": "ਇਸ ਯੋਜਨਾ ਨੂੰ ਸੁਣੋ",
        "audio_spinner": "ਆਡੀਓ ਬਣਾਇਆ ਜਾ ਰਿਹਾ ਹੈ...",
        "audio_error": "ਮਾਫ ਕਰਨਾ, ਆਡੀਓ ਨਹੀਂ ਬਣਾਇਆ ਜਾ ਸਕਿਆ।",

        "chatbot_header": "💬 ਤੁਰੰਤ ਗੱਲਬਾਤ",
        "chat_input_placeholder": "ਇੱਕ ਤੁਰੰਤ ਸਵਾਲ ਪੁੱਛੋ...",

        "mandi_header": "📈 ਲਾਈਵ ਮੰਡੀ ਕੀਮਤ ਟਰੈਕਰ",
        "mandi_desc": "ਸਰਕਾਰ ਦੁਆਰਾ ਪ੍ਰਮਾਣਿਤ ਬਾਜ਼ਾਰਾਂ (ਮੰਡੀਆਂ) ਤੋਂ ਨਵੀਨਤਮ ਫਸਲਾਂ ਦੀਆਂ ਕੀਮਤਾਂ ਪ੍ਰਾਪਤ ਕਰੋ।",
        "select_state": "ਰਾਜ ਚੁਣੋ:",
        "select_commodity": "ਵਸਤੂ ਚੁਣੋ:",
        "get_prices_button": "ਨਵੀਨਤਮ ਕੀਮਤਾਂ ਅਤੇ ਰੁਝਾਨ ਪ੍ਰਾਪਤ ਕਰੋ",
        "prices_spinner": "ਕੀਮਤਾਂ ਪ੍ਰਾਪਤ ਕੀਤੀਆਂ ਜਾ ਰਹੀਆਂ ਹਨ...",
        "price_trend_header": "📊 ਕੀਮਤ ਰੁਝਾਨ (ਪਿਛਲੇ 7 ਦਿਨ)",

        "health_header": "🌿 ਫਸਲ ਰੋਗ ਦੀ ਪਛਾਣ",
        "health_desc": "ਰੋਗਾਂ ਦੀ ਪਛਾਣ ਕਰਨ ਲਈ ਫਸਲ ਦੇ ਪੱਤੇ ਦੀ ਤਸਵੀਰ ਅਪਲੋਡ ਕਰੋ।",
        "upload_image": "ਇੱਕ ਤਸਵੀਰ ਚੁਣੋ...",
        "uploaded_image_caption": "ਅਪਲੋਡ ਕੀਤੀ ਪੱਤੇ ਦੀ ਤਸਵੀਰ।",
        "detect_disease_button": "ਰੋਗ ਦੀ ਪਛਾਣ ਕਰੋ",
        "disease_spinner": "ਤਸਵੀਰ ਦਾ ਵਿਸ਼ਲੇਸ਼ਣ ਕੀਤਾ ਜਾ ਰਿਹਾ ਹੈ...",
        "detected_disease": "ਪਛਾਣਿਆ ਗਿਆ ਰੋਗ: {disease}",
        "confidence_score": "ਵਿਸ਼ਵਾਸ ਸਕੋਰ: {score:.2f}%",
        "organic_remedies": "ਜੈਵਿਕ ਉਪਚਾਰ:",
        "chemical_solutions": "ਰਸਾਇਣਕ ਹੱਲ:",

        "schemes_header": "📜 ਵਿਅਕਤੀਗਤ ਸਰਕਾਰੀ ਯੋਜਨਾਵਾਂ",
        "schemes_desc": "ਪਤਾ ਕਰੋ ਕਿ ਤੁਸੀਂ ਕਿਹੜੀਆਂ ਸਰਕਾਰੀ ਯੋਜਨਾਵਾਂ ਲਈ ਯੋਗ ਹੋ।",
        "gender": "ਲਿੰਗ:",
        "land_holding": "ਜ਼ਮੀਨ ਦੀ ਮਾਲਕੀ (ਏਕੜ ਵਿੱਚ):",
        "has_loan": "ਕੀ ਤੁਸੀਂ ਬੈਂਕ ਤੋਂ ਕਰਜ਼ਾ ਲਿਆ ਹੈ?",
        "find_schemes_button": "ਮੇਰੀਆਂ ਯੋਜਨਾਵਾਂ ਲੱਭੋ",
        "schemes_spinner": "ਯੋਗ ਯੋਜਨਾਵਾਂ ਲੱਭੀਆਂ ਜਾ ਰਹੀਆਂ ਹਨ...",
        "eligible_schemes_header": "ਤੁਹਾਡੇ ਲਈ ਯੋਗ ਯੋਜਨਾਵਾਂ:",
        "learn_more": "ਹੋਰ ਜਾਣੋ",
        "no_schemes_found": "ਤੁਹਾਡੇ ਪ੍ਰੋਫਾਈਲ ਲਈ ਕੋਈ ਖਾਸ ਯੋਜਨਾਵਾਂ ਨਹੀਂ ਮਿਲੀਆਂ।",

        "recommendations_header": "🌍 ਫਸਲ ਦੀਆਂ ਸਿਫਾਰਸ਼ਾਂ",
        "recommendations_desc": "ਆਪਣੇ ਸਥਾਨ ਦੇ ਖੇਤੀ-ਜਲਵਾਯੂ ਜ਼ੋਨ ਦੇ ਅਧਾਰ 'ਤੇ ਫਸਲ ਦੀਆਂ ਸਿਫਾਰਸ਼ਾਂ ਪ੍ਰਾਪਤ ਕਰੋ।",
        "get_recommendations_button": "ਸਿਫਾਰਸ਼ਾਂ ਪ੍ਰਾਪਤ ਕਰੋ",
        "recommendations_spinner": "ਸਿਫਾਰਸ਼ਾਂ ਲੱਭੀਆਂ ਜਾ ਰਹੀਆਂ ਹਨ...",
        "recommendations_for": "{city} ਲਈ ਸਿਫਾਰਸ਼ਾਂ:",
        "acz": "ਖੇਤੀ-ਜਲਵਾਯੂ ਜ਼ੋਨ:",
        "suitable_crops": "ਉਚਿਤ ਫਸਲਾਂ:",
        "enter_city": "ਸ਼ਹਿਰ ਦਾਖਲ ਕਰੋ:"
    },
    "ml": {
        "header": "കൃഷിമിത്ര",
        "subheader": "ഇന്ത്യയിലെ സ്മാർട്ട് കാർഷിക തീരുമാനങ്ങൾക്കായി നിങ്ങളുടെ AI-പവർഡ് അസിസ്റ്റന്റ്.",
        "bhashabuddy_header": "ഭാഷാബഡ്ഡി",
        "choose_language": "ഭാഷ തിരഞ്ഞെടുക്കുക:",
        "sidebar_info": "പൂർണ്ണമായി വിവർത്തനം ചെയ്ത അനുഭവത്തിനായി ഒരു ഭാഷ തിരഞ്ഞെടുക്കുക.",
        "tab_expert_diagnosis": "👩‍⚕️ വിദഗ്ദ്ധ രോഗനിർണയം",
        "tab_mandi": "📈 മണ്ഡി വിലകൾ",
        "tab_health": "🌿 വിള ആരോഗ്യം",
        "tab_schemes": "📜 സർക്കാർ പദ്ധതികൾ",
        "tab_recommendations": "🌍 വിള ശുപാർശകൾ",

        "expert_header": "🧠 വിദഗ്ദ്ധ രോഗനിർണയവും ഉത്പാദനക്ഷമത പദ്ധതിയും",
        "expert_desc": "ഞങ്ങളുടെ AI അഗ്രോണമിസ്റ്റിൽ നിന്ന് വിശദമായ പ്രവർത്തന പദ്ധതി ലഭിക്കുന്നതിന് നിങ്ങളുടെ വിളയുടെ സാഹചര്യം വിവരിക്കുക.",

        "enter_crop": "1. നിങ്ങളുടെ വിള നൽകുക:",
        "crop_stage": "2. വിളയുടെ ഘട്ടം തിരഞ്ഞെടുക്കുക:",
        "problem_desc": "3. പ്രശ്നം വിവരിക്കുക (ഉദാ., 'താഴത്തെ ഇലകളിൽ മഞ്ഞ പാടുകൾ'):",
        "goal": "4. നിങ്ങളുടെ പ്രാഥമിക ലക്ഷ്യം എന്താണ്?",

        "get_plan_button": "വിദഗ്ദ്ധ പദ്ധതി തയ്യാറാക്കുക",
        "ai_spinner": "🤖 കൃഷിനെറ്റ് AI നിങ്ങളുടെ സാഹചര്യം വിശകലനം ചെയ്യുന്നു...",
        "expert_plan_header": "നിങ്ങളുടെ കസ്റ്റം പ്രവർത്തന പദ്ധതി:",
        "listen_plan": "ഈ പദ്ധതി കേൾക്കുക",
        "audio_spinner": "ഓഡിയോ നിർമ്മിക്കുന്നു...",
        "audio_error": "ക്ഷമിക്കണം, ഓഡിയോ നിർമ്മിക്കാൻ കഴിഞ്ഞില്ല.",

        "chatбот_header": "💬 പെട്ടെന്നുള്ള ചാറ്റ്",
        "chat_input_placeholder": "ഒരു പെട്ടെന്നുള്ള ചോദ്യം ചോദിക്കുക...",

        "mandi_header": "📈 ലൈവ് മണ്ഡി വില ട്രാക്കർ",
        "mandi_desc": "സർക്കാർ-പരിശോധിച്ച മാർക്കറ്റുകളിൽ (മണ്ഡികളിൽ) നിന്ന് ഏറ്റവും പുതിയ വിള വിലകൾ നേടുക.",
        "select_state": "സംസ്ഥാനം തിരഞ്ഞെടുക്കുക:",
        "select_commodity": "ചരക്ക് തിരഞ്ഞെടുക്കുക:",
        "get_prices_button": "ഏറ്റവും പുതിയ വിലകളും ട്രെൻഡും നേടുക",
        "prices_spinner": "വിലകൾ നേടുന്നു...",
        "price_trend_header": "📊 വില ട്രെൻഡ് (കഴിഞ്ഞ 7 ദിവസം)",

        "health_header": "🌿 വിള രോഗ നിർണ്ണയം",
        "health_desc": "രോഗങ്ങൾ നിർണ്ണയിക്കാൻ വിളയുടെ ഇലയുടെ ഒരു ചിത്രം അപ്‌ലോഡ് ചെയ്യുക.",
        "upload_image": "ഒരു ചിത്രം തിരഞ്ഞെടുക്കുക...",
        "uploaded_image_caption": "അപ്‌ലോഡ് ചെയ്ത ഇല ചിത്രം.",
        "detect_disease_button": "രോഗം നിർണ്ണയിക്കുക",
        "disease_spinner": "ചിത്രം വിശകലനം ചെയ്യുന്നു...",
        "detected_disease": "കണ്ടെത്തിയ രോഗം: {disease}",
        "confidence_score": "ആത്മവിശ്വാസ സ്കോർ: {score:.2f}%",
        "organic_remedies": "ജൈവ പ്രതിവിധികൾ:",
        "chemical_solutions": "രാസപരമായ പരിഹാരങ്ങൾ:",

        "schemes_header": "📜 വ്യക്തിഗതമാക്കിയ സർക്കാർ പദ്ധതികൾ",
        "schemes_desc": "ഏത് സർക്കാർ പദ്ധതികൾക്കാണ് നിങ്ങൾ യോഗ്യരെന്ന് കണ്ടെത്തുക.",
        "gender": "ലിംഗഭേദം:",
        "land_holding": "ഭൂമി കൈവശം (ഏക്കറിൽ):",
        "has_loan": "നിങ്ങൾ ബാങ്ക് വായ്പ എടുത്തിട്ടുണ്ടോ?",
        "find_schemes_button": "എന്റെ പദ്ധതികൾ കണ്ടെത്തുക",
        "schemes_spinner": "യോഗ്യമായ പദ്ധതികൾ കണ്ടെത്തുന്നു...",
        "eligible_schemes_header": "നിങ്ങൾക്കുള്ള യോഗ്യമായ പദ്ധതികൾ:",
        "learn_more": "കൂടുതലറിയുക",
        "no_schemes_found": "നിങ്ങളുടെ പ്രൊഫൈലിനായി പ്രത്യേക പദ്ധതികളൊന്നും കണ്ടെത്തിയില്ല.",

        "recommendations_header": "🌍 വിള ശുപാർശകൾ",
        "recommendations_desc": "നിങ്ങളുടെ സ്ഥലത്തെ കാർഷിക-കാലാവസ്ഥാ മേഖലയെ അടിസ്ഥാനമാക്കി വിള ശുപാർശകൾ നേടുക.",
        "get_recommendations_button": "ശുപാർശകൾ നേടുക",
        "recommendations_spinner": "ശുപാർശകൾ കണ്ടെത്തുന്നു...",
        "recommendations_for": "{city} എന്നതിനായുള്ള ശുപാർശകൾ:",
        "acz": "കാർഷിക-കാലാവസ്ഥാ മേഖല:",
        "suitable_crops": "അനുയോജ്യമായ വിളകൾ:",
        "enter_city": "നഗരം നൽകുക:"
    }
}
# (Note: For brevity, I included 7 languages commonly used in your code snippet.
# If you need the remaining ones exactly as earlier (e.g., Urdu or others), add them with the same keys.)

# --- Language Options (sidebar names -> codes) ---
language_options = {
    "English": "en",
    "हिन्दी (Hindi)": "hi",
    "मराठी (Marathi)": "mr",
    "ગુજરાતી (Gujarati)": "gu",
    "বাংলা (Bengali)": "bn",
    "தமிழ் (Tamil)": "ta",
    "తెలుగు (Telugu)": "te",
    "ಕನ್ನಡ (Kannada)": "kn",
    "മലയാളം (Malayalam)": "ml",
    "ਪੰਜਾਬੀ (Punjabi)": "pa"
}

# --- Helpers ---
def get_lang_dict(lang_code: str) -> dict:
    """Return the language dict with English fallback."""
    return translations.get(lang_code, translations["en"])

def tr(lang_dict: dict, key: str, **kwargs) -> str:
    """Safe translator with fallback and format support."""
    text = lang_dict.get(key, translations["en"].get(key, key))
    try:
        return text.format(**kwargs) if kwargs else text
    except Exception:
        # If formatting fails due to missing kwargs, return raw text
        return text

# --- Sidebar Language Picker ---
with st.sidebar:
    st.header("BhashaBuddy (भाषाबडी)")
    selected_language_name = st.selectbox(
        label="Choose Language:",
        options=list(language_options.keys())
    )
    selected_language_code = language_options.get(selected_language_name, "en")
    t = get_lang_dict(selected_language_code)
    st.markdown("---")
    st.info(tr(t, "sidebar_info"))

# --- Title / Subtitle ---
st.title(f"🌾 {tr(t, 'header')}")
st.markdown(f"#### {tr(t, 'subheader')}")

# --- Tabs ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    tr(t, "tab_expert_diagnosis"),
    tr(t, "tab_mandi"),
    tr(t, "tab_health"),
    tr(t, "tab_schemes"),
    tr(t, "tab_recommendations")
])

# =========================
# Tab 1: Expert Diagnosis + Chat
# =========================
with tab1:
    col1, col2 = st.columns([2, 1], vertical_alignment="top")

    with col1:
        with st.container(border=True):
            st.header(tr(t, "expert_header"))
            st.markdown(tr(t, "expert_desc"))

            expert_crop = st.text_input(tr(t, "enter_crop"), "Tomato")
            crop_stages = ["Sowing", "Vegetative Growth", "Flowering", "Harvesting"]
            expert_stage = st.selectbox(tr(t, "crop_stage"), crop_stages)
            expert_problem = st.text_area(tr(t, "problem_desc"),
                                          "Yellow spots with brown edges on lower leaves.")
            goals = ["Increase Yield", "Improve Quality", "Reduce Costs", "Control Pests"]
            expert_goal = st.selectbox(tr(t, "goal"), goals)

            if st.button(tr(t, "get_plan_button"), use_container_width=True, type="primary"):
                api_endpoint = f"{BACKEND_URL}/api/v1/expert_advice"
                payload = {
                    "crop": expert_crop,
                    "crop_stage": expert_stage,
                    "problem_description": expert_problem,
                    "goal": expert_goal,
                    "lang": selected_language_code
                }
                try:
                    with st.spinner(tr(t, "ai_spinner")):
                        resp = requests.post(api_endpoint, json=payload, timeout=60)
                        resp.raise_for_status()
                        data = resp.json() if resp.content else {}
                        st.subheader(tr(t, "expert_plan_header"))
                        expert_plan_text = data.get("expert_plan", "No plan generated.")
                        st.markdown(expert_plan_text)

                        if expert_plan_text and "error" not in str(expert_plan_text).lower():
                            st.markdown("---")
                            st.subheader(tr(t, "listen_plan"))
                            try:
                                with st.spinner(tr(t, "audio_spinner")):
                                    tts_params = {"text": expert_plan_text, "lang": selected_language_code}
                                    audio_response = requests.get(
                                        f"{BACKEND_URL}/api/v1/generate_audio",
                                        params=tts_params, timeout=60
                                    )
                                    if audio_response.status_code == 200 and audio_response.content:
                                        st.audio(BytesIO(audio_response.content), format="audio/mpeg")
                                    else:
                                        st.error(tr(t, "audio_error"))
                            except requests.exceptions.RequestException:
                                st.error(tr(t, "audio_error"))
                except requests.exceptions.RequestException as e:
                    st.error(f"Connection Error: {e}")

    with col2:
        with st.container(border=True):
            st.header(tr(t, "chatbot_header"))
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # render history
            for m in st.session_state.messages:
                with st.chat_message(m["role"]):
                    st.markdown(m["content"])

            if prompt := st.chat_input(tr(t, "chat_input_placeholder")):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    try:
                        # Convert minimal history for backend (you can adapt to your backend schema)
                        history_for_api = [
                            {"role": msg["role"], "content": msg["content"]}
                            for msg in st.session_state.messages[:-1]
                        ]
                        response = requests.post(
                            f"{BACKEND_URL}/api/v1/chatbot",
                            json={"user_message": prompt, "history": history_for_api, "language": selected_language_code},
                            timeout=60
                        )
                        bot_response = "..."
                        if response.status_code == 200 and response.content:
                            bot_response = response.json().get("response", "...")
                        st.markdown(bot_response)
                        st.session_state.messages.append({"role": "assistant", "content": bot_response})
                    except requests.exceptions.RequestException as e:
                        st.error(f"Connection Error: {e}")

# =========================
# Tab 2: Mandi Price Tracker
# =========================
with tab2:
    with st.container(border=True):
        st.header(tr(t, "mandi_header"))
        st.markdown(tr(t, "mandi_desc"))

        available_states = ["Rajasthan", "Maharashtra", "Punjab", "Uttar Pradesh", "Madhya Pradesh"]
        available_commodities = ["Wheat", "Mustard", "Cotton", "Maize", "Paddy", "Soyabean", "Gram"]

        c1, c2 = st.columns(2)
        with c1:
            selected_state = st.selectbox(tr(t, "select_state"), available_states, key="mandi_state")
        with c2:
            selected_commodity = st.selectbox(tr(t, "select_commodity"), available_commodities, key="mandi_commodity")

        if st.button(tr(t, "get_prices_button"), use_container_width=True):
            api_endpoint = f"{BACKEND_URL}/api/v1/mandi_prices"
            params = {"state": selected_state, "commodity": selected_commodity}
            try:
                with st.spinner(tr(t, "prices_spinner")):
                    response = requests.get(api_endpoint, params=params, timeout=30)
                    response.raise_for_status()
                    data = response.json() if response.content else {}

                    if "error" in data:
                        st.error(f"⚠️ {data.get('error', 'Unknown error')}")
                    else:
                        summary = data.get("summary", "")
                        if summary:
                            st.success(f"**{summary}**")

                        prices = data.get("prices", [])
                        if prices:
                            df = pd.DataFrame(prices)
                            # rename for display, only if columns exist
                            rename_map = {
                                "market_name": "Market",
                                "district": "District",
                                "modal_price": "Price (₹/Quintal)",
                                "arrival_date": "Date"
                            }
                            existing = {k: v for k, v in rename_map.items() if k in df.columns}
                            df = df.rename(columns=existing)
                            st.dataframe(df, use_container_width=True, hide_index=True)
                        else:
                            st.info("No price data received.")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection Error: {e}")

# =========================
# Tab 3: Crop Health
# =========================
with tab3:
    with st.container(border=True):
        st.header(tr(t, "health_header"))
        st.markdown(tr(t, "health_desc"))

        uploaded_file = st.file_uploader(tr(t, "upload_image"), type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            st.image(uploaded_file, caption=tr(t, "uploaded_image_caption"), use_column_width=True)

            if st.button(tr(t, "detect_disease_button"), use_container_width=True):
                with st.spinner(tr(t, "disease_spinner")):
                    try:
                        files = {'image': (uploaded_file.name, uploaded_file, uploaded_file.type)}
                        api_endpoint = f"{BACKEND_URL}/api/v1/detect_disease"
                        response = requests.post(api_endpoint, files=files, timeout=60)
                        if response.status_code == 200 and response.content:
                            data = response.json()
                            st.subheader(tr(t, "detected_disease", disease=data.get('detected_disease', 'Unknown')))
                            score = float(data.get('confidence_score', 0.0)) * 100.0
                            st.warning(tr(t, "confidence_score", score=score))

                            st.markdown(f"<h5>{tr(t, 'organic_remedies')}</h5>", unsafe_allow_html=True)
                            for remedy in data.get('organic_remedies', []):
                                st.markdown(f"- {remedy}")

                            st.markdown(f"<h5>{tr(t, 'chemical_solutions')}</h5>", unsafe_allow_html=True)
                            for solution in data.get('chemical_solutions', []):
                                st.markdown(f"- {solution}")
                        else:
                            st.error("Failed to analyze the image.")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Connection Error: {e}")

# =========================
# Tab 4: Government Schemes
# =========================
with tab4:
    with st.container(border=True):
        st.header(tr(t, "schemes_header"))
        st.markdown(tr(t, "schemes_desc"))

        c1, c2, c3 = st.columns(3)
        with c1:
            gender = st.selectbox(tr(t, "gender"), ["Male", "Female", "Other"])
        with c2:
            land_holding = st.number_input(tr(t, "land_holding"), min_value=0.0, step=0.1, value=0.0)
        with c3:
            is_loanee = st.checkbox(tr(t, "has_loan"))

        if st.button(tr(t, "find_schemes_button"), use_container_width=True):
            api_endpoint = f"{BACKEND_URL}/api/v1/govt_schemes"
            profile = {"gender": gender, "land_holding_acres": land_holding, "is_loanee": is_loanee}
            params = {"state": "Rajasthan", "lang": selected_language_code}
            try:
                with st.spinner(tr(t, "schemes_spinner")):
                    response = requests.post(api_endpoint, json=profile, params=params, timeout=60)
                    if response.status_code == 200 and response.content:
                        data = response.json()
                        st.subheader(tr(t, "eligible_schemes_header"))
                        if data.get("eligible_schemes"):
                            for scheme in data["eligible_schemes"]:
                                with st.expander(scheme.get('name', 'Scheme')):
                                    st.markdown(f"**Description:** {scheme.get('description', '-')}")
                                    link = scheme.get('link')
                                    if link:
                                        st.markdown(f"[{tr(t, 'learn_more')}]({link})")
                        else:
                            st.info(data.get("message", tr(t, "no_schemes_found")))
                    else:
                        st.error("Could not fetch schemes.")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection Error: {e}")

# =========================
# Tab 5: Crop Recommendations
# =========================
with tab5:
    with st.container(border=True):
        st.header(tr(t, "recommendations_header"))
        st.markdown(tr(t, "recommendations_desc"))

        rec_city = st.text_input(tr(t, "enter_city"), "Jodhpur", key="rec_city")
        if st.button(tr(t, "get_recommendations_button"), use_container_width=True):
            api_endpoint = f"{BACKEND_URL}/api/v1/crop_recommendation"
            params = {"city": rec_city, "state": "Rajasthan"}
            try:
                with st.spinner(tr(t, "recommendations_spinner")):
                    response = requests.get(api_endpoint, params=params, timeout=30)
                    if response.status_code == 200 and response.content:
                        data = response.json()
                        st.subheader(tr(t, "recommendations_for", city=rec_city))
                        loc = data.get("location", {})
                        acz = loc.get("agro_climatic_zone", "—")
                        st.success(f"**{tr(t, 'acz')}** {acz}")
                        crops = data.get("recommended_crops", [])
                        if crops:
                            st.markdown(f"**{tr(t, 'suitable_crops')}**")
                            st.markdown(", ".join(crops))
                        else:
                            st.info("No crop recommendations returned.")
                    else:
                        st.error("Could not get recommendations.")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection Error: {e}")
