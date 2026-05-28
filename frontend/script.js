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
        alert("Выберите изображение");
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
    `
    <img class="main-image"
    src="/image/${current}?v=${Date.now()}">
    `;
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
    `
    <img class="main-image"
    src="/image/${current}?v=${Date.now()}">
    `;
}

async function resetImage(){

    if(!original){
        alert("Нет исходного изображения");
        return;
    }

    current = original;

    document.getElementById("preview").innerHTML =
    `
    <img class="main-image"
    src="/image/${current}?v=${Date.now()}">
    `;
}

async function loadExif(){

    if(!safe()) return;

    let res = await fetch(
        `/exif?filename=${current}`
    );

    let data = await res.json();

    let html = `
    <tr>
        <th>Категория</th>
        <th>Тег</th>
        <th>Значение</th>
    </tr>
    `;

    for(let group in data){

        for(let tag in data[group]){

            html += `
            <tr>
                <td>${group}</td>
                <td>${tag}</td>
                <td>${data[group][tag]}</td>
            </tr>
            `;
        }
    }

    document.getElementById(
        "exifTable"
    ).innerHTML = html;
}

async function editExif(){

    if(!safe()) return;

    let fd = new FormData();

    fd.append("filename", current);

    fd.append(
        "ifd",
        document.getElementById("ifd").value
    );

    fd.append(
        "tag",
        document.getElementById("tag").value
    );

    fd.append(
        "value",
        document.getElementById("value").value
    );

    let res = await fetch("/exif/edit",{
        method:"POST",
        body:fd
    });

    let data = await res.json();

    current = data.file;

    alert("EXIF обновлён");

    loadExif();

    document.getElementById("preview").innerHTML =
    `
    <img class="main-image"
    src="/image/${current}?v=${Date.now()}">
    `;
}

async function compareImages(){

    let f1 =
        document.getElementById("file").files[0];

    let f2 =
        document.getElementById("file2").files[0];

    if(!f1 || !f2){
        alert("Выберите два изображения");
        return;
    }

    let fd = new FormData();

    fd.append("file1", f1);
    fd.append("file2", f2);

    let res = await fetch("/compare",{
        method:"POST",
        body:fd
    });

    let data = await res.json();

    alert(
        "Разница: "
        + data.difference_score
        + "\n\n"
        + data.interpretation
    );
}

async function analyzeImage(){

    if(!safe()) return;

    let fd = new FormData();

    fd.append("filename", current);

    let res = await fetch("/analyze",{
        method:"POST",
        body:fd
    });

    let data = await res.json();

    document.getElementById("out").innerText =
        "Результат: "
        + data.result
        + "\n\nУверенность: "
        + data.confidence
        + "\n\n"
        + data.explanation
        + "\n\nNoise: "
        + data.noise
        + "\nMean: "
        + data.mean
        + "\nSTD: "
        + data.std
        + "\nDCT Low: "
        + data.dct_low
        + "\nDCT High: "
        + data.dct_high;

    document.getElementById("heatmap").src =
        data.heatmap + "?v=" + Date.now();
}

async function runELA(){

    if(!safe()) return;

    let fd = new FormData();

    fd.append("filename", current);

    let res = await fetch("/ela",{
        method:"POST",
        body:fd
    });

    let data = await res.json();

    document.getElementById("analysisImage").src =
        data.image + "?v=" + Date.now();

    alert(
        "ELA Score: "
        + data.score
        + "\n\n"
        + data.interpretation
    );
}

async function runCMFD(){

    if(!safe()) return;

    let fd = new FormData();

    fd.append("filename", current);

    let res = await fetch("/cmfd",{
        method:"POST",
        body:fd
    });

    let data = await res.json();

    document.getElementById("analysisImage").src =
        data.image + "?v=" + Date.now();

    alert(
        "Совпадений: "
        + data.matches
        + "\n\n"
        + data.interpretation
    );
}

async function runCFA(){

    if(!safe()) return;

    let fd = new FormData();

    fd.append("filename", current);

    let res = await fetch("/cfa",{
        method:"POST",
        body:fd
    });

    let data = await res.json();

    document.getElementById("analysisImage").src =
        data.image + "?v=" + Date.now();

    alert(
        "Variance: "
        + data.variance
        + "\n\n"
        + data.interpretation
    );
}

function showHelp(type){

    const help = {

        exif:
`EXIF — метаданные изображения.

Можно увидеть:
• автора
• дату съёмки
• GPS
• камеру
• разрешение
• ПО обработки
• описание файла`,

        compare:
`Сравнение вычисляет
пиксельную разницу
между двумя изображениями.`,

        analyze:
`ML-анализ использует:

• статистику шума
• variance
• DCT-анализ
• цифровые артефакты

и оценивает вероятность
редактирования.`

    };

    alert(help[type]);
}