/*!
* Start Bootstrap - New Age v6.0.7 (https://startbootstrap.com/theme/new-age)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-new-age/blob/master/LICENSE)
*/
//
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            offset: 74,
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

});

let slideWrap = $(".slide_wrap"),
slideShow = slideWrap.find(".slide_show"),
slideList = slideShow.find(".slide_list"),
slides = slideList.find(".slide"),
slideBtn = slideWrap.find(".slide_btn");

let slideCount = slides.length,
slideWidth = slides.innerWidth(),
showNum = 3,
num = 0,
currentIndex = 0,

slideCopy = $(".slide:lt("+ showNum +")").clone();
slideList.append(slideCopy);

//이미지 움직이기
function backShow(){
if( num == 0 ){
//시작
num= slideCount;
slideList.css("left", -num * slideWidth + "px");
}
num--;
slideList.stop().animate({ left : -slideWidth * num +"px"}, 400);
}

function nextShow(){
if( num == slideCount ){
//마지막
num= 0;
slideList.css("left", num);
}
num++;
slideList.stop().animate({ left : -slideWidth * num +"px"}, 400);
}

//왼쪽, 오른쪽 버튼 설정
slideBtn.on("click","button",function(){
if( $(this).hasClass("prev")){
//왼쪽 버튼을 클릭
backShow();
} else {
//오른쪽 버튼을 클릭
nextShow();
}
});
