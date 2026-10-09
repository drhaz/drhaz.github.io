// Opens and closes the slide-out site navigation on small screens.
// The drawer is styled by .site-nav and body.exp in _sass; while it is open, the
// full-screen ::before overlay of the menu button catches taps outside the drawer.
(function () {
  var button = document.querySelector(".menu-icon");
  if (!button) return;

  function setOpen(open) {
    document.body.classList.toggle("exp", open);
    button.setAttribute("aria-expanded", open ? "true" : "false");
  }

  button.addEventListener("click", function () {
    setOpen(!document.body.classList.contains("exp"));
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") setOpen(false);
  });
})();
