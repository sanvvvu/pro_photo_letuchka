let current = "";
let original = "";

function safe(){
    if(!current){
        alert("Сначала загрузите изображение");
        return false;
    }

    return true;
}


async function upload(){

    let file =
        document.getElementById("file").files[0];

    if(!file){
        alert("Выберите файл");
        return;
    }

    let fd = new FormData();

    fd.append("file", file);

    let res = await fetch("/upload",{
        method:"POST",
        body:fd
    });

    let data = await res.json();

    current = data.filename;

    original = data.filename;

    document.getElementById("preview").innerHTML =
        `<img class="main-image"
        src="/image/${current}?v=${Date.now()}">`;
}


async function process(action){

    if(!safe()) return;

    let fd = new FormData();

    fd.append("filename", current);

    fd.append("action", action);

    let res = await fetch("/process",{
        method:"POST",
        body:fd
    });

    let data = await res.json();

    current = data.file;

    document.getElementById("preview").innerHTML =
        `<img class="main-image"
        src="/image/${current}?v=${Date.now()}">`;
}


async function resetImage(){

    current = original;

    document.getElementById("preview").innerHTML =
        `<img class="main-image"
        src="/image/${current}?v=${Date.now()}">`;
}

async function loadExif(){
    let res = await fetch(`/exif?filename=${current}`);
    let data = await res.json();

    let html = `
    <tr>
        <th>Группа</th>
        <th>Тег</th>
        <th>Значение</th>
    </tr>`;

    for(let group in data){
        for(let tag in data[group]){
            html += `
            <tr>
                <td>${group}</td>
                <td>${tag}</td>
                <td>${data[group][tag]}</td>
            </tr>`;
        }
    }

    document.getElementById("exifTable").innerHTML = html;
}
function showHelp(type){
    const help = {
        exif: "EXIF — это метаданные фото: камера, дата, GPS, автор.",
        stego: "Стеганография скрывает текст/файлы внутри изображения.",
        analyze: "Анализ проверяет, редактировалось ли изображение с помощью ML.",
        compare: "Сравнение показывает разницу между двумя изображениями."
    };

    alert(help[type]);
}