function logout() {
  document.cookie = "token=;";
}

setTimeout(function () {
  let flashItem = document.getElementById("flashes");
  flashItem.style.display = "none";
}, 2000);
