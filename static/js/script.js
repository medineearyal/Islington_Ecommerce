const swiper = new Swiper('.swiper', {
  // Optional parameters
  direction: 'horizontal',
  loop: false,
  slidesPerView: 6,

  // If we need pagination
  pagination: {
    el: '.swiper-pagination',
  },

  // Navigation arrows
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },
});

window.addEventListener("DOMContentLoaded", function (){
  const copyrightDate = document.querySelector(".copyright-date");
  if (copyrightDate) {
    copyrightDate.innerHTML = new Date().getFullYear();
  }else{
    copyrightDate.innerHTML = "2025";
  }
});