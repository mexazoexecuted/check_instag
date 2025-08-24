#!/usr/bin/env python3
# DEVELOPERS : ./MexazoExecuted
# TEAM : YOUTH OF PANTURA
# INFORMASI : GET INFORMASI INSTAGRAM
# PERINGATAN : JANGAN JUAL SCRIP INI KARENA SCRIPT INI HANYA UNTUK EDUKASI DAN PEMBELAJARAN BAGAIMANA KITA MELIHAT DENGAN DETAIL PADA USERNANE TARGET
# CONTACT DEVELOPERS : https:/t.me/@Abenkkyoy
# JIKA ADA BUG ATAU PUN ERROR DALAM SYSTEM HARAL HUBUNGI DELEVELOPERS AGAR SEGERA DI PERBAIKI !!


import json
import time
import requests
import re
import sys
import os
from os import system
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich import print as rprint

console = Console()
system("clear")

def install_module(module_name, package_name=None):
    if package_name is None:
        package_name = module_name
    try:
        __import__(module_name)
        console.print(f"[bold green]✓ {module_name} sudah terinstall[/]")
        system("clear")
        return True
    except ImportError:
        console.print(f"[bold green]Menginstall {module_name}...[/]")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            system("clear")
            return True
        except Exception as e:
            console.print(f"[bold red]✗ Gagal menginstall {module_name}: {e}[/]")
            return False

def check_dependencies():
    return install_module("requests") and install_module("rich")

def animate_text(text, color="bold white", speed=0.03):
    console.print()
    with console.status(f"[bold {color}]Loading...[/]") as status:
        for i in range(len(text) + 1):
            status.update(f"[bold {color}]{text[:i]}[/]")
            time.sleep(speed)
        time.sleep(0.3)
    console.print()

def print_banner():
    console.print(Panel("""[bold red]

　　　　⢀⣤⣶⣶⣖⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀    [bold red][!]Developers: ./MexazoExecuted
　　　⢀⣾⡟⣉⣽⣿⢿⡿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀    [bold red][!]Version : 1.7
　　⢠⣿⣿⣿⡗⠋⠙⡿⣷⢌⣿⣿⠀⠀⠀⠀⠀⠀⠀     [bold red][!]Script : Free
⣷⣄⣀⣿⣿⣿⣿⣷⣦⣤⣾⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀      [bold red][!]Warning : [bold yelloe]Script Not Sell!!![bold red]
⠈⠙⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀⢀⠀⠀⠀⠀      [bold red][!]Team : YOUTH OF PANTURA
　　⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠻⠿⠿⠋⠀⠀⠀⠀
　　　⠹⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀
　　　　⠈⢿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⡄
　　　　　⠙⢿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⢀⡾⠀
　　　　　　⠈⠻⣿⣿⣿⣿⣷⣶⣴⣾⠏⠀⠀
　　　　　　　　⠈⠉⠛⠛⠛⠋⠁⠀⠀⠀[/]""",
        width=75,
    ))

def get_instagram_user_data(username):
    url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'X-IG-App-ID': '936619743392459',
        'Accept': 'application/json',
        'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    try:
        with console.status(f"[bold yellow]Get In data @{username}...[/]", spinner="dots"):
            response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            console.print(f"[bold red]❌ Username '@{username}' tidak ditemukan![/]")
            system("clear")
            return None
        else:
            console.print(f"[bold red]❌ Error: Status code {response.status_code}[/]")
            system("clear")
            return None
    except Exception as e:
        console.print(f"[bold red]❌ Error: {e}[/]")
        system("clear")
        return None

def analyze_profile_completeness(user):
    completeness_score = 0
    total_items = 5
    if user.get('biography'):
        completeness_score += 1
    if user.get('external_url'):
        completeness_score += 1
    if user.get('profile_pic_url_hd'):
        completeness_score += 1
    if user.get('full_name') and user['full_name'].strip():
        completeness_score += 1
    if user.get('edge_owner_to_timeline_media', {}).get('count', 0) > 0:
        completeness_score += 1
    percentage = (completeness_score / total_items) * 100
    return f"{percentage:.0f}%"

def get_account_age_estimate(user_data):
    try:
        posts = user_data['data']['user']['edge_owner_to_timeline_media']['edges']
        if posts:
            oldest_post = posts[-1]['node']['taken_at_timestamp']
            account_age = (datetime.now().timestamp() - oldest_post) / (365 * 24 * 3600)
            return f"{account_age:.1f} tahun"
    except:
        pass
    return "Tidak dapat diestimasi"

def analyze_following_pattern(followers, following):
    if following == 0:
        return "Tidak following siapapun"
    ratio = followers / following if following > 0 else 0
    if ratio > 10:
        return "Popular (Followers >> Following) 🎯"
    elif ratio > 5:
        return "Selective Following ⚡"
    elif ratio > 1:
        return "Balanced Following ⚖️"
    elif ratio > 0.5:
        return "Followback Strategy 🤝"
    else:
        return "Mass Following 📈"

