from fastapi import FastAPI, Request, HTTPException
import httpx
import uvicorn

app = FastAPI()

ANGEL_API_URL = "https://apiconnect.angelone.in/rest/secure/angelbroking/order/v1/placeOrder"

@app.get("/")
def home():
    return {"status": "Snipper Machine Angel Bridge is Active!"}

@app.get("/ip")
async def get_my_ip():
    async with httpx.AsyncClient() as client:
        res = await client.get("https://api.ipify.org?format=json")
        return res.json()

@app.post("/place-order")
async def place_order(request: Request):
    try:
        body = await request.json()
        headers = {k: v for k, v in request.headers.items() if k.lower() in [
            "authorization", "x-privatekey", "x-usercode", 
            "x-sourceid", "x-clientlocalip", "x-clientpublicip", 
            "x-macaddress", "content-type", "accept"
        ]}
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(ANGEL_API_URL, json=body, headers=headers)
            return resp.json()
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
