function openModal(name) {
    const loc = window.currentData.find(l => l.name === name);

    document.getElementById("modal").style.display = "block";
    document.getElementById("modal-title").innerText = loc.name;
    document.getElementById("modal-image").src = "http://127.0.0.1:8000" + loc.image;
    document.getElementById("modal-desc").innerText = loc.description;

    let galleryHTML = "";
    loc.gallery.forEach(img => {
        galleryHTML += `<img src="http://127.0.0.1:8000${img}">`;
    });

    document.getElementById("gallery").innerHTML = galleryHTML;
}