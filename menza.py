#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import datetime

# Program címe és verziószám
print("━━━━━━━━━━━━━━━━━━━━━━━")

print("REFI-Menza Fetcher v1.0")

print("By Takács")

print("━━━━━━━━━━━━━━━━━━━━━━━")

# Étkezési menü weboldala
URL = "https://refi-papa.hu/etlap/"

# Weboldal letöltése és táblázat kinyerése
def get_menu():
    print("\U0001F4E1 Próbálkozom az étlap letöltésével...")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
        print("✅ Weboldal sikeresen letöltve!")
    except requests.exceptions.RequestException as e:
        print(f"❌ Hiba történt az oldal letöltésekor: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Keresés a táblázatban
    table = soup.find('table')
    if not table:
        print("⚠️ Nem található étlap táblázat a weboldalon!")
        return None

    rows = table.find_all('tr')
    menu = []

    for row in rows:
        cols = row.find_all('td')
        if cols:
            menu.append([col.get_text(strip=True) for col in cols])

    if not menu:
        print("⚠️ A táblázat nem tartalmaz étkezési adatokat.")
        return None

    print("✅ Heti menü sikeresen kinyerve!")
    return menu

# Mai napi menü kiírása
def get_today_menu():
    weekly_menu = get_menu()
    if not weekly_menu:
        return "❌ Nincs elérhető étlap."

    today = datetime.datetime.today()
    weekday = today.weekday()  # 0 = Hétfő, 6 = Vasárnap
    napok = ["Hétfő", "Kedd", "Szerda", "Csütörtök", "Péntek", "Szombat", "Vasárnap"]

    if weekday >= 5:
        return "🎉 Ma hétvége van, nincs menza!"

    today_menu = weekly_menu[weekday + 1]  # +1, mert az első sor lehet fejléc
    ebéd = today_menu[3] if len(today_menu) > 3 else "Nincs adat"  # **Ebéd** a 4. oszlopból
    vacsora = today_menu[5] if len(today_menu) > 5 else "Nincs adat"  # **Vacsora** az 5. oszlopból

    today_str = today.strftime("%m.%d.")

    # Szebb, letisztultabb kiírás, plusz sorközzel az ebéd és vacsora között
    return f"""
━━━━━━━━━━━━━━━━━━━━━━━
📅 {napok[weekday]} {today_str}
━━━━━━━━━━━━━━━━━━━━━━━

🍽 Ebéd:  
{ebéd}

🌙 Vacsora:  
{vacsora}

━━━━━━━━━━━━━━━━━━━━━━━
"""

# Futtatás főprogramként
if __name__ == "__main__":
    today = datetime.datetime.today()
    weekday = today.weekday()
    napok = ["Hétfő", "Kedd", "Szerda", "Csütörtök", "Péntek", "Szombat", "Vasárnap"]

    print(f"\n📆 Mai nap: {napok[weekday]} {today.strftime('%m.%d.')}")

    if weekday < 5:
        print(get_today_menu())
    else:
        print("🎉 Ma hétvége van, nincs menza!")
