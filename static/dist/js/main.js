var currentThemeSetting = 'dark';
var embedfile;
var img;

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

    $('#drop-area').on('click', function () {
        $('#file-input').trigger('click'); 
    });

    $('#file-input').on('change', function () {
        const file = this.files[0];
        if (file) {
            $('#drop-area').removeClass('dragging');
            $('#drop-area').hide();
            $('#loading').show();
            uploadFiles(file);
        }
    });

    $('#drop-area').on('drop', function (e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).removeClass('dragging');
        $(this).hide();

        $('#loading').show();

        let file = e.originalEvent.dataTransfer.files;
        uploadFiles(file);

    });

    $('#decrypt-button').on('click', function (e) {
        console.log("decrypting")
        e.preventDefault();
        e.stopPropagation();
        $(this).removeClass('dragging');

        $('#decrypting').show();
        uploadPassphrase();

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
                response.viewOutput ? setImagesSrc(response.viewOutput) : $("#ViewButton").hide();
                response.exifOutput ? updateExifOutpput(response.exifOutput) : $("#ExifButton").hide();
                response.contentOutput ? updateContentOutput(response.contentOutput) : $("HexDumpButton#").hide();
                response.stringOutput ? $("#String-output").text(response.stringOutput) : $("#StringButton").hide();
                response.lsbOutput ? $("#LSB-output").text(response.lsbOutput) : $("#LsbButton").hide();
                response.img_data ? $("#img-upload").attr("src", response.img_data) : $("#SpectroButton").hide();
                response.embedOutput ? ($("#Embed-output").text(response.embedOutput), embedfile=response.embedOutput) : $("#EmbedButton").hide();
                response.file_path ? ($("#myImage").attr("src", response.file_path),img=response.file_path) : $("#myImage").hide();
                $('#output-area').show().css('display', 'flex');
                $('#loading').hide();
            }
        });
    }
    function uploadPassphrase() {
        var passphrase = document.getElementById('pass').value;
        var formData = new FormData();
        formData.append('pass', passphrase);
        formData.append('img', img);
        $.ajax({
            url: '/passphrase',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                if(response.fileUrl) {
                    window.location.href = response.fileUrl; 
                    $('#result').text('Found something !');
                }
                else {
                    console.log(response.error)
                    $('#result').text(response.error);
                }
                $('#result').show(); 
                
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    }
});

function setImagesSrc(view_data) {
    // Get all img elements in the div with id 'Output'
    const images = document.querySelectorAll('#Output img');

    // Define the names of the images
    const imageNames = ['image_rgb', 'image_r', 'image_g', 'image_b', 'image_a'];

    // Loop through each img element
    images.forEach((img, index) => {
        // Calculate the image type and variation
        const imageTypeIndex = Math.floor(index / 8);
        const variation = index % 8 + 1;

        // Set the src attribute to the corresponding image file in the 'view_data' folder
        img.src = `${view_data}/${imageNames[imageTypeIndex]}_${variation}.png`; // Assuming the images are .png format
    });
}



const toggleMode = (event) => {
    const newTheme = currentThemeSetting === "dark" ? "light" : "dark";
    const button = event.target;

    // update the button text
    const newCta = newTheme === "light" ? "Dark Theme" : "Light Theme";
    button.innerText = newCta;  

    // use an aria-label if you are omitting text on the button
    // and using sun/moon icons, for example
    button.setAttribute("aria-label", newCta);

    // update theme attribute on HTML to switch theme in CSS
    document.querySelector("html").setAttribute("data-theme", newTheme);

    // update in local storage
    localStorage.setItem("theme", newTheme);

    // update the currentThemeSetting in memory
    currentThemeSetting = newTheme;
}

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
        tablinks[i].classList.remove("selected");
    }

    evt.currentTarget.classList.add("selected");

    // Show the current tab, and add an "active" class to the button that opened the tab
    if(tabName==="Output") {
    document.getElementById(tabName).style.display = "grid";
    }
    else if(tabName==="Files") {
        document.getElementById(tabName).style.display = "flex"
    }
    else {
    document.getElementById(tabName).style.display = "block"
    }
    evt.currentTarget.className += " active";
}

const updateContentOutput = (data) => {
    document.getElementById("Content-output").innerText = data;
}

const updateExifOutpput = (data) => {
    newdata = data.replace( new RegExp( "/n", "g" ),"<br>");
    document.getElementById("EXIF-output").innerHTML = newdata;
}