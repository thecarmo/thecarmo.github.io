#!/usr/bin/env python3
"""
Regenera os dois arquivos derivados da configuração:

    contato.vcf          cartão de contato que a pessoa salva no celular
    assets/qr-pagina.svg QR code com o endereço da página (serve para o pôster)

Os valores vêm de assets/config.js — edite lá, rode aqui.

    python3 gerar-assets.py

Requer: segno  (pip install segno). Sem ele, o .vcf ainda é gerado.
"""

import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent


def ler_config() -> dict:
    """Extrai os pares chave: "valor" do objeto window.CONTATO em config.js."""
    fonte = (RAIZ / "assets" / "config.js").read_text(encoding="utf-8")
    corpo = re.search(r"window\.CONTATO\s*=\s*\{(.*?)\n\};", fonte, re.S)
    if not corpo:
        sys.exit("não encontrei window.CONTATO em assets/config.js")
    return dict(re.findall(r'(\w+)\s*:\s*"([^"]*)"', corpo.group(1)))


def formatar_telefone(digitos: str) -> str:
    return "+" + re.sub(r"\D", "", digitos)


def gerar_vcard(cfg: dict) -> str:
    """vCard 3.0 — a versão que iOS e Android leem sem reclamar."""
    linhas = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        "N:Carmo;Rafael Augusto Ferreira do;;Prof.;",
        "FN:Rafael Augusto Ferreira do Carmo",
        "TITLE:Professor Adjunto",
        "ORG:Universidade Federal do Ceará;Instituto UFC Virtual",
        f"EMAIL;TYPE=INTERNET,WORK:{cfg['email']}",
        f"TEL;TYPE=CELL,VOICE:{formatar_telefone(cfg['whatsapp'])}",
        f"TEL;TYPE=WORK,VOICE:{formatar_telefone(cfg['telefone'])}",
        "ADR;TYPE=WORK:;;Av. Mister Hull s/n - Campus do Pici - Bloco 901;Fortaleza;CE;"
        "60455-760;Brasil",
        f"URL:{cfg['url']}",
        f"URL;TYPE=GitHub:{cfg['github']}",
        f"URL;TYPE=Lattes:{cfg['lattes']}",
        f"URL;TYPE=ORCID:{cfg['orcid']}",
        "NOTE:Pesquisa em comunicacao entre a Central de Transplantes e equipes "
        "transplantadoras (projeto MaCaMu). Conhecemo-nos no CBIS 2026.",
        "END:VCARD",
    ]
    # vCard exige CRLF.
    return "\r\n".join(linhas) + "\r\n"


def gerar_qr(cfg: dict) -> bool:
    try:
        import segno
    except ImportError:
        print("! segno não instalado — QR não regenerado (pip install segno)")
        return False

    # nível de correção alto: sobrevive a impressão ruim e a foto torta no congresso
    qr = segno.make(cfg["url"], error="h")
    qr.save(
        RAIZ / "assets" / "qr-pagina.svg",
        scale=8,
        border=2,
        dark="#1a1a1a",
        light=None,          # fundo transparente, funciona em claro e escuro
        svgclass=None,
        lineclass=None,
    )
    return True


def main() -> None:
    cfg = ler_config()

    destino_vcf = RAIZ / "contato.vcf"
    with destino_vcf.open("w", encoding="utf-8", newline="") as arquivo:
        arquivo.write(gerar_vcard(cfg))
    print(f"✓ {destino_vcf.name}")

    if gerar_qr(cfg):
        print(f"✓ assets/qr-pagina.svg  →  {cfg['url']}")


if __name__ == "__main__":
    main()
