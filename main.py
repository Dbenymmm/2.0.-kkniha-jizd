from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import json
import os
import uuid
from openpyxl import load_workbook
import tempfile

# ----- Konfigurace -----
CARS_JSON = [
  {
    "Firma": "OK BROKERS s.r.o.",
    "IČO": 25267001,
    "Vozidlo": "Škoda Superb",
    "RZ": "8M15169",
    "PHM": "Nafta",
    "Spotřeba l/100km": 6.23,
    "Řidič/odpovědná osoba": "Kubišová Jana"
  },
  {
    "Firma": "OK ECONOMY s.r.o.",
    "IČO": 44014929,
    "Vozidlo": "Škoda Superb",
    "RZ": "OKH00003",
    "PHM": "Benzín",
    "Spotřeba l/100km": 6.23,
    "Řidič/odpovědná osoba": "Šimková Petra"
  },
  {
    "Firma": "OK GROUP",
    "IČO": 28110056,
    "Vozidlo": "BMW 5",
    "RZ": "OKH00033",
    "PHM": "Benzín",
    "Spotřeba l/100km": 6.4,
    "Řidič/odpovědná osoba": "Ing. Michal Kubiš"
  },
  {
    "Firma": "Agroteam CZ s.r.o.",
    "IČO": 25561804,
    "Vozidlo": "Škoda Kodiaq",
    "RZ": "OKH30620",
    "PHM": "Benzín",
    "Spotřeba l/100km": 7.4,
    "Řidič/odpovědná osoba": "Kubišová Iva"
  },
  {
    "Firma": "OK Group a.s.",
    "IČO": 25561804,
    "Vozidlo": "BMW X5",
    "RZ": "7AA3030",
    "PHM": "Nafta",
    "Spotřeba l/100km": 9.9,
    "Řidič/odpovědná osoba": "Milan Ondra"
  },
  {
    "Firma": "OK GROUP s.r.o.",
    "IČO": 25561804,
    "Vozidlo": "ASTON MARTIN",
    "RZ": "OKH00007",
    "PHM": "Benzín",
    "Spotřeba l/100km": 10.2,
    "Řidič/odpovědná osoba": "Ing. Vladimíra Kubišová"
  },
  {
    "Firma": "OK Group a.s.,",
    "IČO": 25561804,
    "Vozidlo": "Škoda Superb",
    "RZ": "2BZ1888",
    "PHM": "Benzín",
    "Spotřeba l/100km": 6.23,
    "Řidič/odpovědná osoba": "Maloch Jan"
  },
  {
    "Firma": "OK Group a.s.",
    "IČO": 25561804,
    "Vozidlo": "Škoda Superb",
    "RZ": "2BZ1777",
    "PHM": "Benzín",
    "Spotřeba l/100km": 6.23,
    "Řidič/odpovědná osoba": "Malochová Renata"
  },
  {
    "Firma": "OK KLIENT a.s.",
    "IČO": 29185114,
    "Vozidlo": "BMW 5",
    "RZ": "OKH00088",
    "PHM": "Benzín",
    "Spotřeba l/100km": 6.4,
    "Řidič/odpovědná osoba": "Kubiš Radoslav ml."
  },
  {
    "Firma": "OK Group a.s.",
    "IČO": 25561804,
    "Vozidlo": "BMW 5",
    "RZ": "OKH00011",
    "PHM": "Natural",
    "Spotřeba l/100km": 6.4,
    "Řidič/odpovědná osoba": "Ing Kubiš Radoslav"
  },
  {
    "Firma": "Agroteam CZ s.r.o.",
    "IČO": 25561804,
    "Vozidlo": "LR Defender",
    "RZ": "OKH00001",
    "PHM": "Benzín",
    "Spotřeba l/100km": 11,
    "Řidič/odpovědná osoba": "Ing. Kubiš Radoslav"
  },
  {
    "Firma": "Agroteam CZ s.r.o.",
    "IČO": 25561804,
    "Vozidlo": "Range Rover",
    "RZ": "0KH11111",
    "PHM": "Benzín",
    "Spotřeba l/100km": 10.2,
    "Řidič/odpovědná osoba": "Ing. Kubiš Radoslav"
  },
  {
    "Firma": "OK GRANT s.r.o.",
    "IČO": 28268318,
    "Vozidlo": "BMW 8",
    "RZ": "0KH00002",
    "PHM": "Benzín",
    "Spotřeba l/100km": 7.4,
    "Řidič/odpovědná osoba": "Ing. Vladimíra Kubišová"
  }
]

EXCEL_TEMPLATE_PATH = "Template_Kniha_jizd_simulace.xlsx"

app = FastAPI()

# Umožníme servírovat statický frontend (index.html)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root():
    # Frontendová stránka na /static/index.html
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()

@app.get("/cars")
def get_cars():
    return CARS_JSON

@app.post("/simulate")
async def simulate(request: Request):
    """
    Očekává JSON ve formátu:
    {
        "car": {...},
        "events": [{...}]
    }
    """
    data = await request.json()
    car = data["car"]
    events = data["events"]

    # Zde by byla logika pro trasování, AI simulaci a zápis do excelu (pro ukázku dummy zápis)
    file_id = str(uuid.uuid4())
    temp_path = os.path.join(tempfile.gettempdir(), f"{file_id}.xlsx")
    wb = load_workbook(EXCEL_TEMPLATE_PATH)
    ws = wb.active

    # Zápis do šablony – ukázka
    ws["B3"] = car["Vozidlo"]
    ws["B4"] = car["IČO"]
    ws["B5"] = car["Vozidlo"]
    ws["B6"] = car["RZ"]
    ws["B7"] = car["PHM"]
    ws["B8"] = car["Řidič/odpovědná osoba"]

    # Dummy data do tabulky (A10:E11)
    ws["A10"] = "01.04.2025"
    ws["B10"] = "Tankování: Brno"
    ws["C10"] = "Brno–Praha"
    ws["D10"] = 210
    ws["E10"] = "Služební cesta"

    wb.save(temp_path)
    return {"success": True, "download_url": f"/download/{file_id}"}

@app.get("/download/{file_id}")
def download_excel(file_id: str):
    temp_path = os.path.join(tempfile.gettempdir(), f"{file_id}.xlsx")
    return FileResponse(temp_path, filename="Kniha_jizd.xlsx")

