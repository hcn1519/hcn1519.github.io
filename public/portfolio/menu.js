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
