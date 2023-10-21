
# Projekt Asystent
[info o projekcie]

## Spis Treści

- [Instrukcja GitFlow](#instrukcja-gitflow)
- [Instrukcje rozruchowe](#instrukcje-rozruchowe)
- [TODOs](#todos)


# Instrukcja GitFlow

### Podstawowe Zasady:

- **main**: Zawsze zawiera działający, sprawdzony kod, który jest gotowy do produkcji.
- **development**: Główna gałąź rozwoju, zawiera najnowsze zmiany/kod, który został zatwierdzony, ale nie jest jeszcze gotowy do produkcji.
  
### Proces Tworzenia Funkcji/Komponentu:

#### 1. Utworzenie Brancha Funkcji

- Każda nowa funkcja/komponent powinna być tworzona na nowym branchu.
  
  ```bash
  git checkout -b feature/your_feature_name develop
  ```
  
#### 2. Praca nad Funkcją/Komponentem

- Wykonaj wszystkie zmiany dotyczące danej funkcji/komponentu na tym branchu.
- Zatwierdzaj (commit) zmiany z czytelnym i konkretnym komunikatem.

  ```bash
  git commit -m "Add a concise and descriptive message about changes"
  ```
  
#### 3. Publikacja Brancha Funkcji

- Udostępnij swój branch na zdalnym repozytorium.

  ```bash
  git push origin feature/your_feature_name
  ```

#### 4. Pull Request (PR)/Merge Request (MR)

- Po zakończeniu pracy nad funkcją, utwórz PR/MR do brancha `development`.
- Prośba o przegląd kodu przez przynajmniej jednego innego członka zespołu.
  
### Hotfixes

Jeśli napotkasz krytyczny błąd, który musi zostać natychmiast naprawiony na głównej gałęzi (np. `main`):

```bash
git checkout -b hotfix/your_hotfix_name master
```
  
Następnie, po zakończeniu pracy i przetestowaniu, hotfix powinien zostać scalony z powrotem zarówno do `main`, jak i do `development` (lub innego odpowiedniego brancha funkcji).

### Wskazówki Ogólne

- **Zawsze** pobieraj najnowszy kod z brancha, na którym pracujesz przed rozpoczęciem pracy na nowej funkcji/komponentu.
- Upewnij się, że Twój kod jest zgodny z wszelkimi standardami lub wytycznymi zespołu.
- Przetestuj swój kod lokalnie przed przesłaniem go na zdalne repozytorium.
- Zawsze komunikuj się z zespołem na temat postępów i wszelkich problemów, które mogą wystąpić.

### Czytaj Więcej

Zalecam również zapoznanie się z [oficjalnym przewodnikiem GitFlow](https://nvie.com/posts/a-successful-git-branching-model/) dla pełniejszego obrazu tego podejścia do zarządzania gałęziami.

### Przykład Cyklu Życia Brancha

1. **Tworzenie Brancha**: Developer tworzy brancha funkcji.
2. **Praca nad Kodem**: Zmiany są dodawane i zatwierdzane na branchu funkcji.
3. **Weryfikacja Kodu**: Poprzez proces recenzji kodu.
4. **Scalanie**: Po zatwierdzeniu, branch funkcji jest scalany z `development`.
5. **Testowanie**: Kod jest testowany w środowisku zbliżonym do produkcyjnego.
6. **Przygotowanie do Produkcji**: Kod z `development` jest przygotowywany do umieszczenia na `main`.
7. **Wdrożenie**: Kod z `main` jest wdrażany na środowisko produkcyjne.

### Koniec

# Instrukcje rozruchowe

## Inicjalizacja bazy
W katalogu głównym wpisać:
```bash
python3 database/init_db.py 
```

## Pobranie wiadomości z maila
Po inicjalizacji bazy danych wkatalogu głównym
```bash
python3 mail_api/mail_api.py 
```

## Aplikacja monitorująca
Aby uruchomić aplikację, należy wykonać poniższą komendę na poziomie głównego katalogu projektu:
```bash
python3 -m flask_app.app
```
Po pomyślnym uruchomieniu, aplikacja będzie dostępna pod adresem http://127.0.0.1:5000/


# TODOs

## Modernizacja systemu: dokumentacja, logi, testy:
- [ ] Przygotować dokumentację dla całego systemu
- [ ] Sprawdzić czy wszystkie pliki mają logi i testy prowadzące do folerów -> Prompt: "dodaj do kodu logi które będą informować o tym że serwer działa, która funkcja została wywołana, monitorujące stan serwera + kod"
- [ ] Nie tworzą się pliki log w flask_app/app.py i database/operations/queries.py
- [ ] Należy dodać testy dal plkiów database - obecnie są tylko dla init_db.py, session_db.py, operations/queries.py

## Asystenci:
- [ ] dodać serwer który cały czas monitoruje co dzieje się w aplikacji
- [ ] analogicznie do asystenta logów asystent testowania

## Baza danych:
- [x] stworzyć część aplikacji odpowiedzialną za inicjalizowanie bazy
- [x] stworzyć serwis wyświetlający zawartość bazy
- [ ] podpiąć bazę pod endpointy od przetwarzania wiadomości
- [ ] przetestować zapisywanie attachment
- [ ] nie zapisuje się ścieżka do attachment
- [ ] w operations/queries.py jest TODO

## Sztuczna Inteligencja:
- [ ] Podpiąć model
- [ ] Skonfigurować bazę pod model

## Telegram:
- [ ] Nie działa pobieranie wiadomości

## Komunikatory:
- [ ] dodać i przetestować pobieranie attachmentów

## Funkcjonalności:
- [ ] Ekstrakcja wszystkich kontaktów z maila | Zapisanie do bazy informacji na temat osoby
- [ ] Dodać w aplikacji wyświetlanie tylko kolumn
- [ ] Dodać w aplikacji navbar
- [ ] -> docs/supervisor.txt system do fallback


## Uwagi dotyczące `WP_api.py`:
Jeśli napotkasz błędy związane z `chromedriver`, upewnij się, że masz odpowiednie uprawnienia do jego uruchamiania. Możesz to zrobić przy pomocy poni
