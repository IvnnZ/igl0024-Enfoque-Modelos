async function enviarPregunta() {
    const texto = document.getElementById("preguntaInput").value;
    document.getElementById("preguntaInput").value = '';

    if (!texto) {
        alert("Por favor, escribe una pregunta.");
        return;
    }

    agregarMensajeUser(texto, 'usuario');

    const response = await fetch("http://127.0.0.1:8000/consulta", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ texto })
    });
    
    if (response.ok) {
        const data = await response.json();
        
        agregarMensaje(data['respuesta'], 'bot', data['categoria'], data['precision']);
    } else {
        agregarMensaje('Error al consultar al chatbot.', 'bot');
    }
}

function agregarMensaje(texto, tipo, categoria, precision) {
    const respuestaBot = document.getElementById('respuestaBot');
    const div = document.createElement('div');
    div.classList.add('mensaje', tipo);
    div.innerHTML ="<strong>Asistente: </strong>" +  texto;  
    respuestaBot.appendChild(div);

    // Auto scroll al final
    respuestaBot.scrollTop = respuestaBot.scrollHeight;
}

function agregarMensajeUser(texto, tipo) {
    const respuestaBot = document.getElementById('respuestaBot');
    const div = document.createElement('div');
    div.classList.add('mensaje', tipo);
    div.innerHTML = "<strong>Tú: </strong>" + texto;
    respuestaBot.appendChild(div);

    // Auto scroll al final
    respuestaBot.scrollTop = respuestaBot.scrollHeight;
}

function clearChatBox() {
    const respuestaBot = document.getElementById('respuestaBot');
    respuestaBot.innerHTML = '';
    init();
}

function onKeyDownHandler(event) {
    var codigo = event.which || event.keyCode;

    if(codigo === 13){
      document.getElementById('btnEnviar').click();
    }  
}

function toggleChat() {
    const chatBox = document.getElementById("chatContainer");
    chatBox.style.display = chatBox.style.display === "none" || chatBox.style.display === "" ? "block" : "none";
}