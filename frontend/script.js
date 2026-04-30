let current = "";

function safe(){
    if(!current){
        alert("Сначала загрузите изображение");
        return false;
    }
    return true;
}

async function upload(){
    let file = document.getElementById("file").files[0];

    let fd = new FormData();
    fd.append("file", file);

    let res = await fetch("/upload",{method:"POST",body:fd});
    let data = await res.json();

    current = data.filename;

    document.getElementById("preview").innerHTML =
        `<img src="/image/${current}?t=${Date.now()}">`;
}


async function process(action){
    let fd = new FormData();
    fd.append("filename", current);
    fd.append("action", action);

    let res = await fetch("/process",{method:"POST",body:fd});
    let data = await res.json();

    current = data.file;

    document.getElementById("preview").innerHTML =
        `<img src="/image/${current}?t=${Date.now()}">`;
}


async function loadExif(){
    let res = await fetch(`/exif?filename=${current}`);
    let data = await res.json();

    let table = "<tr><th>IFD</th><th>TAG</th><th>VALUE</th></tr>";

    for(let ifd in data){
        for(let tag in data[ifd]){
            table += `<tr><td>${ifd}</td><td>${tag}</td><td>${data[ifd][tag]}</td></tr>`;
        }
    }

    document.getElementById("exifTable").innerHTML = table;
}


async function editExif(){
    let fd = new FormData();
    fd.append("filename", current);
    fd.append("tag", document.getElementById("tag").value);
    fd.append("value", document.getElementById("value").value);

    await fetch("/exif/edit",{method:"POST",body:fd});

    alert("EXIF обновлён");
}


async function embed(){
    let file = document.getElementById("secretFile").files[0];

    let fd = new FormData();
    fd.append("file", file);
    fd.append("filename", current);

    let res = await fetch("/stego/embed",{method:"POST",body:fd});
    let data = await res.json();

    document.getElementById("stegoPreview").innerText =
        "Скрыто: " + file.name;
}


async function extract(){
    let fd = new FormData();
    fd.append("filename", current);

    let res = await fetch("/stego/extract",{method:"POST",body:fd});
    let data = await res.json();

    alert("Извлечено: " + data.text);
}


async function compare(){
    let f1 = document.getElementById("file").files[0];
    let f2 = document.getElementById("file2").files[0];

    let fd = new FormData();
    fd.append("file1", f1);
    fd.append("file2", f2);

    let res = await fetch("/compare",{method:"POST",body:fd});
    let data = await res.json();

    alert("Разница: " + data.difference_score);
}


async function analyze(){
    let fd = new FormData();
    fd.append("filename", current);

    let res = await fetch("/analyze",{method:"POST",body:fd});
    let data = await res.json();

    document.getElementById("out").innerText =
        data.result + "\n" + data.explanation;

    document.getElementById("heatmap").src = data.heatmap;
}


function reset(){
    location.reload();
}