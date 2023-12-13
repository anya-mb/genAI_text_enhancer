// Check if event listeners have already been added
if (!window.hasEventListenersAdded) {
    document.addEventListener("DOMContentLoaded", function () {
        // Event listener for reverseText button
        document.getElementById("reverseText").addEventListener("click", function () {
            chrome.tabs.executeScript({
                code: 'window.getSelection().toString();'
            }, async function (selection) {
                const selectedText = selection[0];

                // Call service to reverse text
                const response = await fetch("https://bcnhtyp368.execute-api.us-east-1.amazonaws.com/reverse", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ text: selectedText, 'operation': 'reverse' })
                });

                const data = await response.json();
                const reversedText = data.text;

                // Insert reversed text
                chrome.tabs.executeScript({
                    code: `document.execCommand('insertText', false, "${reversedText}");`
                });
            });
        });

        // Event listener for summarizeText button
        document.getElementById("summarizeText").addEventListener("click", function () {
            chrome.tabs.executeScript({
                code: 'window.getSelection().toString();'
            }, async function (selection) {
                const selectedText = selection[0];

                // Call service to summarize text
                const response = await fetch("https://bcnhtyp368.execute-api.us-east-1.amazonaws.com/summarize", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ text: selectedText, 'operation': 'summarize' })
                });

                const data = await response.json();
                const summarizedText = data.text;

                // Insert summarized text
                chrome.tabs.executeScript({
                    code: `document.execCommand('insertText', false, "${summarizedText}");`
                });
            });
        });
    });

    window.hasEventListenersAdded = true;
}
