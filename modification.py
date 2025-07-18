import requests

def process_host_file():
    # URL источника
    url = "https://raw.githubusercontent.com/neodevpro/neodevhost/master/host"
    output_file = "sophos_web_blocklist.txt"
    
    try:
        # Скачиваем файл
        response = requests.get(url)
        response.raise_for_status()
        
        lines = response.text.splitlines()
        clean_domains = []
        
        for line in lines:
            # Убираем пробелы в начале и конце
            line = line.strip()
            
            # Пропускаем комментарии (строки начинающиеся с #)
            if line.startswith('#') or not line:
                continue
            
            # Убираем "0.0.0.0 " из начала строки
            if line.startswith('0.0.0.0 '):
                domain = line[8:].strip()  # Убираем "0.0.0.0 " (8 символов)
                
                # Проверяем, что домен не пустой и не содержит системные записи
                if domain and domain not in ['localhost', 'broadcasthost', 'local']:
                    clean_domains.append(domain)
            
            # Также обрабатываем строки с 127.0.0.1 (если есть)
            elif line.startswith('127.0.0.1 '):
                domain = line[10:].strip()  # Убираем "127.0.0.1 " (10 символов)
                
                if domain and domain not in ['localhost', 'broadcasthost', 'local']:
                    clean_domains.append(domain)
        
        # Убираем дубликаты и сортируем
        clean_domains = sorted(list(set(clean_domains)))
        
        # Сохраняем результат
        with open(output_file, 'w', encoding='utf-8') as f:
            for domain in clean_domains:
                f.write(domain + '\n')
        
        print(f"Обработано доменов: {len(clean_domains)}")
        print(f"Результат сохранен в: {output_file}")
        
    except requests.RequestException as e:
        print(f"Ошибка при скачивании файла: {e}")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    process_host_file()