var co2 = [];
var co2g = [];
var mq2g = [];
var s135 = [];
var mq4 = [];
var mq7 = [];
///-////_////_///_///_///_//_//
var valormq2 = "0";
var valorco2 = "0";
var valorco2g = "0";
var valormq7 = "0";
var valormq4 = "0";
var mq135 = "0";
var data = [];
var strigs = "";

data.push('co2win,co2g,mq4,mq7,mq135,mq2,time');

let save = document.getElementById("save");
//Guarda los datos
save.onclick = () => {
    console.log("save");
    downloadFile();
}
setInterval(function() {
    //Peticion para obtener valores de corriente
    let respuesta = new XMLHttpRequest();
    respuesta.open('GET', 'http://192.168.1.14/co2');

    respuesta.onreadystatechange = function() {
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            valorco2 = this.responseText;
        }
    };
    respuesta.send();
    let respuesta2 = new XMLHttpRequest();
    respuesta2.open('GET', 'http://192.168.1.15/co2');

    respuesta2.onreadystatechange = function() {
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            valorco2g = this.responseText;
        }
    };
    respuesta2.send();

    let respuesta3 = new XMLHttpRequest();
    respuesta3.open('GET', 'http://192.168.1.14/mq7');

    respuesta3.onreadystatechange = function() {
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            valormq7 = this.responseText;
        }
    };
    respuesta3.send();

    let respuesta4 = new XMLHttpRequest();
    respuesta4.open('GET', 'http://192.168.1.14/mq4');

    respuesta4.onreadystatechange = function() {
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            valormq4 = this.responseText;
        }
    };
    respuesta4.send();
    let respuesta5 = new XMLHttpRequest();
    respuesta5.open('GET', 'http://192.168.1.14/mq135');

    respuesta5.onreadystatechange = function() {
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            mq135 = this.responseText;
        }
    };
    respuesta5.send();
    let respuesta6 = new XMLHttpRequest();
    respuesta6.open('GET', 'http://192.168.1.14/mq2');

    respuesta6.onreadystatechange = function() {
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            valormq2 = this.responseText;
        }
    };
    respuesta6.send();
    co2.push(valorco2);
    co2g.push(valorco2g);
    mq4.push(valormq4);
    mq7.push(valormq7);
    s135.push(mq135);
    mq2g.push(valormq2);
    //150 250 0
    console.log(co2);
    console.log(co2g);
    console.log(mq4);
    console.log(mq7);
    console.log(s135);
    console.log(mq2g);
    var time = new Date();
    strigs = valorco2 + "," + valorco2g + ", " + valormq4 + "," + valormq7 + ", " + +mq135 + ", " + valormq2 + ',' + time;
    localStorage.setItem('datos', data);
    console.log("Datos");
    //  console.log(localStorage.getItem('datos'));

    //console.log(strigs);
    data.push(strigs);
    // console.log(data);

}, 1000);


function arrayObjToCsv(ar) {
    //comprobamos compatibilidad
    if (window.Blob && (window.URL || window.webkitURL)) {
        var contenido = "",
            d = new Date(),
            blob,
            reader,
            save,
            clicEvent;
        //creamos contenido del archivo
        for (var i = 0; i < ar.length; i++) {
            //construimos cabecera del csv
            if (i == 0)
                contenido += Object.keys(ar[i]).join("") + "\n";
            //resto del contenido
            contenido += Object.keys(ar[i]).map(function(key) {
                return ar[i][key];
            }).join("") + "\n";
        }
        //creamos el blob
        blob = new Blob(["\ufeff", contenido], { type: 'text/csv' });
        //creamos el reader
        var reader = new FileReader();
        reader.onload = function(event) {
                //escuchamos su evento load y creamos un enlace en dom
                save = document.createElement('a');
                save.href = event.target.result;
                save.target = '_blank';
                //aquí le damos nombre al archivo
                save.download = "log_" + d.getDate() + "_" + (d.getMonth() + 1) + "_" + d.getFullYear() + ".csv";
                try {
                    //creamos un evento click
                    clicEvent = new MouseEvent('click', {
                        'view': window,
                        'bubbles': true,
                        'cancelable': true
                    });
                } catch (e) {
                    //si llega aquí es que probablemente implemente la forma antigua de crear un enlace
                    clicEvent = document.createEvent("MouseEvent");
                    clicEvent.initEvent('click', true, true);
                }
                //disparamos el evento
                save.dispatchEvent(clicEvent);
                //liberamos el objeto window.URL
                (window.URL || window.webkitURL).revokeObjectURL(save.href);
            }
            //leemos como url
        reader.readAsDataURL(blob);
    } else {
        //el navegador no admite esta opción
        alert("Su navegador no permite esta acción");
    }
};
setInterval(function() { downloadFile() }, 10000000);

//Download archivo 
function downloadFile() {
    arrayObjToCsv(data);
}