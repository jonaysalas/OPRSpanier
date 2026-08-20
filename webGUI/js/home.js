function GenerarListas(){
    var data = {};
    var form = new FormData(document.getElementById("FormGenerarListas"))
    form.forEach(function(value, key){
        data[key] = value;
        
    });
    eel.GenerateFicheros(data);
    var path = document.getElementById("selectorDocumento");
}

async function SelectManualConfigPath(){
    var filePath = await eel.FileSelector()();
    eel.SetManualTranslator(filePath)
}

async function SelectFicheroPath(){
    var filePath = await eel.FileSelector()();
    eel.SetPathFicheroListas(filePath);
    document.getElementById("labelFicheroListas").innerHTML = filePath;
}

async function SelectCarpetaPDFPath(){
    var filePath = await eel.FolderSelector()();
    eel.SetGuardarPdfEn(filePath);
    document.getElementById("labelCarpetaPdfs").innerHTML = filePath;
}

async function ToongleVisibility(){
    var visibility = await eel.GetBrowserVisible()();
    var LabelOption = document.getElementById("VisibilityStatus")
    if (visibility == true){
        eel.SetBrowserVisible(false);
        LabelOption.textContent = "Ocultar Navegador: Off";
    }else{
        eel.SetBrowserVisible(true);
        LabelOption.textContent = "Ocultar Navegador: On";
    }
}

async function SaveConfiguration(){
    try{
        eel.SaveConfiguration();
        alert("Se ha guardado la configuración")
    }catch{
        alert("No se pudo guardar la configuración")
    }
}

async function PreparePage(){
    try{
        document.getElementById("labelCarpetaPdfs").innerHTML = await eel.GetGuardarPdfEn()();
        var visibility = await eel.GetBrowserVisible()();
        var LabelOption = document.getElementById("VisibilityStatus")
        if (visibility == true){
            LabelOption.textContent = "Ocultar Navegador: On";
        }else{
            LabelOption.textContent = "Ocultar Navegador: Off";
        }
    }catch{
        alert("No se pudo cargar la configuración")
    }
}

async function ResetTraductorHistorico(){
    var ok = await eel.ResetHistoryTranslator()();
    if (ok==true){
        alert("El historico de traducciones se reseteó correctamente")
    }else{
        alert("ERROR: No se pudo resetear el historial de traducciones")
    }
}

async function CreateTraductorManual(){
    var ok = await eel.CreateMaualTranslator()();
    if (ok==true){
        alert("Se creó el traductor manual")
    }else{
        alert("ERROR: No se pudo crear el tracutor manual")
    }
}

function PrintMessage(message){
    alert(message)
}
eel.expose(PrintMessage)
window.onload = function(){
    PreparePage()
}