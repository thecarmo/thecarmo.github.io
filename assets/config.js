/* ---------------------------------------------------------------------------
   ÚNICO ARQUIVO QUE VOCÊ PRECISA EDITAR.

   Depois de mudar qualquer valor aqui, rode:   python3 gerar-assets.py
   (regenera contato.vcf e o QR code a partir destes mesmos dados)
--------------------------------------------------------------------------- */
window.CONTATO = {
  // Endereço final da página. É o que vai dentro do QR code do pôster.
  url: "https://rafael.carmo.cc/",

  // WhatsApp: só dígitos, com código do país (55) e DDD.
  whatsapp: "5585981089287",

  // Mensagem que já vem digitada quando a pessoa abre a conversa.
  mensagem: "Olá, Rafael! Nos conhecemos no CBIS 2026.",

  email: "carmorafael@virtual.ufc.br",
  assuntoEmail: "Contato — CBIS 2026",

  github: "https://github.com/thecarmo",
  lattes: "http://lattes.cnpq.br/3102406452063651",
  orcid: "https://orcid.org/0000-0002-5080-1688",
  telefone: "+558533669465"
};

/* --------------------------------------------------------------------------
   Daqui para baixo não precisa mexer: preenche os links da página.
-------------------------------------------------------------------------- */
(function () {
  var c = window.CONTATO;
  var wa = "https://wa.me/" + c.whatsapp + "?text=" + encodeURIComponent(c.mensagem);
  var mail = "mailto:" + c.email + "?subject=" + encodeURIComponent(c.assuntoEmail);

  function aplicar(raiz) {
    var mapa = {
      wa: wa,
      email: mail,
      github: c.github,
      lattes: c.lattes,
      orcid: c.orcid,
      tel: "tel:" + c.telefone
    };
    raiz.querySelectorAll("[data-link]").forEach(function (a) {
      var destino = mapa[a.dataset.link];
      if (destino) a.setAttribute("href", destino);
    });
    raiz.querySelectorAll("[data-texto]").forEach(function (el) {
      var valores = {
        email: c.email,
        telefone: c.telefone.replace(/^\+55(\d{2})(\d{4})(\d{4})$/, "($1) $2-$3"),
        whatsapp: c.whatsapp.replace(/^55(\d{2})(\d{5})(\d{4})$/, "($1) $2-$3"),
        url: c.url.replace(/^https?:\/\//, "")
      };
      if (valores[el.dataset.texto]) el.textContent = valores[el.dataset.texto];
    });
  }

  document.addEventListener("DOMContentLoaded", function () { aplicar(document); });
  // As parciais carregadas por htmx também têm links: reaplica após cada troca.
  document.addEventListener("htmx:afterSwap", function (e) { aplicar(e.target); });
})();
