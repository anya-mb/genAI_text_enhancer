document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("reverseText").addEventListener("click", function() {
    console.log("Hello")
        chrome.tabs.executeScript({
            code: `
            var selectedText = window.getSelection().toString();
            var reversedText = selectedText.split('').reverse().join('');
            document.execCommand('insertText', false, reversedText);
            `
        });
    });
});