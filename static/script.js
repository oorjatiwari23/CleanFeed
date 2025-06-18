function analyzeImage(image) {
    alert(`Analyzing image: ${image}\nResult: Inappropriate content detected.`);
}

function analyzeText(text) {
    const offensiveWords = ['badword1', 'badword2', 'offensive'];
    const found = offensiveWords.some(word => text.toLowerCase().includes(word));
    
    if (found) {
        alert(`Offensive content detected in text:\n${text}`);
    } else {
        alert(`No offensive content found in text:\n${text}`);
    }
}

function showImageModeration() {
    const image = prompt("Please upload an image (URL or file path):");
    if (image) analyzeImage(image);
}

function showTextModeration() {
    const text = prompt("Enter text for analysis:");

    if (text) {
        fetch("http://localhost:50611/moderate", { 
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }

            document.getElementById("output").style.display = "block";
            document.getElementById("status").innerText = `Status: ${data.status}`;
            document.getElementById("confidence").innerText = `Confidence: ${data.confidence}%`;
            document.getElementById("sentiment").innerText = `Sentiment: ${data.sentiment}`; // NEW LINE

            if (data.status === "Flagged" && data.polite_version) {
                document.getElementById("rephrased").innerText = `Suggested polite version: ${data.polite_version}`;
            } else {
                document.getElementById("rephrased").innerText = "";
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
    }
}

