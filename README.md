# Página pessoal de Rafael Augusto Ferreira do Carmo

Publicada em **[rafael.carmo.cc](https://rafael.carmo.cc/)** pelo GitHub Pages,
a partir da raiz da branch `main` deste repositório. A página reúne contatos,
trajetória, produção e o trabalho sobre o MaCaMu apresentado no CBIS 2026.

HTML estático, navegação por **htmx** e estilo em **Bulma**. Sem etapa de build,
rastreadores ou CDN: as bibliotecas estão em `assets/vendor/`.

## Arquivos

```text
index.html              cabeçalho, abas, rodapé com contatos e QR
parciais/
  poster.html           o trabalho apresentado (aba inicial)
  macamu.html           o projeto e a leitura em dois níveis
  sobre.html            formação e atuação
  producao.html         publicações selecionadas e orientações
assets/
  config.js             endereço, contatos e links
  estilo.css            ajustes sobre o Bulma
  qr-pagina.svg         QR para https://rafael.carmo.cc/
  vendor/               Bulma 1.0.4 e htmx 2.0.4
contato.vcf             cartão de contato
gerar-assets.py         regenera o cartão e o QR a partir de config.js
CNAME                   domínio personalizado do GitHub Pages
.nojekyll               publica os arquivos sem processamento pelo Jekyll
```

## Editar e visualizar

A pasta local está conectada a `https://github.com/thecarmo/thecarmo.github.io.git`
como `origin`, com `main` acompanhando `origin/main`.

```sh
cd ~/Claude/Projects/MaCaMu/pagina-cbis26
git pull --ff-only
python3 -m http.server 8000 --bind 127.0.0.1
```

Abra <http://localhost:8000>. As abas carregam arquivos por HTTP, então abrir
`index.html` com `file://` não funciona.

Os textos de cada seção ficam em `parciais/`. Os contatos e links usados pelo
JavaScript ficam em `assets/config.js`. Ao alterá-los, regenere o cartão e o QR:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install segno
python gerar-assets.py
```

O HTML também contém contatos de fallback para visitantes sem JavaScript;
mantenha esses valores coerentes ao editar os contatos. Se mudar o domínio,
atualize também `CNAME`, a URL canônica, `og:url` e o endereço no rodapé do
`index.html`, além das configurações de Pages e DNS.

## Publicar alterações

Depois de conferir a página localmente:

```sh
git status
git add README.md index.html parciais assets contato.vcf gerar-assets.py CNAME .nojekyll .gitignore .gitattributes
git commit -m "Atualiza página pessoal"
git push origin main
```

O GitHub Pages publica automaticamente os arquivos de `main` na raiz `/`.
O domínio é `rafael.carmo.cc`, com HTTPS obrigatório. No Cloudflare, o subdomínio
`rafael` aponta para `thecarmo.github.io`.

## Navegação

- Cada aba faz uma requisição htmx à parcial correspondente; `?s=poster`,
  `?s=macamu`, `?s=sobre` e `?s=producao` podem ser compartilhados diretamente.
- O histórico usa `pushState` e `popstate` para recarregar a seção ao voltar
  ou avançar, sem depender do cache de histórico do htmx.
- O modo escuro acompanha a preferência do dispositivo.
- Sem JavaScript, nome, cargo, síntese e contatos continuam visíveis; as abas
  dependem de JavaScript.
