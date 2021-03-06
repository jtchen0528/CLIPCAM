SERVER = 'https://180.176.5.132:5003/'

function ajaxSetting(api, data) {
    setting = {
        "async": true,
        "crossDomain": true,
        "url": SERVER + api,
        "method": "POST",
        "headers": {
            "content-type": "application/json",
            "cache-control": "no-cache",
            "postman-token": "e81e0d1c-cde1-b166-2025-1d8726e91517"
        },
        "processData": false,
        "data": JSON.stringify(data)
    }
    return setting
}

window.onload = function ()
{
    const data = 'test';
    $.ajax(ajaxSetting('check-server', data)).done(function(response) {
        if (response.message !== 'server is ok') {
            document.getElementById('server-check-warning').style.display = 'block'
            $('#single')[0].disabled = true;
            $('#grid')[0].disabled = true;
        }
    }).catch(function(error) {
        console.log(error)
        document.getElementById('server-check-warning').style.display = 'block'
        $('#single')[0].disabled = true;
        $('#grid')[0].disabled = true;
    })
}

$('#single').on('click', function(ev) {
    const formData = new FormData(document.getElementById('single-form'));
    console.log(ev.target)
    $('#single')[0].disabled=true
    $.ajax(ajaxSetting('check-using', 'test')).done(function(response) {
        if (response.message === 'currently not in use') {
            fetch(SERVER + 'single', {
                method: 'POST',
                mode: 'cors',
                body: formData
            }).then(response => response.blob())
            .then(imageBlob => {
                // Then create a local URL for that image and print it 
                const imageObjectURL = URL.createObjectURL(imageBlob);
                console.log(imageObjectURL);
                document.querySelector("#result").src = imageObjectURL;
                $('#single')[0].disabled=false
                $('#error')[0].innerHTML = ''
            }).catch(error => {
                $('#error')[0].innerHTML = 'Something went wrong: ' + error + '.'
                console.error('There was an error!', error);
                $('#single')[0].disabled=false
            });
        } else {
            $('#single')[0].disabled=false
            $('#error')[0].innerHTML = 'Someone is running the demo elsewhere. Please wait for a few minutes. (The model is running on a Raspberry Pi, sorry for the inconvenience.)'
        }
    })
})

$('#grid').on('click', function(ev) {
    const formData = new FormData(document.getElementById('grid-form'));
    $('#grid')[0].disabled=true
    $.ajax(ajaxSetting('check-using', 'test')).done(function(response) {
        if (response.message === 'currently not in use') {
            fetch(SERVER + 'grid', {
                method: 'POST',
                mode: 'cors',
                body: formData
            }).then(response => response.blob())
            .then(imageBlob => {
                // Then create a local URL for that image and print it 
                console.log(response)
                const imageObjectURL = URL.createObjectURL(imageBlob);
                console.log(imageObjectURL);
                document.querySelector("#result").src = imageObjectURL;
                $('#grid')[0].disabled=false
                $('#error')[0].innerHTML = ''
            }).catch(error => {
                $('#error')[0].innerHTML = 'Something went wrong: ' + error + '.'
                console.error('There was an error!', error);
                $('#grid')[0].disabled=false
            });
        } else {
            $('#grid')[0].disabled=false
            $('#error')[0].innerHTML = 'Someone is running the demo elsewhere. Please wait for a few minutes. (The model is running on a Raspberry Pi, sorry for the inconvenience.)'
        }
    })
})

$('#grid-toggle').on('click', function(ev) {
    if ($('#grid-toggle')[0].classList.value === 'btn btn-lg btn-secondary') {
        $('#grid-toggle')[0].classList.add('active')
        $('#single-toggle')[0].classList.remove('active')
    } else {
        $('#grid-toggle')[0].classList.remove('active')
        $('#single-toggle')[0].classList.add('active')
    }
})

$('#single-toggle').on('click', function(ev) {
    if ($('#grid-toggle')[0].classList.value === 'btn btn-lg btn-secondary') {
        $('#grid-toggle')[0].classList.remove('active')
        $('#single-toggle')[0].classList.add('active')
    } else {
        $('#grid-toggle')[0].classList.add('active')
        $('#single-toggle')[0].classList.remove('active')
    }
})

function addAlert(content, type) {
    alertID = Date.now()
    clearTimeout(timeout)

    // add an alert to #alertBox
    document.getElementById("alertBox").innerHTML += `
        <div class="alert alert-` + type + ` alert-dismissible fade show JobAdded" role="alert" id="` + alertID + `">
            <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
            ` + content + `
        </div>
    `;

    timeout = setTimeout(() => { $(`.JobAdded`).alert('close') }, 3000);
}

$('#file').on('change',function(){
    //get the file name
    var fileName = $(this).val().replace('C:\\fakepath\\', " ");
    //replace the "Choose a file" label
    $(this).next('.custom-file-label').html(fileName);
})

$('#file1').on('change',function(){
    //get the file name
    var fileName = $(this).val().replace('C:\\fakepath\\', " ");
    //replace the "Choose a file" label
    $(this).next('.custom-file-label').html(fileName);
})

$('#file2').on('change',function(){
    //get the file name
    var fileName = $(this).val().replace('C:\\fakepath\\', " ");
    //replace the "Choose a file" label
    $(this).next('.custom-file-label').html(fileName);
})

$('#file3').on('change',function(){
    //get the file name
    var fileName = $(this).val().replace('C:\\fakepath\\', " ");
    //replace the "Choose a file" label
    $(this).next('.custom-file-label').html(fileName);
})

$('#file4').on('change',function(){
    //get the file name
    var fileName = $(this).val().replace('C:\\fakepath\\', " ");
    //replace the "Choose a file" label
    $(this).next('.custom-file-label').html(fileName);
})

 