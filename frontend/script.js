document.getElementById('convert-btn').addEventListener('click', () => {
  const regex = document.getElementById('regex-input').value;
  if (!regex) {
    alert('Please enter a regular expression');
    return;
  }
  
  fetch('http://127.0.0.1:5000/convert', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ regex })
  })
  .then(response => response.json())
  .then(data => {
    d3.select("#nfa-graph").html('').graphviz().renderDot(data.nfa);
    d3.select("#dfa-graph").html('').graphviz().renderDot(data.dfa);
    d3.select("#minimized-dfa-graph").html('').graphviz().renderDot(data.minimized_dfa);
  })
  .catch(error => {
    console.error('Error:', error);
    alert('Error converting regex. Make sure the backend server is running.');
  });
});

document.getElementById('test-string-btn').addEventListener('click', () => {
  const regex = document.getElementById('regex-input').value;
  const string = document.getElementById('test-string-input').value;
  
  if (!regex) {
    alert('Please enter a regular expression first');
    return;
  }
  
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
    resultElement.textContent = data.accepted ? '✓ Accepted' : '✗ Rejected';
    resultElement.className = data.accepted ? 'accepted' : 'rejected';
  })
  .catch(error => {
    console.error('Error:', error);
    alert('Error testing string. Make sure the backend server is running.');
  });
});