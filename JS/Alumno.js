document.querySelector('#btn-read').addEventListener('click', function(){
    obtenerDatos();
});
function obtenerDatos(){
    

    let url = 'https://lfhb3ctl05.execute-api.us-east-1.amazonaws.com/test/alumno/7/aaaa';
    const api = new XMLHttpRequest();
    api.open('GET', url, true);
    api.send();
    api.onreadystatechange= function(){
    if(this.status == 200 && this.readyState == 4){
    let datos=JSON.parse(this.responseText);
    console.log(datos);
    }

    }

}   

