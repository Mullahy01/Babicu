# pyright: basic
import httpx
import asyncio
import requests


async def claim(t, bearer, address):
    try:
        headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": f"Bearer {bearer}",
            # "baggage": "sentry-environment=vercel-production,sentry-release=07d1a93d09c736d4e29bd38d95b510c7c430a397,sentry-public_key=9cd8084e4c392be803a6305f665971e6,sentry-trace_id=d3b8c67866f3451a9491d29ae96b72ee,sentry-org_id=4508965485674496",
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
            open('http.log','a',encoding='utf-8').write(f"{res.text}\n")
            success = res.json().get("success")  # pyright: ignore
            if success:
                print(f"[{t}] success claim faucet !")
            else:
                print(f"[{t}] failed claim faucet !")
    except:  # noqa: E722
        print(f"[{t}] failed claim faucet !")


async def main():
    bearer = open("bearer.txt").read().splitlines()[0]
    address = open("address.txt").read().splitlines()[0]
    th = input("input thread : ")
    tasks = []
    for i in range(int(th)):
        tasks.append(claim(i + 1, bearer, address))
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        exit()
