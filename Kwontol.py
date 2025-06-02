# pyright: basic
import httpx
import asyncio


async def claim(t, bearer, address):
    try:
        headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": f"Bearer {bearer}",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Host": "faucet-miniapp.monad.xyz",
            "Origin": "https://faucet-miniapp.monad.xyz",
            "Referer": "https://faucet-miniapp.monad.xyz/",
            "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Storage-Access": "active",
            "sentry-trace": "d3b8c67866f3451a9491d29ae96b72ee-8e095b01352df675",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        }
        claim_url = "https://faucet-miniapp.monad.xyz/api/claim"
        claim_data = {"address": address}
        async with httpx.AsyncClient(headers=headers) as ses:
            res = await ses.post(claim_url, json=claim_data)
            open('http.log', 'a', encoding='utf-8').write(f"{res.text}\n")
            success = res.json().get("success")  # pyright: ignore
            if success:
                print(f"[{t}] ✅ SUCCESS claim faucet!")
            else:
                print(f"[{t}] ❌ FAILED claim faucet!")
    except Exception as e:
        print(f"[{t}] ❌ ERROR: {e}")


async def main():
    bearer = open("bearer.txt").read().strip()
    address = open("address.txt").read().strip()

    total_tasks = 500  # 500 klik per batch
    print(f"⏳ Sending {total_tasks} concurrent requests...")

    tasks = [claim(i + 1, bearer, address) for i in range(total_tasks)]
    await asyncio.gather(*tasks)

    print("✅ Done.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        exit()
