from fastapi import FastAPI, HTTPException, Query
import httpx
import random
import asyncio
from datetime import datetime

app = FastAPI(title="Architect_v30_Final")

# --- BANCO DE CABEÇALHOS REAIS (Fingerprinting) ---
# Em vez de fake-useragent, usamos perfis reais para evitar detecção por discrepância de headers
BROWSER_PROFILES = [
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Sec-Ch-Ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
    },
    {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
    }
]

@app.get("/execute")
async def start_process(url: str = Query(...)):
    # 1. EVASÃO: Seleção de Perfil Completo (Fingerprint)
    profile = random.choice(BROWSER_PROFILES)
    
    # 2. EVASÃO: Jitter (Atraso aleatório para simular humano)
    # Isso evita que o site pago detecte um robô pela velocidade sobre-humana
    await asyncio.sleep(random.uniform(0.5, 2.0))
    
    # 3. ORQUESTRAÇÃO: Cliente HTTP/2 (Mais difícil de detectar que HTTP/1.1)
    async with httpx.AsyncClient(
        headers=profile, 
        follow_redirects=True, 
        http2=True,
        verify=False # Ignora SSL se necessário para certos proxies
    ) as client:
        try:
            # 4. EXECUÇÃO
            response = await client.get(url, timeout=15.0)
            
            # Log de auditoria simples
            print(f"[{datetime.now()}] Request sent to {url} using {profile['User-Agent'][:20]}...")
            
            return {
                "status": response.status_code,
                "data_preview": response.text[:1000],
                "fingerprint_used": profile["User-Agent"]
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro na Orquestração: {str(e)}")
