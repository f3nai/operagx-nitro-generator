import requests
import time
import random
from colorama import Fore

DEFAULT_TIMEOUT_SECONDS = 60
ROTATE_CYCLE = 10
ROTATE_ON_RATELIMIT = True

headersData = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "sec-ch-ua": "\"Opera GX\";v=\"105\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "Referer": "https://www.opera.com/",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}

apiLink = "https://api.discord.gx.games/v1/direct-fulfillment"
body = "{\"partnerUserId\":\"cbff3f16cf548aa83eccf98003f4e4d8ff6e4d7eb22ae496c16dab75e4047d19\"}"
linkPrefix = "https://discord.com/billing/partner-promotions/1180231712274387115/"
currentProxy = None
currentPos = 0

proxies = []

# proxy loader
def loadProxies():
    ProxyFile = open("proxies.txt", "r")
    __proxyData = ProxyFile.read()

    global proxies
    proxies = __proxyData.split("\n")
    print(Fore.RED + '[PROXY] Loaded ' + str(len(proxies)) + " proxies!")
    rotateProxy()

# random proxy returner
def getRandomProxy():
    choice = random.choice(proxies)

    if choice == currentProxy:
        return getRandomProxy()
    
    return choice

# Rotate proxy
def rotateProxy():
    newProxy = getRandomProxy()
    global currentProxy
    currentProxy = newProxy
    print(Fore.CYAN + "[ROTATION] Rotated to new proxy: " + newProxy)
    print(Fore.GREEN + "[PROXY] Remaining proxy amount: " + str(len(proxies)))

# nitro generator
def generateNitro():
    try:
        requestProxy = {
            'http': currentProxy,
        }
        
        response = requests.post(apiLink, headers=headersData, data=body, proxies=requestProxy)
        link = linkPrefix + response.json()['token']

        f = open("output.txt", "a")
        f.write(link + "\n")
        print(Fore.GREEN + "[VALID] " + link)
        global currentPos
        currentPos = currentPos + 1
    except requests.exceptions.JSONDecodeError: # if theres no token value
        if ROTATE_ON_RATELIMIT:
            print(Fore.RED + '[ERROR] Being ratelimited by Discord! Rotating proxy now..')
            
            # Rotate to new proxy
            proxies.remove(currentProxy)
            print(Fore.CYAN + "[PROXY] Removed " + currentProxy + " from the proxy list!")
            rotateProxy()  

            generateNitro()
        else:
            print(Fore.RED + '[ERROR] Being ratelimited by Discord! Will refresh in ' + str(DEFAULT_TIMEOUT_SECONDS) +  ' seconds..')
            # rotate to new proxy
            proxies.remove(currentProxy)
            print(Fore.CYAN + "[PROXY] Removed " + currentProxy + " from the proxy list!")
            rotateProxy()
            
            time.sleep(DEFAULT_TIMEOUT_SECONDS)
            generateNitro()
# Main function
def main():
    open("output.txt", "a")
    print(Fore.RED + """
                                                      
   ▄████████    ▄████████ ███▄▄▄▄      ▄████████  ▄█  
  ███    ███   ███    ███ ███▀▀▀██▄   ███    ███ ███  
  ███    █▀    ███    █▀  ███   ███   ███    ███ ███▌ 
 ▄███▄▄▄      ▄███▄▄▄     ███   ███   ███    ███ ███▌ 
▀▀███▀▀▀     ▀▀███▀▀▀     ███   ███ ▀███████████ ███▌ 
  ███          ███    █▄  ███   ███   ███    ███ ███  
  ███          ███    ███ ███   ███   ███    ███ ███  
  ███          ██████████  ▀█   █▀    ███    █▀  █▀   
                                                      
""")
    loadProxies()
    amountWanted = int(input(Fore.RED + "How many Nitro links do you need?\n> "))

    for i in range(amountWanted):
        #print("[" + str(i + 1) + "] Generated nitro!")
        generateNitro()

        if currentPos == amountWanted:
            print(Fore.GREEN + "[FINISH] Finished process! Exiting now..")
            ##exit()
        
        if currentPos % ROTATE_CYCLE == 0:
            rotateProxy()

## made by @f3nai. DO NOT TAKE CREDITS
main()