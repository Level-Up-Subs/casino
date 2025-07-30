async function trackSubmission(subNumber)
{
  fetch("https://api.nberr.io/dealer", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ number: subNumber, key:<API_KEY_HERE> })
})
.then(res => res.json())
.then(data => console.log("Backend response:", data))
.catch(err => console.error("Error:", err));
}
