document.getElementById('convert-btn').addEventListener('click', () => {
  const regex = document.getElementById('regex-input').value;
  if (!regex) {
    alert('Please enter a regular expression');
    return;
  }

  const API_BASE_URL = 'https://regex-to-dfa.onrender.com';
  
  fetch(`${API_BASE_URL}/convert`, {
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

    document.querySelectorAll('.graph-wrapper').forEach(w => {
      w.style.animation = 'none';
      void w.offsetWidth;
      w.style.animation = '';
    });
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
  
  fetch(`${API_BASE_URL}/test`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ regex, string })
  })
  .then(response => response.json())
  .then(data => {
    animateTestFeedback(string, data.accepted);
  })
  .catch(error => {
    console.error('Error:', error);
    alert('Error testing string. Make sure the backend server is running.');
  });
});

document.querySelectorAll('.download-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const targetId = btn.getAttribute('data-target');
    const prettyName = btn.parentElement && btn.parentElement.textContent ? btn.parentElement.textContent.trim().split('\n')[0].replace(/\s+/g, '_').toLowerCase() : targetId;
    downloadGraphAsPng(targetId, `${prettyName}.png`);
  });
});

function downloadGraphAsPng(targetId, filename) {
  const container = document.getElementById(targetId);
  if (!container) return;
  const svg = container.querySelector('svg');
  if (!svg) {
    alert('No image to download yet. Convert first.');
    return;
  }

  const serializer = new XMLSerializer();
  let svgString = serializer.serializeToString(svg);

  if (!svgString.startsWith('<?xml')) {
    svgString = '<?xml version="1.0" standalone="no"?>\r\n' + svgString;
  }

  const svgBlob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' });
  const url = URL.createObjectURL(svgBlob);
  const img = new Image();

  const { width, height } = svg.getBoundingClientRect();
  const canvas = document.createElement('canvas');
  canvas.width = Math.max(1, Math.floor(width));
  canvas.height = Math.max(1, Math.floor(height));
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = '#ffffff';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  img.onload = function() {
    ctx.drawImage(img, 0, 0);
    URL.revokeObjectURL(url);
    canvas.toBlob(blob => {
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
    }, 'image/png');
  };
  img.onerror = function() {
    URL.revokeObjectURL(url);
    alert('Failed to render image for download.');
  };
  img.src = url;
}

function animateTestFeedback(text, accepted) {
  const result = document.getElementById('test-result');
  result.className = '';
  result.innerHTML = '';

  const bubbles = document.createElement('div');
  bubbles.className = 'char-bubbles';
  result.appendChild(bubbles);

  const chars = text.split('');
  const bubblesList = chars.map(ch => {
    const b = document.createElement('span');
    b.className = 'char-bubble';
    b.textContent = ch || '∅';
    bubbles.appendChild(b);
    return b;
  });

  let i = 0;
  function step() {
    if (i > 0) {
      bubblesList[i - 1].classList.remove('active');
      bubblesList[i - 1].classList.add(accepted ? 'pass' : 'fail');
    }

    if (i < bubblesList.length) {
      const b = bubblesList[i];
      b.classList.add('show', 'active');
      i += 1;
      setTimeout(step, 130);
    } else {
      const label = document.createElement('div');
      label.style.marginTop = '10px';
      label.textContent = accepted ? '✓ Accepted' : '✗ Rejected';
      result.appendChild(label);
      result.className = accepted ? 'accepted' : 'rejected';

      if (!accepted) {
        result.classList.add('shake');
        setTimeout(() => result.classList.remove('shake'), 500);
      }
    }
  }

  if (bubblesList.length === 0) {
    const label = document.createElement('div');
    label.textContent = accepted ? '✓ Accepted' : '✗ Rejected';
    result.appendChild(label);
    result.className = accepted ? 'accepted' : 'rejected';
    return;
  }

  bubblesList.forEach((b, idx) => setTimeout(() => b.classList.add('show'), 40 * idx));
  setTimeout(step, 60 * bubblesList.length + 100);
}

