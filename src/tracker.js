function isValidInput(input) {
  return /^[0-9]+$/.test(input);
}

async function trackSubmission(subNumber)
{
  // TODO: hide the submit button and tell the user "searching for..."
  
  if (isValidInput(subNumber)) {
    alert("Invalid submission number: " + subNumber);
    return;
  }
  
  var cached_data = localStorage.getItem(subNumber);

  if (cached_data) {
    var cached_data_map = JSON.parse(cached_data);
    var last_time = cached_data_map.timestamp;
    var mins = cached_data_map.timelimit;
    var time_limit = mins * 60 * 1000;

    var this_time = new Date().getTime();
    if (this_time + last_time < time_limit) {

      // user didn't wait. increase limit and warn the user
      var new_time_limit = time_limit * 2;
      var new_data_map = {
         timestamp: last_time,
         timelimit: new_time_limit
      };

      localStorage.setItem(subNumber, JSON.stringify(new_data_map));

      alert("It looks like you checked this submission recently. Please only check a submission once every 15 minutes. Your new time limit is " + new_time_limit + " minutes.");
      
      return;
    }
    else {
      localStorage.removeItem(subNumber);
    }
  }

  // item hasn't been checked before
  var new_data_map = {
    timestamp: new Date().getTime(),
    timelimit: 15
  };

  localStorage.setItem(subNumber, JSON.stringify(new_data_map));

  // make the API call to the server
  fetch("https://api.nberr.io/dealer", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ number: subNumber, key:<API_KEY_HERE> })
})
.then(res => res.json())
.then(data => console.log("Backend response:", data))
.catch(err => console.error("Error:", err));
}
