///*** */
// Fetch trending topics
async function loadTrends() {
    let res = await fetch("http://127.0.0.1:5000/api/trends");
    let data = await res.json();
    let list = document.getElementById("trendList");
    list.innerHTML = "";
    data.trends.forEach(t => {
        let li = document.createElement("li");
        li.textContent = `${t.topic} (from ${t.platform})`;
        list.appendChild(li);
    });
}

// Generate meme caption
async function generateMeme() {
    let topic = document.getElementById("topicInput").value;
    let res = await fetch("http://127.0.0.1:5000/api/generate-meme", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({topic: topic})
    });
    let data = await res.json();
    document.getElementById("memeResult").innerText = data.caption;
}

async function displaymeme(){
    document.getElementById("postForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const text = document.getElementById("postText").value;
  const time = document.getElementById("postTime").value;

  try {
    const res = await fetch("http://127.0.0.1:5000/api/schedule", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, time })
    });

    const data = await res.json();
    document.getElementById("responseMsg").innerText = data.message;
  } catch (err) {
    document.getElementById("responseMsg").innerText = "Error connecting to backend!";
    console.error(err);
  }
})};


function playMemeAudio(memeId) {
    const audio = document.getElementById(memeId);
    if (audio) {
        audio.currentTime = 0; // restart if already playing
        audio.play();
    }
}

// Run on page load
window.onload = loadTrends;
window.onload= generateMeme;
window.onload= displaymeme;