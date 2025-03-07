async function getRootPage(){
    window.location.replace(window.location.origin);
}

async function getPage(page){
    window.location.replace(window.location.origin+'/'+page);
}

document.addEventListener("keydown", function(event) {
    console.log("Key Pressed:", event.key); // Debugging log

    if (event.key === "Enter") {
        console.log("Final Input Sequence:", inputSequence); // Debugging log

        if (inputSequence === "7200774E84") {
            console.log("Sequence recognized!");
            getPage("compare")
        } else {
            console.log("Wrong sequence:", inputSequence);
        }

        inputSequence = ""; // Reset sequence after Enter
    } else if (/^[a-zA-Z0-9]$/.test(event.key)) { 
        // Append key only if it's alphanumeric & within limit
        if (inputSequence.length < maxLength) {
            inputSequence += event.key;
        } else {
            console.log("⚠️ Input limit reached (32 chars). Ignoring extra input.");
        }
    }
});

