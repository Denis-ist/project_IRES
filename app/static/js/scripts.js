const anchors = document.querySelectorAll('a[href*="#"]')

for (let anchor of anchors) {
  anchor.addEventListener('click', function (e) {
    e.preventDefault()

    const blockID = anchor.getAttribute('href').substr(1)

    document.getElementById(blockID).scrollIntoView({
      behavior: 'smooth',
      block: 'start'
    })
  })
}

let reg = document.querySelector('.register');
let auth = document.querySelector('.auth');
let button_account = document.querySelector('#button_account');
let label = 'd-none'
function change(){
    if (reg.classList.contains('d-none')){
    reg.classList.remove('d-none')
    auth.classList.add('d-none')
    button_account.innerText = 'Есть аккаунт?'
    }else{
    reg.classList.add('d-none')
    auth.classList.remove('d-none')
    button_account.innerText = 'Нет аккаунта?'
    }
}

$(document).ready(function(){
  $(".owl-carousel").owlCarousel();
});
var owl = $('.owl-carousel');
owl.owlCarousel({
    items:1,
    loop:true,
    margin:10,
    autoplay:true,
    autoplayTimeout:5000,
    autoplayHoverPause:true,

});