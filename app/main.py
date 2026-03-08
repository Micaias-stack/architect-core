from fastapi import FastAPI, HTTPException, Query
import httpx, random

app = FastAPI()

# Simulação de Evasão (User-Agents Rotativos)
UA_LIST = ["Mozilla/5.0 Chrome/119.0", "AppleWebKit/537.36 Safari/605.1"]

@app.get("/execute")
async def start_process(url: str = Query(...)):
    headers = {"User-Agent": random.choice(UA_LIST)}
    
    async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
        try:
            # Orquestração e Evasão em tempo real
            response = await client.get(url, timeout=10.0)
            return {"status": 200, "data_preview": response.text[:500]}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
