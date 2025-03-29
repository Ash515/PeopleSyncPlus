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


let timerInterval;
let startTime;


function checkIn() {
    startTime = Date.now();
    localStorage.setItem("checkinTime", startTime);
    updateTimer();
    timerInterval = setInterval(updateTimer, 1000);
}


function checkOut() {
    clearInterval(timerInterval);
    localStorage.removeItem("checkinTime");
    document.getElementById("timer").textContent = "00:00:00";
}


function updateTimer() {
    let checkinTime = localStorage.getItem("checkinTime");
    if (!checkinTime) return;

    let elapsed = Date.now() - parseInt(checkinTime);
    let hours = Math.floor(elapsed / (1000 * 60 * 60));
    let minutes = Math.floor((elapsed % (1000 * 60 * 60)) / (1000 * 60));
    let seconds = Math.floor((elapsed % (1000 * 60)) / 1000);

    document.getElementById("timer").textContent =
        String(hours).padStart(2, "0") + ":" +
        String(minutes).padStart(2, "0") + ":" +
        String(seconds).padStart(2, "0");
}


document.addEventListener("DOMContentLoaded", function () {
    if (localStorage.getItem("checkinTime")) {
        updateTimer();
        timerInterval = setInterval(updateTimer, 1000);
    }
});


// 📅 Function to Display Current Date in "Thursday 23, 2025" Format
function displayDate() {
  const dateElement = document.getElementById("current-date");
  const options = { weekday: 'long', day: 'numeric', year: 'numeric' };
  const today = new Date();
  
  // Formatting the date as "Thursday 23, 2025"
  const formattedDate = today.toLocaleDateString('en-US', options);
  const [weekday, day, year] = formattedDate.split(" ");
  
  dateElement.textContent = `${weekday} ${day}, ${year}`;
}


async function fetchQuote() {
  const quoteElement = document.getElementById("productivity-quote");

  try {
      const response = await fetch("https://api.quotable.io/random?tags=productivity");
      const data = await response.json();
      
      // Display the fetched quote
      quoteElement.textContent = `"${data.content}" - ${data.author}`;
  } catch (error) {
      console.error("Error fetching quote:", error);
      quoteElement.textContent = `"Stay focused and never give up!" - Unknown`; // Fallback quote
  }
}

// Run on Page Load
document.addEventListener("DOMContentLoaded", function () {
  displayDate();
  fetchQuote();
});




