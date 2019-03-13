document.addEventListener("DOMContentLoaded", () => { 
    "use strict"
    
    const fileInput = document.getElementById("video")
    const handleButton = document.getElementById("handling")
    const videoResult = document.getElementById("result")

    fileInput.addEventListener("change", () => handleButton.disabled = false)
    
    handleButton.addEventListener("click", () => {
        const formData = new FormData()
        formData.append('file', fileInput.files[0])
        const start = async function(){
            const result = await fetch("/upload", {
                method: "POST",
                body: formData
            })
            const v1 = await result.json()
            location.href = v1.target
        }

        start()
    })
})