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
            const result = await response.text();
            console.log(result);
            document.getElementById('output').innerText = result;
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
