document.addEventListener("DOMContentLoaded", () => { 
    "use strict"
    
    const fileInput = document.getElementById("video")
    const handleButton = document.getElementById("handling")
    const videoResult = document.getElementById("result")

    fileInput.addEventListener("change", () => handleButton.disabled = false)
    
    handleButton.addEventListener("click", () => {
        const formData = new FormData()
        formData.append('file', fileInput.files[0])

        fetch("/upload", {
            method: "POST",
            body: formData
        }).then( res => {
            window.location = res
        })
    })
})