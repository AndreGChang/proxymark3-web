// document.getElementById('commandForm').addEventListener('submit', async function (event) {
//     event.preventDefault();

//     // Limpar o conteúdo anterior
//     document.getElementById('output').innerText = '';

//     try {
//         const response = await fetch('/execute', {
//             method: 'POST'
//         });

//         if (response.ok) {
//             const person = await response.json();
//             console.log(`Redirecting to /person/${person.uid}`);
//             window.location.href = `/person/${person.uid}`;
//         } else {
//             const result = await response.text();
//             console.log(`Error response: ${result}`);
//             document.getElementById('output').innerText = result;
//         }
//     } catch (error) {
//         console.error('Fetch error:', error);
//         document.getElementById('output').innerText = 'An error occurred';
//     }
// });
document.getElementById('commandForm').addEventListener('submit', async function (event) {
    event.preventDefault();

    // Limpar o conteúdo anterior
    document.getElementById('output').innerText = '';

    try {
        const response = await fetch('/execute', {
            method: 'POST'
        });

        if (response.ok) {
            const person = await response.json();
            console.log(`Redirecting to /person?uid=${person.uid}`);
            window.location.href = `/person?uid=${person.uid}`;
        } else {
            const result = await response.text();
            console.log(`Error response: ${result}`);
            document.getElementById('output').innerText = result;
        }
    } catch (error) {
        console.error('Fetch error:', error);
        document.getElementById('output').innerText = 'An error occurred';
    }
});
