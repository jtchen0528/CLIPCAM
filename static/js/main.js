$('#single').on('click', function(ev) {
    console.log('clicked')
    const formData = new FormData(document.getElementById('single-form'));
    fetch('/single', {
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
    fetch('/grid', {
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