def extract_profile_insights(user):
    bio = user.get('biography', '')
    insights = {
        'has_email': len(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', bio)) > 0,
        'has_phone': len(re.findall(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}\b|\b\d{3}[-\s]?\d{4}[-\s]?\d{4}\b', bio)) > 0,
        'has_links': len(re.findall(r'https?://[^\s]+', bio)) > 0,
        'bio_length': len(bio),
        'word_count': len(bio.split())
    }
    return insights

def display_profile_details(data, username):
    if not data or 'data' not in data:
        console.print("[bold red]❌ Data Not valid[/]")
        return
    try:
        user = data['data']['user']
        followers = user['edge_followed_by']['count']
        following = user['edge_follow']['count']
        posts = user['edge_owner_to_timeline_media']['count']
        insights = extract_profile_insights(user)
        recent_posts = user['edge_owner_to_timeline_media']['edges'][:3]
        system("clear")
        print_banner()
        basic_info_panel = Panel.fit(
            f"[bold white] Username:[/] [bold green]@{user['username']}[/]\n"
            f"[bold white] Nama Lengkap:[/] [bold green]{user['full_name']}[/]\n"
            f"[bold white] Bio:[/] [bold green]{user.get('biography', 'Tidak ada bio')}[/]\n"
            f"[bold white] Website:[/] [bold green]{user.get('external_url', 'Tidak ada')}[/]\n"
            f"[bold white] Profil URL:[/] [bold green]https://www.instagram.com/{user['username']}/[/]\n\n"
            f"[bold white] Followers:[/] [bold green]{followers:,}[/]\n"
            f"[bold white] Following:[/] [bold green]{following:,}[/]\n"
            f"[bold white] Total Post:[/] [bold green]{posts:,}[/]\n"
            f"[bold white] Rasio Follow:[/] [bold green]{analyze_following_pattern(followers, following)}[/]\n"
            f"[bold white] Tipe Akun:[/] [bold grern]{'Bisnis ' if user.get('is_business_account') else 'Personal '}[/]\n\n"
            f"[bold white] Terverifikasi:[/] {'[bold green]Ya [/]' if user.get('is_verified') else '[bold red]Tidak [/]'}\n"
            f"[bold white] Private:[/] {'[bold green]Ya [/]' if user.get('is_private') else '[bold red]Tidak [/]'}\n"
            f"[bold white] Akun Bisnis:[/] {'[bold green]Ya [/]' if user.get('is_business_account') else '[bold red]Tidak [/]'}\n"
            f"[bold white] Estimasi Usia Akun:[/] [bold green]{get_account_age_estimate(data)}[/]\n"
            f"[bold white] Kelengkapan Profil:[/] [bold green]{analyze_profile_completeness(user)}[/]\n\n"
            f"[bold white] Panjang Bio:[/] [bold green]{insights['bio_length']} karakter[/]\n"
            f"[bold white] Jumlah Kata:[/] [bold green]{insights['word_count']} kata[/]\n"
            f"[bold white] Email di Bio:[/] {'[bold green]Ya ✅[/]' if insights['has_email'] else '[bold red]Tidak [/]'}\n"
            f"[bold white] Telepon di Bio:[/] {'[bold green]Ya ✅[/]' if insights['has_phone'] else '[bold red]Tidak [/]'}\n"
            f"[bold white] Link di Bio:[/] {'[bold green]Ya ✅[/]' if insights['has_links'] else '[bold red]Tidak [/]'}\n\n"
            f"[bold white] Data diambil:[/] [bold green]{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}[/]\n"
            f"[bold white] User ID:[/] [bold green]{user.get('id', 'N/A')}[/]",
            title="[bold green]INFORMASI PENGGUNA[/]",
            border_style="bold white"
        )
        console.print(basic_info_panel)
    except Exception as e:
        console.print(f"[bold red]❌ Error menampilkan data: {e}[/]")
        import traceback
        console.print(f"[bold red]{traceback.format_exc()}[/]")

def main():
    if not check_dependencies():
        console.print("[bold red]❌ Tidak bisa melanjutkan[/]")
        system("clear")
        return
    print_banner()
    while True:
        try:
            username = console.input("[bold white] Masukkan username Instagram: [/]").strip()
            if not username:
                console.print("[bold red]❌ Username tidak boleh kosong![/]")
                system("clear")
                continue
            if username.lower() in ['exit', 'quit', 'keluar']:
                break
            username = username.replace('@', '').strip()
            data = get_instagram_user_data(username)
            if data:
                display_profile_details(data, username)
            cont = console.input("[bold white] Get Informasi Username Lain? (y/n): [/]").lower()
            if cont not in ['y', 'yes', 'ya']:
                system("clear")
                break
        except KeyboardInterrupt:
            console.print("\n\n[bold red]❌ Dihentikan[/]")
            break
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/]")

if __name__ == "__main__":
    main()
