$('#single').on('click', function(ev) {
    console.log('clicked')
    const formData = new FormData(document.getElementById('single-form'));
    console.log(formData)
    fetch('http://180.176.5.132:5002/single', {
        method: 'POST',
        body: formData
    }).then(response => response.blob())
    .then(imageBlob => {
        // Then create a local URL for that image and print it 
        const imageObjectURL = URL.createObjectURL(imageBlob);
        console.log(imageObjectURL);
        document.querySelector("#result").src = imageObjectURL;
    });
})

$('#grid').on('click', function(ev) {
    console.log('clicked')
    const formData = new FormData(document.getElementById('grid-form'));
    fetch('http://180.176.5.132:5002/grid', {
        method: 'POST',
        body: formData
    }).then(response => response.blob())
    .then(imageBlob => {
        // Then create a local URL for that image and print it 
        const imageObjectURL = URL.createObjectURL(imageBlob);
        console.log(imageObjectURL);
        document.querySelector("#result").src = imageObjectURL;
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