document.addEventListener("DOMContentLoaded", () => {
  function setPreviewImg(e) {
    const output = document.getElementById("imgpreview");
    output.src = URL.createObjectURL(e.target.files[0]);
    output.onload = function () {
      URL.revokeObjectURL(output.src);
    };
  }
  document.getElementById("img-inp").onchange = setPreviewImg;

  function validateResponse(response) {
    if (!response.ok) {
      throw Error(response.statusText);
    }
    return response;
  }

  function ajaxSubmission(e) {
    e.preventDefault();
    const form = e.target;
    const url = form.action;

    fetch(url, { method: "POST", body: new FormData(form) })
      .then(validateResponse)
      .then((response) => response.blob())
      .then((blob) => {
        const output = document.getElementById("imgpreview");
        output.src = URL.createObjectURL(blob);
        output.onload = function () {
          URL.revokeObjectURL(output.src);
        };
      });
  }
  document.getElementById("file-form").onsubmit = ajaxSubmission;
});
