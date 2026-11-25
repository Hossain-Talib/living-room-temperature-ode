"""Download the real UCI Appliances Energy Prediction dataset (dataset 374)."""
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO

folder = Path(__file__).parent
output = folder / 'data' / 'energydata_complete.csv'
url = 'https://archive.ics.uci.edu/static/public/374/appliances+energy+prediction.zip'

if output.exists():
    print('Dataset already exists:', output)
else:
    print('Downloading official UCI dataset (internet required)...')
    with urlopen(url, timeout=90) as response:
        downloaded = response.read()
    with ZipFile(BytesIO(downloaded)) as archive:
        matching = [name for name in archive.namelist() if name.endswith('energydata_complete.csv')]
        if not matching:
            raise FileNotFoundError('The UCI ZIP did not contain energydata_complete.csv')
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(archive.read(matching[0]))
    print('Downloaded:', output)
print('You can now run: python analysis.py')
