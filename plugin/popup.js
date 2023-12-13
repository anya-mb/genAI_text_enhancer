function setupTextProcessingButton(buttonId, apiUrl, operationType) {
    document.getElementById(buttonId).addEventListener("click", function () {
        chrome.tabs.executeScript({
            code: 'window.getSelection().toString();'
        }, async function (selection) {
            const selectedText = selection[0];

            // Call the API service
            const response = await fetch(apiUrl, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text: selectedText, 'operation': operationType })
            });

            const data = await response.json();
            const processedText = data.text;

            // Insert processed text
            chrome.tabs.executeScript({
                code: `document.execCommand('insertText', false, "${processedText.replace(/"/g, '\\"')}");`
            });
        });
    });
}


// Check if event listeners have already been added
if (!window.hasEventListenersAdded) {
    document.addEventListener("DOMContentLoaded", function () {

        setupTextProcessingButton("reverseText",
                                  "https://bcnhtyp368.execute-api.us-east-1.amazonaws.com/reverse",
                                  "reverse");

        setupTextProcessingButton("summarizeText",
                                  "https://bcnhtyp368.execute-api.us-east-1.amazonaws.com/summarize",
                                  "summarize");
    });

    window.hasEventListenersAdded = true;
}
