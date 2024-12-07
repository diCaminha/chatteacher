let chat = document.querySelector('#chat');
let input = document.querySelector('#input');
let botaoEnviar = document.querySelector('#botao-enviar');
let botaoMaisArquivo = document.querySelector('#mais_arquivo');
let selectedFile = null; // To store the selected file

async function enviarMensagem() {
    if (input.value == "" || input.value == null) return;
    let mensagem = input.value;
    input.value = "";

    // Create user bubble
    let novaBolha = criaBolhaUsuario();
    novaBolha.innerHTML = mensagem;
    chat.appendChild(novaBolha);

    // Create bot bubble (for loading)
    let novaBolhaBot = criaBolhaBot();
    chat.appendChild(novaBolhaBot);
    vaiParaFinalDoChat();
    novaBolhaBot.innerHTML = "Analisando ..."

    // Prepare form data for sending text and file
    const formData = new FormData();
    formData.append('msg', mensagem);
    if (selectedFile) {
        formData.append('file', selectedFile);
    }

    // Send request to the /chat endpoint with FormData
    const resposta = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        body: formData
    });

    const textoDaResposta = await resposta.text();
    console.log(textoDaResposta);
    novaBolhaBot.innerHTML = textoDaResposta.replace(/\n/g, '<br>');
    vaiParaFinalDoChat();

    // Reset the selected file after sending, if desired
    selectedFile = null;
    document.querySelector('#fileInput').value = '';
}

function criaBolhaUsuario() {
    let bolha = document.createElement('p');
    bolha.classList = 'chat__bolha chat__bolha--usuario';
    return bolha;
}

function criaBolhaBot() {
    let bolha = document.createElement('p');
    bolha.classList = 'chat__bolha chat__bolha--bot';
    return bolha;
}

function vaiParaFinalDoChat() {
    chat.scrollTop = chat.scrollHeight;
}

botaoEnviar.addEventListener('click', enviarMensagem);
input.addEventListener("keyup", function(event) {
    event.preventDefault();
    if (event.keyCode === 13) {
        botaoEnviar.click();
    }
});

document.querySelector('#fileInput').addEventListener('change', function() {
    selectedFile = this.files[0];
    let fileStatus = document.querySelector('#file-status');
    if (selectedFile) {
        // Show the file name or a short message
        fileStatus.textContent = `Arquivo selecionado: ${selectedFile.name}`;
        fileStatus.style.color = "green"; // Optional styling
    } else {
        fileStatus.textContent = "";
    }
});

// Trigger the file chooser when "mais_arquivo" is clicked
botaoMaisArquivo.addEventListener('click', function() {
    document.querySelector('#fileInput').click();
});
