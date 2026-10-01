import html
import shutil
import subprocess
import tempfile
from pathlib import Path

from backend.schemas import PartyDataSchema


def create_extract_pdf(party: PartyDataSchema) -> bytes:
    """Render a readable PDF extract with the locally installed Edge browser."""
    edge = next((item for item in (
        shutil.which("msedge"),
        shutil.which("chromium"),
        shutil.which("chromium-browser"),
        shutil.which("google-chrome"),
        r"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
        r"C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/usr/bin/google-chrome",
    ) if item and Path(item).exists()), None)
    if not edge:
        raise RuntimeError("Microsoft Edge is not available for PDF generation")

    def text(value: object) -> str:
        return html.escape(str(value)) if value not in (None, "") else "Нет данных"

    rows = [
        ("Полное наименование", party.name), ("ИНН", party.inn), ("ОГРН", party.ogrn),
        ("КПП", party.kpp), ("Статус", party.status), ("Руководитель", party.director),
        ("Должность руководителя", party.manager_position), ("Адрес", party.address),
        ("Дата регистрации", party.registration_date), ("Организационная форма", party.legal_form),
        ("ОКВЭД", party.okved), ("Уставный капитал", party.authorized_capital),
        ("Оценка риска", party.risk_level), ("Факторы риска", "; ".join(party.risk_factors)),
    ]
    body = "".join(f"<tr><th>{text(key)}</th><td>{text(value)}</td></tr>" for key, value in rows)
    document = f"""<!doctype html><html lang=\"ru\"><meta charset=\"utf-8\"><style>
      @page {{ size: A4; margin: 18mm; }} body {{ font-family: Arial, sans-serif; color:#171717; font-size:11pt; }}
      h1 {{ font-size:21pt; margin:0 0 6px }} .meta {{ color:#666; margin-bottom:24px }}
      table {{ border-collapse:collapse; width:100% }} th,td {{ border-bottom:1px solid #ddd; padding:9px 6px; text-align:left; vertical-align:top }}
      th {{ color:#666; width:35%; font-weight:normal }} footer {{ margin-top:24px; color:#777; font-size:9pt }}
    </style><body><h1>Выписка по контрагенту</h1><div class=\"meta\">Smart Retail · данные DaData / ЕГРЮЛ · ИНН {text(party.inn)}</div><table>{body}</table><footer>Документ сформирован автоматически. Сведения носят информационный характер.</footer></body></html>"""
    with tempfile.TemporaryDirectory(prefix="smart-retail-") as directory:
        source = Path(directory) / "extract.html"
        target = Path(directory) / "extract.pdf"
        source.write_text(document, encoding="utf-8")
        subprocess.run([edge, "--headless", "--disable-gpu", f"--print-to-pdf={target}", source.as_uri()], check=True, timeout=30, capture_output=True)
        return target.read_bytes()
