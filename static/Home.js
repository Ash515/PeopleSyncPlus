function display_c() {
  var refresh = 1000; // Refresh rate in milli seconds
  mytime = setTimeout("display_ct()", refresh);
}

function display_ct() {
  var x = new Date();
  //var x1=x.getMonth() + 1+ "/" + x.getDate() + "/" + x.getFullYear();

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


// var inputField = document.getElementById("notes");
// console.log(inputField)

// inputField.addEventListener("input", (event) => {
//   const value = event.target.value;
//   localStorage.setItem("myInputFieldValue", value);
// });

// const savedValue = localStorage.getItem("myInputFieldValue");
// if (savedValue) {
//   inputField.value = savedValue;
// }




// localStorage.setItem('my-input-value', document.getElementById('day-note'));

  
//   const savedInputValue = localStorage.getItem('my-input-value');
//   if (savedInputValue) {
//     inputField.value = savedInputValue;
//   }


  document.addEventListener("DOMContentLoaded", function() {
    var myForm = document.getElementById("day-note");
    myForm.addEventListener("keydown", function(e) {
        if (e.keyCode === 13) {  // 13 is the "Enter" key code
            e.preventDefault();  // prevent default form submission
            myForm.submit();  // submit the form
        }
    });
});