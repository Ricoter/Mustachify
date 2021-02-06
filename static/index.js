document.addEventListener("DOMContentLoaded", () => {
    function setPreviewImg(e) {
        const output = document.getElementById("imgpreview")
        output.src = URL.createObjectURL(e.target.files[0]);
        output.onload = function() {
            URL.revokeObjectURL(output.src)
        }
    }
    document.getElementById("imgInp").onchange = setPreviewImg
})