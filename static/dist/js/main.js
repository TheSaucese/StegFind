$(document).ready(function () {
    $('#drop-area').on('dragover', function (e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).addClass('dragging');
    });

    $('#drop-area').on('dragleave', function (e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).removeClass('dragging');
    });

    $('#drop-area').on('drop', function (e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).removeClass('dragging');
        $(this).hide();
        $('#output-area').show();

        let files = e.originalEvent.dataTransfer.files;
        uploadFiles(files);

    });

    function uploadFiles(files) {
        let formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            formData.append('file', files[i]);
        }

        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                if (response.exifOutput) {
                    $("#EXIF-output").text(response.exifOutput);
                } else {
                    $("#EXIF-output").text("No EXIF data found.");
                }
                if (response.contentOutput) {
                    $("#Content-output").text(response.contentOutput);
                    updateContentOutput(document.getElementById("Content-output").innerText);
                } else {
                    $("#Content-output").text("No Hex data found.");
                }
                if (response.stringOutput) {
                    $("#String-output").text(response.stringOutput);
                } else {
                    $("#String-output").text("No String data found.");
                }
                if (response.img_data) {
                    $("#img-upload").attr("src", response.img_data);
                } else {
                    $("#img-upload").hide();
                }
               
            }
        });
    }
});

function openTab(evt, tabName) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
        tablinks[i].classList.remove("bg-red-500");
    }

    evt.currentTarget.classList.add("bg-red-500");

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

function updateContentOutput(content) {
    // Replace each "| " with "\n"
    content = content.replace(/\| /g, "\n");

    // Set the modified content
    document.getElementById("Content-output").innerText = content;
}