$('#single').on('click', function(ev) {
    const formData = new FormData(document.getElementById('single-form'));
    console.log(ev.target)
    ev.target.disabled = true
    fetch('https://180.176.5.132:5003/single', {
        method: 'POST',
        body: formData
    }).then(response => response.blob())
    .then(imageBlob => {
        // Then create a local URL for that image and print it 
        const imageObjectURL = URL.createObjectURL(imageBlob);
        console.log(imageObjectURL);
        document.querySelector("#result").src = imageObjectURL;
        ev.target.disabled = false
    }).catch(error => {
        $('#error')[0].innerHTML = 'Something went wrong: ' + error + '.'
        console.error('There was an error!', error);
        ev.target.disabled = false
    });
})

$('#grid').on('click', function(ev) {
    const formData = new FormData(document.getElementById('grid-form'));
    ev.target.disabled = true
    fetch('https://180.176.5.132:5003/grid', {
        method: 'POST',
        body: formData
    }).then(response => response.blob())
    .then(imageBlob => {
        // Then create a local URL for that image and print it 
        const imageObjectURL = URL.createObjectURL(imageBlob);
        console.log(imageObjectURL);
        document.querySelector("#result").src = imageObjectURL;
        ev.target.disabled = false
    }).catch(error => {
        $('#error')[0].innerHTML = 'Something went wrong: ' + error + '.'
        console.error('There was an error!', error);
        ev.target.disabled = false
    });

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

 