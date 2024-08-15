async function handleFormSubmit(event, url) {
    event.preventDefault();

    // Limpar o conteúdo anterior
    document.getElementById('output').innerText = '';
    document.getElementById('loading').style.display = 'block';

    try {
        const response = await fetch(url, {
            method: 'POST'
        });

        document.getElementById('loading').style.display = 'none';

        const outputDiv = document.getElementById('output');

        if (response.ok) {
            const data = await response.json();
            console.log('Data received:', data);

            if (url === '/execute') {
                const detailsSection = document.createElement('div');
                detailsSection.className = 'details-section';

                detailsSection.innerHTML = `
                    <img src="${data.photo_path}" alt="Foto" class="image-avatar">
                    <div class="info">
                        <p><strong>Nome:</strong> ${data.name}</p>
                        <p><strong>Idade:</strong> ${data.age}</p>
                        <p><strong>Email:</strong> ${data.email}</p>
                        <p><strong>UID:</strong> ${data.uid}</p>
                    </div>
                `;

                const jsonSection = document.createElement('div');
                jsonSection.className = 'json-section';
                jsonSection.innerHTML = `
                    <pre>
                        {
                            "age": ${data.age},
                            "email": "${data.email}",
                            "name": "${data.name}",
                            "uid": "${data.uid}",
                            "photo_path": "${data.photo_path}"
                        }
                    </pre>
                `;

                // Adicionar as seções ao outputDiv
                outputDiv.innerHTML = ''; // Limpa conteúdo anterior (se aplicável)
                outputDiv.appendChild(detailsSection);
                outputDiv.appendChild(jsonSection);

            } else if (url === '/execute_dump') {
                // Criar a seção principal
                const section = document.createElement('section');
                section.className = 'card-output';

                // Criar as duas divs
                const divLeft = document.createElement('div');
                const divRight = document.createElement('div');
                divLeft.className = 'left-output';
                divRight.className = 'right-output';

                // Inserir os textos nas divs
                divLeft.innerHTML = `<pre>${data.part1}</pre>`;
                divRight.innerHTML = `<pre>${data.part2}</pre>`;

                // Adicionar as divs à seção
                section.appendChild(divLeft);
                section.appendChild(divRight);

                // Adicionar a seção ao outputDiv
                outputDiv.appendChild(section);

            } else if (url === '/execute_clone' || url === '/execute_wipe') {
                outputDiv.innerHTML = `
                    <p><strong>Status:</strong> ${data.status}</p>
                `;
            }
        } else {
            // Captura de erros nas respostas com status diferente de 200 OK
            const data = await response.json();
            outputDiv.innerHTML = `<p><strong>Error:</strong> ${data.error}</p>`;
        }
    } catch (error) {
        console.error('Fetch error:', error);
        document.getElementById('output').innerText = 'An error occurred';
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
}

document.getElementById('commandForm1').addEventListener('submit', function (event) {
    handleFormSubmit(event, '/execute');
});

document.getElementById('commandForm2').addEventListener('submit', function (event) {
    handleFormSubmit(event, '/execute_dump');
});

document.getElementById('commandForm3').addEventListener('submit', function (event) {
    handleFormSubmit(event, '/execute_clone');
});

document.getElementById('commandForm4').addEventListener('submit', function (event) {
    handleFormSubmit(event, '/execute_wipe');
});

