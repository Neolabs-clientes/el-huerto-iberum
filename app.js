/* El Huerto Iberum: menú móvil, cabecera al bajar y aparición suave de los bloques.
   Los bloques aparecen al entrar en pantalla, pero con un tope de tiempo: si alguien
   no hace scroll (o la página se captura para una vista previa), todo queda visible. */
(function () {
  'use strict';

  var cabecera = document.getElementById('cabecera');
  var boton = document.getElementById('hamburguesa');
  var menu = document.getElementById('menu');

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

  if (cabecera) {
    var alScroll = function () {
      cabecera.classList.toggle('solida', window.scrollY > 40);
    };
    alScroll();
    window.addEventListener('scroll', alScroll, { passive: true });
  }

  var piezas = document.querySelectorAll('.bloque > .contenedor > *, .tira-caja > *');
  var anima = window.matchMedia('(prefers-reduced-motion: reduce)').matches === false;

  function mostrarTodo() {
    piezas.forEach(function (el) { el.classList.add('visible'); });
  }

  if (anima && 'IntersectionObserver' in window && piezas.length) {
    piezas.forEach(function (el) { el.classList.add('revela'); });

    var vigilante = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (entrada) {
        if (entrada.isIntersecting) {
          entrada.target.classList.add('visible');
          vigilante.unobserve(entrada.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    piezas.forEach(function (el) { vigilante.observe(el); });

    // Red de seguridad: a los 3 segundos se muestra todo lo que quede pendiente,
    // para que nadie se quede con la pagina a medias.
    window.setTimeout(function () {
      piezas.forEach(function (el) {
        if (!el.classList.contains('visible')) {
          el.classList.add('visible');
          vigilante.unobserve(el);
        }
      });
    }, 3000);

    // Si la pestaña se abre en segundo plano, al volver tambien se muestra todo.
    window.addEventListener('pagehide', mostrarTodo);
  }

  // Año del pie, si algun dia se añade
  var anyo = document.getElementById('anyo');
  if (anyo) { anyo.textContent = String(new Date().getFullYear()); }
})();
