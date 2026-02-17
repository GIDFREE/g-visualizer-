let recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'he-IL';
        recognition.continuous = true;
        recognition.interimResults = true;

        let accumulatedTranscript = "";
        let isProcessing = false;

        // קוצב זמן שבודק כל 5 שניות אם יש טקסט חדש לעבד
        setInterval(() => {
            if (accumulatedTranscript.trim().length > 10 && !isProcessing) {
                const textToProcess = accumulatedTranscript;
                accumulatedTranscript = ""; // איפוס המצבור
                sendToRender(textToProcess);
            }
        }, 5000); 

        recognition.onresult = (event) => {
            let interimTranscript = "";
            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    accumulatedTranscript += event.results[i][0].transcript + " ";
                } else {
                    interimTranscript += event.results[i][0].transcript;
                }
            }
            liveText.innerText = accumulatedTranscript + interimTranscript;
        };

        async function sendToRender(text) {
            isProcessing = true;
            status.innerText = "מנתח מקטע טקסט...";
            try {
                const response = await fetch('https://g-visualizer-app.onrender.com/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: text })
                });
                const data = await response.json();
                if (data.image_url) {
                    outputImg.src = data.image_url;
                    outputImg.style.display = 'block';
                    placeholder.style.display = 'none';
                    status.innerText = "איור עודכן אוטומטית";
                }
            } catch (err) {
                console.error("Error:", err);
            }
            isProcessing = false;
        }
