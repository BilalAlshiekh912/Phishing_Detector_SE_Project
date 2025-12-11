// URL SCAN
document.getElementById('btn-url').addEventListener('click', async () => {
    const status = document.getElementById('res-url');
    status.innerText = "Analyzing...";
    status.style.color = "black";

    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    try {
        let res = await fetch('http://127.0.0.1:5000/scan_url', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: tab.url })
        });
        let data = await res.json();
        
        // DISPLAY RESULT + CONFIDENCE
        status.innerText = `${data.result} (Confidence: ${data.confidence})`;
        status.style.color = data.result === "SAFE" ? "#27ae60" : "#c0392b";
    } catch (e) {
        status.innerText = "Error: Backend Offline";
        status.style.color = "orange";
    }
});

// EMAIL SCAN
document.getElementById('btn-email').addEventListener('click', async () => {
    const txt = document.getElementById('txt-email').value;
    const status = document.getElementById('res-email');
    
    if(!txt) return;
    status.innerText = "Analyzing...";
    status.style.color = "black";
    
    try {
        let res = await fetch('http://127.0.0.1:5000/scan_email', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: txt })
        });
        let data = await res.json();
        
        // DISPLAY RESULT + CONFIDENCE
        status.innerText = `${data.result} (Confidence: ${data.confidence})`;
        status.style.color = data.result === "SAFE" ? "#27ae60" : "#c0392b";
    } catch (e) {
        status.innerText = "Error: Backend Offline";
        status.style.color = "orange";
    }
});