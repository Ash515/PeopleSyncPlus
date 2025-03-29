function display_c() {
  var refresh = 1000; // Refresh rate in milli seconds
  mytime = setTimeout("display_ct()", refresh);
}

function display_ct() {
  var x = new Date();
  var ampm = x.getHours() >= 12 ? " PM" : " AM";
  var x1 =
    x.getHours() + ":" + x.getMinutes() + ":" + x.getSeconds() + ":" + ampm;
  hours = x.getHours() % 12;
  hours = hours ? hours : 12;
 
  document.getElementById("ct").innerHTML = x1;
  display_c();
}


var loader = document.getElementById("preloader");

window.addEventListener("load", function () {
  loader.style.display = "none";
});

document.addEventListener("DOMContentLoaded", function() {
    var myForm = document.getElementById("day-note");
    myForm.addEventListener("keydown", function(e) {
        if (e.keyCode === 13) {  // 13 is the "Enter" key code
            e.preventDefault();  // prevent default form submission
            myForm.submit();  // submit the form
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
  fetch("/get_status")
      .then(response => response.json())
      .then(data => {
          const statusText = document.getElementById("status-text");
          statusText.textContent = data.status;
          statusText.style.color = data.color;
      })
      .catch(error => console.error("Error fetching status:", error));
});

function updateStatus(status, color) {
  const statusText = document.getElementById("status-text");
  statusText.textContent = status;
  statusText.style.color = color;

  fetch("/update_status", {
      method: "POST",
      headers: {
          "Content-Type": "application/json"
      },
      body: JSON.stringify({ status, color })
  })
  .then(response => response.json())
  .then(data => console.log(data.message))
  .catch(error => console.error("Error updating status:", error));
}


function filterNames() {
  let input = document.getElementById("search-bar").value.toLowerCase();
  let listItems = document.querySelectorAll(".person");

  listItems.forEach(item => {
      let name = item.querySelector(".newhires-name").textContent.toLowerCase();
      if (name.includes(input)) {
          item.style.display = "flex"; 
      } else {
          item.style.display = "none";
      }
  });
}