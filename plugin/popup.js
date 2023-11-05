document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("reverseText").addEventListener("click", async function () {
        chrome.tabs.executeScript({
            code: `window.getSelection().toString();`
        }, async function (selection) {
            const selectedText = selection[0];

            // Call service to reverse text
            const response = await fetch("https://bcnhtyp368.execute-api.us-east-1.amazonaws.com/reverse", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ text: selectedText })
            });

            const data = await response.json();

            const reversedText = data.reversed;

            // Insert reversed text
            chrome.tabs.executeScript({
                code: `
                    document.execCommand('insertText', false, "${reversedText}");
                `
            });
        });
    });
});
