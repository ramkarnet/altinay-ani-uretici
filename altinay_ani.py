import streamlit as st
import google.generativeai as genai
import os

# Sayfa yapılandırması
st.set_page_config(
    page_title="Altınay Anı Üretici 🎭",
    page_icon="🎭",
    layout="centered"
)

# Başlık ve açıklama
st.title("🎭 ALTINAY ANI ÜRETİCİ")
st.markdown("### *Her şeyle anısı olan efsane arkadaşınız için özel anı üreticisi*")
st.divider()

# Yan panel bilgilendirme
with st.sidebar:
    st.header("📖 Nasıl Kullanılır?")
    st.markdown("""
    1. **Anahtar kelimeler** girin (örn: pizza, kedi, matematik)
    2. **Yıl** seçin (1990-2024)
    3. **Anı Üret** butonuna tıklayın
    4. Altınay'ın o konuyla ilgili muhteşem anısını okuyun! 😄
    
    ---
    
    *Not: Bu uygulama tamamen eğlence amaçlıdır ve yapay zeka tarafından üretilen kurgusal anılardır.*
    """)
    
    st.info("💡 **İpucu:** Ne kadar absürd kelimeler girerseniz o kadar eğlenceli sonuçlar alırsınız!")
    
    st.success("✨ **Powered by Google Gemini** - Tamamen ücretsiz!")

# Ana form
col1, col2 = st.columns([3, 1])

with col1:
    keywords = st.text_input(
        "🔑 Anahtar Kelimeler",
        placeholder="Örn: pizza, kedi, matematik sınavı",
        help="Virgülle ayırarak birden fazla kelime girebilirsiniz"
    )

with col2:
    year = st.number_input(
        "📅 Yıl",
        min_value=1990,
        max_value=2024,
        value=2010,
        step=1
    )

# Anı tonu seçimi
tone = st.select_slider(
    "🎨 Anı Tonu",
    options=["Dramatik", "Komik", "Nostaljik", "Epik", "Absürt"],
    value="Komik"
)

st.divider()

# Anı üret butonu
if st.button("✨ Anı Üret", type="primary", use_container_width=True):
    if not keywords.strip():
        st.error("❌ Lütfen en az bir anahtar kelime girin!")
    else:
        with st.spinner("🎭 Altınay'ın anısı üretiliyor..."):
            try:
                # Google Gemini API configuration
                api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
                
                if not api_key:
                    st.error("❌ GEMINI_API_KEY bulunamadı! Lütfen API anahtarınızı ayarlayın.")
                    st.info("💡 API anahtarı almak için: https://makersuite.google.com/app/apikey")
                    st.stop()
                
                genai.configure(api_key=api_key)
                
                # Prompt hazırlama
                tone_descriptions = {
                    "Dramatik": "dramatik, duygusal ve etkileyici bir şekilde",
                    "Komik": "komik, eğlenceli ve gülünç detaylarla dolu",
                    "Nostaljik": "nostaljik, içten ve özlem dolu",
                    "Epik": "epik, kahramanca ve abartılı bir şekilde",
                    "Absürt": "tamamen absürt, mantıksız ama eğlenceli bir şekilde"
                }
                
                prompt = f"""Sen Altınay'ın yakın bir arkadaşısın ve onun hakkında bir anı anlatıyorsun. 
Altınay gerçekten HER ŞEYLE anısı olan, inanılmaz deneyimleri olan birisidir.

Şu anahtar kelimelerle ilgili {year} yılında yaşanmış bir Altınay anısı üret: {keywords}

Anı {tone_descriptions[tone]} olmalı.

Anıyı birinci şahıs (ben) perspektifinden anlat, sanki sen oradaydın ve Altınay'la birlikte yaşadın.
Anı gerçekçi detaylar içermeli ama aynı zamanda Altınay'ın bu konuyla nasıl özel bir bağlantısı olduğunu göstermeli.
200-300 kelime arası olsun.

Sadece anıyı yaz, başka açıklama ekleme."""

                # Gemini API çağrısı
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt)
                
                # Sonucu göster
                st.success("✅ Anı başarıyla üretildi!")
                st.markdown("---")
                
                # Anı kartı
                st.markdown(f"""
                <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #ff4b4b;">
                    <h3 style="color: #ff4b4b; margin-top: 0;">📖 Altınay'ın {year} Anısı</h3>
                    <p style="font-style: italic; color: #666;">Anahtar Kelimeler: {keywords}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("")
                st.markdown(f"*{response.text}*")
                st.markdown("---")
                
                # Paylaş butonu
                st.markdown("### 💬 Beğendiniz mi?")
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    if st.button("👍 Harika!"):
                        st.balloons()
                with col_b:
                    if st.button("😂 Çok Komik"):
                        st.snow()
                with col_c:
                    if st.button("🔄 Yeni Anı"):
                        st.rerun()
                
            except Exception as e:
                st.error(f"❌ Bir hata oluştu: {str(e)}")
                st.info("💡 API anahtarınızı kontrol edin. Streamlit secrets veya environment variable olarak GEMINI_API_KEY tanımlamalısınız.")
                st.info("🔑 API anahtarı almak için: https://makersuite.google.com/app/apikey")

# Alt bilgi
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9em;">
    <p>🎭 Altınay Anı Üretici v2.0 - Gemini Edition</p>
    <p>Google Gemini AI destekli eğlence uygulaması | Tüm anılar kurgusaldır 😄</p>
    <p>✨ Tamamen ücretsiz API kullanımı!</p>
</div>
""", unsafe_allow_html=True)
