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

        if (response.ok) {
            const data = await response.json();
            console.log(data);

            if (data.error) {
                document.getElementById('output').innerText = data.error;
            } else {
                const outputDiv = document.getElementById('output');
                outputDiv.innerHTML = `
                    <div class="details-section">
                        <img src="${data.photo_path}" alt="Foto" class="image-avatar">
                        <div class="info">
                            <p><strong>Nome:</strong> ${data.name}</p>
                            <p><strong>Idade:</strong> ${data.age}</p>
                            <p><strong>Email:</strong> ${data.email}</p>
                            <p><strong>UID:</strong> ${data.uid}</p>
                        </div>
                    </div>
                    <div class="json-section">
                        <pre>
{
    "age": ${data.age},
    "email": "${data.email}",
    "name": "${data.name}",
    "uid": "${data.uid}",
    "photo_path": "${data.photo_path}"
}
                        </pre>
                    </div>
                `;
            }
        } else {
            const result = await response.text();
            console.log(`Error response: ${result}`);
            document.getElementById('output').innerText = result;
        }
    } catch (error) {
        console.error('Fetch error:', error);
        document.getElementById('output').innerText = 'An error occurred';
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

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            const formData = new FormData(this);
            fetch(this.action, {
                method: this.method,
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        document.querySelector('.output').innerHTML = `<p>${data.error}</p>`;
                    } else {
                        const outputDiv = document.querySelector('.output');
                        outputDiv.innerHTML = `
                        <div class="details-section">
                            <img src="${data.photo_path}" alt="Foto" class="image-avatar">
                            <div class="info">
                                <p><strong>Nome:</strong> ${data.name}</p>
                                <p><strong>Idade:</strong> ${data.age}</p>
                                <p><strong>Email:</strong> ${data.email}</p>
                                <p><strong>UID:</strong> ${data.uid}</p>
                            </div>
                        </div>
                        <div class="json-section">
                            <pre>
{
    "age": ${data.age},
    "email": "${data.email}",
    "name": "${data.name}",
    "uid": "${data.uid}",
    "photo_path": "${data.photo_path}"
}
                            </pre>
                        </div>
                    `;
                    }
                })
                .catch(error => {
                    document.querySelector('.output').innerHTML = `<p>Error: ${error.message}</p>`;
                    console.error('Error:', error);
                });
        });
    });
});
