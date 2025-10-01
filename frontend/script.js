document.getElementById('convert-btn').addEventListener('click', () => {
    const regex = document.getElementById('regex-input').value;
    fetch('http://127.0.0.1:5000/convert', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ regex })
    })
    .then(response => response.json())
    .then(data => {
        d3.select("#nfa-graph").graphviz().renderDot(data.nfa);
        d3.select("#dfa-graph").graphviz().renderDot(data.dfa);
        d3.select("#minimized-dfa-graph").graphviz().renderDot(data.minimized_dfa);
    });
});

document.getElementById('test-string-btn').addEventListener('click', () => {
    const regex = document.getElementById('regex-input').value;
    const string = document.getElementById('test-string-input').value;
    fetch('http://127.0.0.1:5000/test', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ regex, string })
    })
    .then(response => response.json())
    .then(data => {
        const resultElement = document.getElementById('test-result');
        resultElement.textContent = data.accepted ? 'Accepted' : 'Rejected';
    });
});