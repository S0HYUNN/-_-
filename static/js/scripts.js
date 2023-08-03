/*!
* Start Bootstrap - New Age v6.0.7 (https://startbootstrap.com/theme/new-age)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-new-age/blob/master/LICENSE)
*/
//
// Scripts
// 
// function slide(){
//     document.querySelector(".device").style.display = "none";
// }

// document.querySelector("#next").addEventListener('click', slide);

// 현재 노드 뒤의 Element Node를 탐색하는 함수
function setElementNodeNext(node){
	while(node.nodeType !== 1){
		node = node.nextSibling;
	}
	return node;
}
// 현재 노드 앞의 Element Node를 탐색하는 함수
function setElementNodePre(node){
	while(node.nodeType !== 1){
		node = node.previousSibling;
	}
	return node;
}
 
function nodeRotate() {
	
	var list = document.getElementById("list");
	var firstChild = list.firstChild, 
		lastChild = list.lastChild;
 
	function swapNodes(){
 
		// Element 노드 선택
		firstChild = setElementNodeNext(list.firstChild);
		lastChild = setElementNodePre(list.lastChild);
 
		// 마지막 목록을 처음으로 이동하여 목록을 순환시킴
		list.insertBefore(lastChild, firstChild); 
 
		// 첫째 elment node 선택
		firstChild = setElementNodeNext(list.firstChild);
 
		// css 슬라이더 위치 초기화(CSS transition 중단)
		list.className = ""; 
 
		// transitionend 이벤트 리스너 초기화
		list.removeEventListener("transitionend", swapNodes);
 
	}
 
	// 슬라이더 이동 효과(css trasition)를 위란 클래스 지정
	list.className = "animate";
 
	// list 목록의  트랜지션이 끝난 후, 다음 보여줄 목록들의 배치 수행
	list.addEventListener("transitionend", swapNodes);
 
}

var btn = document.getElementById("btn_r");
btn.addEventListener("click", nodeRotate, false);

window.addEventListener('DOMContentLoaded', event => {

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            offset: 74,
        });
    };

    // const buttonNav = document.body.querySelector('#next');
    // if (buttonNav) {
    //     alert('ddd');
    // };
    // var btn = document.querySelector("input");
    // btn.addEventListener("click",updateBtn);
    // function updateBtn(){
    //     alert("dd");
    // }

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