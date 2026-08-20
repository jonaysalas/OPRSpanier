
async function addElementos(tipo){
    var pathTrad = ""
    if (tipo == "manual"){
        document.getElementById("Title").innerText = "Gestor de Traducciones Manuales";
        pathTrad = await eel.GetManualTranslator()();
        document.getElementById("save-changes").addEventListener("click", GuardarCambiosManual);

        var addBtn = document.createElement("button");
        addBtn.classList.add("button");
        addBtn.innerText="Añadir Linea";
        addBtn.addEventListener("click", AddElementEvent)

        saveBtn = document.getElementById("save-changes");
        saveBtn.parentNode.insertBefore(addBtn, saveBtn);

    }else{
        document.getElementById("Title").innerText = "Gestor del Historial de Traducciones";
        pathTrad = await eel.GetHistoryTranslator()();
        document.getElementById("save-changes").addEventListener("click", GuardarCambiosHistorico);
    };
    var dicTrans = await eel.LoadATranslatorDictionary(pathTrad)();
    for (const key of Object.keys(dicTrans).sort()){
        AddElement(key, dicTrans[key]);
    }
}

async function AddElementEvent(event){
    AddElement();
};

async function AddElement(orig = "", trad = ""){
    var li = document.createElement("li");
    var textAreaOrig = document.createElement("textarea");
    var textAreaTrad = document.createElement("textarea");
    
    textAreaOrig.classList.add("entradaOriginal");
    textAreaTrad.classList.add("entradaTraducida");
    
    textAreaOrig.value = orig;
    textAreaTrad.value = trad;

    li.appendChild(textAreaOrig);
    li.appendChild(textAreaTrad);
    document.querySelector("#lista-elementos").appendChild(li);
};

async function GuardarCambiosHistorico(event) {
    await eel.SaveATranslatorDictionary(await GetActualDictionary(), await eel.GetHistoryTranslator()(), true)();
};

async function GuardarCambiosManual(event){
    await eel.SaveATranslatorDictionary(await GetActualDictionary(), await eel.GetManualTranslator()(), true)();
};

async function GetActualDictionary(){
    var new_trans = {};
    for(const li of document.getElementById('lista-elementos').children){
        key = li.children[0].value.trim();
        value = li.children[1].value.trim();
        
        if (key==""){
            continue;
        };

        if(key in Object.keys(new_trans)){
            alert("La traducción '"+key+"' está repetida");
            return undefined;
        };

        if(value == ""){
            alert("El texto '"+key+"' no tiene traducción");
            return undefined;
        };
        new_trans[key] = value;
    };
    return new_trans;
}

var vars = {}; 
var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) { 
   vars[key] = value; 
});
window.onload = (event) => {
    addElementos(vars['tipo']);
};