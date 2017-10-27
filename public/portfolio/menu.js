// click
function selectMenu(i) {
  switch (i) {
    case 1:
      document.getElementById("menu1").classList.add("selected");
      document.getElementById("menu2").classList.remove("selected");
      document.getElementById("menu3").classList.remove("selected");
      break;
    case 2:
    document.getElementById("menu2").classList.add("selected");
    document.getElementById("menu1").classList.remove("selected");
    document.getElementById("menu3").classList.remove("selected");
      break;
    default:
    document.getElementById("menu3").classList.add("selected");
    document.getElementById("menu1").classList.remove("selected");
    document.getElementById("menu2").classList.remove("selected");
    break;
  }
}
function toMenu(i) {
  switch (i) {
    case 1:
      location.href = "#title1"
      break;
    case 2:
    location.href = "#title2"
      break;
    default:
    location.href = "#title3"
    break;
  }
}

window.onscroll = function() {
    var menuOffset1 = document.getElementById("menu1").offsetTop
    var menuOffset2 = document.getElementById("menu2").offsetTop
    var menuOffset3 = document.getElementById("menu3").offsetTop

    if (window.pageYOffset <= 680) {
      selectMenu(1);
    } else if (window.pageYOffset > 680 && window.pageYOffset < 3500) {
      selectMenu(2);
    } else {
      selectMenu(3);
    }
}
