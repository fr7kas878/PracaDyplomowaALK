

echo "=== Aktywacja venv ==="
source .venv/bin/activate

echo "=== Aktualizacja pip ==="
python -m pip install --upgrade pip

echo "=== Instalacja Playwright ==="
pip install playwright

echo "=== Instalacja przeglądarek ==="
python -m playwright install

echo "=== Instalacja zależności systemowych ==="
python -m playwright install-deps

echo "=== GOTOWE ==="