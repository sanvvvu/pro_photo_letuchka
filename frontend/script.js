let current = "";

async function upload() {
    let file = document.getElementById("file").files[0];
    let fd = new FormData();
    fd.append("file", file);

    let res = await fetch("/upload", {method:"POST", body:fd});
    let data = await res.json();

    current = data.filename;

    document.getElementById("preview").innerHTML =
        `<img src="/image/${current}">`;
}

async function process(action){
    let res = await fetch(`/process?filename=${current}&action=${action}`,{method:"POST"});
    let blob = await res.blob();
    document.getElementById("preview").innerHTML =
        `<img src="${URL.createObjectURL(blob)}">`;
}

async function getExif(){
    let res = await fetch(`/exif?filename=${current}`);
    let data = await res.json();
    document.getElementById("out").innerText = JSON.stringify(data,null,2);
}

async function editExif(){
    let model = document.getElementById("model").value;

    await fetch("/exif/edit",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({filename:current, model:model})
    });

    alert("EXIF updated");
}

async function embed(){
    let text = document.getElementById("secret").value;

    await fetch("/stego/embed",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({filename:current,text:text})
    });

    alert("Hidden");
}

async function extract(){
    let res = await fetch("/stego/extract",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({filename:current})
    });

    let data = await res.json();
    alert(data.text);
}

function reset(){
    location.reload();
}

async function save(){
    let format = document.getElementById("format").value;
    alert("Сохраняется в формате "+format);
}

async function analyze(){
    let res = await fetch(`/analyze?filename=${current}`,{method:"POST"});
    let data = await res.json();

    let text = `
РЕЗУЛЬТАТ: ${data.result}

📊 Объяснение:
- ML модель анализирует статистику пикселей
- Проверяется шум, структура JPEG и DCT
- Если показатели отклоняются — фото изменено

🐱 Это нужно для:
- выявления подделок
- защиты данных
`;

    document.getElementById("out").innerText = text;
}

async function compare(){
    let file2 = document.getElementById("file2").value;

    let res = await fetch(`/compare?file1=${current}&file2=${file2}`,{method:"POST"});
    let data = await res.json();

    alert("Difference: "+data.difference_score);
}