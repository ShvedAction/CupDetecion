document.addEventListener("DOMContentLoaded", () => { 
    "use strict"
    
    const fileInput = document.getElementById("video")
    const handleButton = document.getElementById("handling")

    fileInput.addEventListener("change", () => handleButton.disabled = false)
    
    handleButton.addEventListener("click", () => {
        //TODO:
    })
})