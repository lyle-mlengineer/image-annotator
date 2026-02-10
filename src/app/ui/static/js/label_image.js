const promptInput = document.getElementById('promptInput');
const allTags = document.querySelectorAll('.tag')
const genderSelect = document.getElementById('genderSelect')

function saveImage(image_name){
    console.log(image_name)

    if (!promptInput.value) {
        alert("Please enter a prompt")
        return
    }
    console.log(promptInput.value)

    let tags = []
    allTags.forEach(tag => {
        tags.push(tag.innerText)
    })

    console.log(tags)

    console.log(genderSelect.value)

    fetch('http://127.0.0.1:8000/api/v1/images/label', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "image_name": image_name,
            "prompt": promptInput.value,
            "tags": tags,
            "gender": genderSelect.value
        })
    }).then(response => response.json())
    .then(data => {
        console.log(data)
        window.location.href = `/image/label`
    }).catch(error => {
        console.error(error)
    })
}

function addTagModal() {
    document.getElementById("addTag").classList.add("show"); 
}

function closeAddTagModal() {
    document.getElementById("addTag").classList.remove("show"); 
}

function addTag() {
    let tagInput = document.getElementById("tagInput").value;
    const tags = document.querySelectorAll(".tag");
    for (let i = 0; i < tags.length; i++) {
        if (tags[i].innerText.toLowerCase() === tagInput.toLowerCase().JSON) {
            alert("Tag already exists");
            return;
        }
    }
    let newTag = document.createElement("span");
    newTag.classList.add("tag");
    newTag.innerText = tagInput;
    document.getElementById("tags").appendChild(newTag);
    closeAddTagModal();
}