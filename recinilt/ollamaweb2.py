import requests
import json
import subprocess
import sys
from datetime import datetime

class OllamaSearchAgent:
    def __init__(self, api_key, model="gpt-oss:20b"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://ollama.com/api"
    
    def web_search(self, query, max_results=3):
        """Web araması yapar"""
        print(f"🔍 Web araması yapılıyor: '{query}'")
        
        url = f"{self.base_url}/web_search"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "query": query,
            "max_results": max_results
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                results = response.json()
                print(f"✅ {len(results['results'])} sonuç bulundu")
                return results
            else:
                print(f"❌ Arama hatası: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Bağlantı hatası: {e}")
            return None
    
    def create_enhanced_prompt(self, user_question, search_results):
        """Arama sonuçlarını prompt'a ekler"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        context = f"=== GÜNCEL BİLGİLER ({current_time}) ===\n\n"
        
        if search_results and 'results' in search_results:
            for i, result in enumerate(search_results['results'], 1):
                context += f"{i}. KAYNAK: {result['title']}\n"
                context += f"   URL: {result['url']}\n"
                context += f"   İÇERİK: {result['content'][:300]}...\n\n"
        else:
            context += "Web araması sonucu bulunamadı.\n\n"
        
        enhanced_prompt = f"""{context}

=== KULLANICI SORUSU ===
{user_question}

=== TALİMATLAR ===
Yukarıdaki güncel web bilgilerini kullanarak kullanıcının sorusunu Türkçe olarak detaylı şekilde yanıtla.
- Güncel bilgileri öncelikle kullan
- Kendi bilgin varsa ekle
- Kaynak belirt
- Net ve anlaşılır ol"""

        return enhanced_prompt
    
    def ask_ollama(self, prompt):
        """Ollama'ya soru sorar"""
        print(f"🤖 {self.model} modeli düşünüyor...")
        
        try:
            # Ollama komutunu çalıştır
            result = subprocess.run([
                'ollama', 'run', self.model, prompt
            ], capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"Ollama hatası: {result.stderr}"
        except FileNotFoundError:
            return "❌ Ollama bulunamadı. Ollama'nın yüklü ve çalışır durumda olduğundan emin olun."
        except Exception as e:
            return f"❌ Hata: {e}"
    
    def search_and_answer(self, question):
        """Ana fonksiyon: Arama + Ollama cevabı"""
        print("=" * 60)
        print(f"🎯 SORU: {question}")
        print("=" * 60)
        
        # 1. Web araması yap
        search_results = self.web_search(question)
        
        # 2. Gelişmiş prompt oluştur
        enhanced_prompt = self.create_enhanced_prompt(question, search_results)
        
        # 3. Ollama'ya sor
        answer = self.ask_ollama(enhanced_prompt)
        
        print("\n🤖 YANIT:")
        print("-" * 40)
        print(answer)
        print("=" * 60)
        
        return answer

def main():
    # API anahtarınızı buraya yazın
    API_KEY = "ollama_api_keyiniz"
    
    # Ajanı oluştur
    agent = OllamaSearchAgent(API_KEY)
    
    print("🚀 Ollama Web Search Ajanı Başlatıldı!")
    print("Çıkmak için 'quit' yazın\n")
    
    # İnteraktif döngü
    while True:
        try:
            question = input("\n💬 Sorunuzu yazın: ").strip()
            
            if question.lower() in ['quit', 'çık', 'exit', '']:
                print("👋 Görüşürüz!")
                break
            
            # Soruyu işle
            agent.search_and_answer(question)
            
        except KeyboardInterrupt:
            print("\n👋 Program sonlandırıldı!")
            break
        except Exception as e:
            print(f"❌ Beklenmeyen hata: {e}")

if __name__ == "__main__":
    main()