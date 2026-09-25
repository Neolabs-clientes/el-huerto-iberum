/* El Huerto Iberum: menú móvil, cabecera al hacer scroll y aparición suave de los bloques */
(function () {
  'use strict';

  var cabecera = document.getElementById('cabecera');
  var boton = document.getElementById('hamburguesa');
  var menu = document.getElementById('menu');

  // Menú móvil
  if (boton && menu) {
    boton.addEventListener('click', function () {
      var abierto = menu.classList.toggle('abierto');
      boton.classList.toggle('abierto', abierto);
      boton.setAttribute('aria-label', abierto ? 'Cerrar menú' : 'Abrir menú');
      document.body.style.overflow = abierto ? 'hidden' : '';
    });

    menu.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        menu.classList.remove('abierto');
        boton.classList.remove('abierto');
        boton.setAttribute('aria-label', 'Abrir menú');
        document.body.style.overflow = '';
      }
    });
  }

  // Cabecera más sólida cuando la página baja
  if (cabecera) {
    var alScroll = function () {
      cabecera.classList.toggle('solida', window.scrollY > 40);
    };
    alScroll();
    window.addEventListener('scroll', alScroll, { passive: true });
  }

  // Aparición suave al entrar en pantalla
  var piezas = document.querySelectorAll('.bloque > .contenedor > *, .tira-caja > *');
  var anima = window.matchMedia('(prefers-reduced-motion: reduce)').matches === false;

  if (anima && 'IntersectionObserver' in window) {
    piezas.forEach(function (el) { el.classList.add('revela'); });
    var vigilante = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (entrada) {
        if (entrada.isIntersecting) {
          entrada.target.classList.add('visible');
          vigilante.unobserve(entrada.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -60px 0px' });
    piezas.forEach(function (el) { vigilante.observe(el); });
  }
})();
