
    /*show recent detection */
$(function(){
    $("tbody").each(function(elem,index){
      var arr = $.makeArray($("tr",this).detach());
      arr.reverse();
        $(this).append(arr);
    });
});
/**/

/*  filter the whole alert table by specific columns */

$(document).ready(function(){
  $("#Det").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    // Filter the entire table based on the "detection" column
    $("#myTable tr").filter(function() {
      // Use $(this).children("td:first-child") to target the first column (index 0) which corresponds to the "Username" column
      $(this).toggle($(this).children("td:nth-child(2)").text().toLowerCase().indexOf(value) > -1);
    });
  });
});


$(document).ready(function(){
  $("#loc").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    // Filter the entire table based on the "location" column
    $("#myTable tr").filter(function() {
      // Use $(this).children("td:first-child") to target the first column (index 0) which corresponds to the "Username" column
      $(this).toggle($(this).children("td:nth-child(3)").text().toLowerCase().indexOf(value) > -1);
    });
  });
});

$(document).ready(function(){
  $("#user_rec").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    // Filter the entire table based on the "Username" column
    $("#myTable tr").filter(function() {
      // Use $(this).children("td:first-child") to target the first column (index 0) which corresponds to the "Username" column
      $(this).toggle($(this).children("td:nth-child(4)").text().toLowerCase().indexOf(value) > -1);
    });
  });
});


/*  filter date */

function filterTable() {
  var startDate = new Date(document.getElementById('start-date').value);
  var endDate = new Date(document.getElementById('end-date').value);
  var table = document.getElementById('Alerts_table');
  var rows = table.getElementsByTagName('tr');

  for (var i = 0; i < rows.length; i++) {
    var cells = rows[i].getElementsByTagName('td');
    if (cells.length > 4) { // Checking if there's a cell in the fifth column (index 4)
      var dateStr = cells[4].textContent || cells[4].innerText;
      var date = new Date(dateStr);

      // Check if the date is valid and falls within the range
      if (!isNaN(date.getTime()) && date >= startDate && date <= endDate) {
        rows[i].style.display = '';
      } else {
        rows[i].style.display = 'none';
      }
    }
  }
}

window.addEventListener('DOMContentLoaded', (event) => {
        const inputs = document.querySelectorAll('.form-control');
        inputs.forEach(input => {
            input.style.width = `${input.getAttribute('placeholder').length + 3}ch`; // Adjusting width based on placeholder length
        });
    });




/*  filter the users whole table */

$(document).ready(function(){
  $("#user_rec").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    // Filter the entire table based on the "Username" column
    $("#myTable2 tr").filter(function() {
      // Use $(this).children("td:first-child") to target the first column (index 0) which corresponds to the "Username" column
      $(this).toggle($(this).children("td:nth-child(1)").text().toLowerCase().indexOf(value) > -1);
    });
  });
});



$(document).ready(function(){
  $("#loc").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    // Filter the entire table based on the "location" column
    $("#myTable2 tr").filter(function() {
      // Use $(this).children("td:first-child") to target the first column (index 0) which corresponds to the "Username" column
      $(this).toggle($(this).children("td:nth-child(2)").text().toLowerCase().indexOf(value) > -1);
    });
  });
});






 // Function to fetch the number of alerts and update the count
 function updateAlertCount() {
  fetch('/get_alert_count')
    .then(response => response.json())
    .then(data => {
      document.getElementById('alertCount').textContent = data.alertCount;
    })
    .catch(error => console.error('Error fetching alert count:', error));
}

// Call updateAlertCount function initially to update the count when the page loads
updateAlertCount();


setInterval(updateAlertCount, 500); // refresh every 1 sec 


