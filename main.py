import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

def checkWhats(numero):
    response = ''
    while True:
        try:
            headers = {
                'content-type': 'application/json',
            }
            response = requests.get(
                f'https://api.z-api.io/instances/{instancia_id}/token/{instancia_token}/phone-exists/55{numero}',
                headers=headers,
            ).json()
            break
        except:
            continue
    return response

def remove_duplicate_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Using a set to store unique lines
    unique_lines = set()

    for line in lines:
        # Strip leading/trailing whitespaces and add to the set
        unique_lines.add(line.strip())

    with open(file_path, 'w') as file:
        # Write back the unique lines to the file
        file.write('\n'.join(unique_lines))

def remove_google_links(links):
    keywords_to_exclude = ["google", "support.google", "policies.google"]
    filtered_links = [link for link in links if not any(keyword in link for keyword in keywords_to_exclude)]
    return filtered_links

def get_search_results(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def extract_links(html):
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        parsed_url = urllib.parse.urlparse(href)
        if parsed_url.netloc and parsed_url.scheme:
            links.append(parsed_url.geturl())
    return links

def save_links_to_file(links, filename):
    with open(filename, "a") as file:  # Use "a" mode for appending instead of "w" for writing
        for link in links:
            file.write(link + "\n")

def perform_google_search(query, filename):
    try:
        html = get_search_results(query)
        links = extract_links(html)
        filtered_links = remove_google_links(links)
        save_links_to_file(filtered_links, filename)
        remove_duplicate_lines(filename)
        print(f"Salvo com sucesso {len(filtered_links)} links para {filename}.")
    except requests.HTTPError as e:
        print(f"Ocorreu um erro: {e}")

def extract_cell_numbers(text):
    # Pattern to match phone numbers
    regex = r"\b(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4})\b"
    phone_numbers = re.findall(regex, text)
    return phone_numbers

def extract_cell_numbers_from_file(links_filename, output_filename):
    with open(links_filename, "r") as file:
        links = file.readlines()

    cell_numbers = []
    for link in links:
        link = link.strip()
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
            response = requests.get(link, headers=headers)
            response.raise_for_status()
            numbers = extract_cell_numbers(response.text)
            cell_numbers.extend(numbers)
        except requests.HTTPError as e:
            pass

    with open(output_filename, "a") as file:  
        for number in cell_numbers:
            file.write(number + "\n")

    remove_duplicate_lines(output_filename)
    print(f"Telefones salvos em:  {output_filename}.")

if __name__ == '__main__':
    print("""
          

██████  ███    ███ ██ ████████ ██████  ██        ██████  ███████ ████████ ██    ██ 
██   ██ ████  ████ ██    ██    ██   ██ ██       ██       ██         ██    ██    ██ 
██   ██ ██ ████ ██ ██    ██    ██████  ██ █████ ██   ███ ███████    ██    ██    ██ 
██   ██ ██  ██  ██ ██    ██    ██   ██ ██       ██    ██      ██    ██     ██  ██  
██████  ██      ██ ██    ██    ██   ██ ██        ██████  ███████    ██      ████ 
       TELEGRAM: +7 906 849 1831                                   RECUSE IMITAÇÕES""")
    print('Escolha uma opção - Digite somente o número sem parênteses!')
    print(' (1) -  para pesquisa e extração de links')
    print(' (2) -  para extração de telefones dos links')
    print(' (3) -  para verificar se existe WhastApp')
    print(' (4) -  para sair e finalizar o programa')
    resposta = input('Digite sua resposta: ')

    if resposta == '1':
        fila_pesquisa = input('Digite sua palavra-chave para pesquisa e extração: ')
        saida_file = "links.txt"
        perform_google_search(fila_pesquisa, saida_file)

    elif resposta == '2':
        links_name_file = "links.txt"
        saida_name_file = "telefones.txt"
        extract_cell_numbers_from_file(links_name_file, saida_name_file)
        
    elif resposta == '3':
        print('A validação vai ser a partir dos telefones salvos na ETAPA/OPÇÃO 2')
        instancia_id = input('Digite seu instancia_id: ')
        instancia_token = input('Digite seu instancia_token: ')
        if not instancia_id and instancia_token:
            print('Os campos não podem ser vazios.')
            print('Encerrando...')
            exit()
            
        else:
            db = open('telefones.txt', 'r')
            linhas = db.readlines()
            aprovados = open('lista_whatsapp.txt', 'a')
            for linha in linhas:
                numero = linha.strip()
                while True:
                    try:
                        if checkWhats(numero)['exists'] == True:
                            with open('lista_whatsapp.txt', 'a') as file:
                                file.write(numero + '\n')
                        break
                    except Exception as e:
                        print(e)
                        continue
            aprovados.close()
            print('WhatApp salvos..')                                                                 
        
    elif resposta == '4':
        print('Programa encerrado.')
        exit()

    elif resposta != '1' or '2' or '3' or '4':
        print('Escolha somente entre 1, 2, 3 ou 4')
        
print('Feito por: dmitri-gstv!')
print('Feito por: dmitri-gstv!')
print('Feito por: dmitri-gstv!')