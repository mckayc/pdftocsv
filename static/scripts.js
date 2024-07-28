document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    let formData = new FormData();
    formData.append('pdfFile', document.getElementById('pdfFile').files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
      .then(data => {
          if (data.success) {
              window.location.href = '/groups';
          } else {
              document.getElementById('response').innerText = data.message;
          }
      });
});

document.getElementById('groupForm').addEventListener('submit', function(event) {
    event.preventDefault();
    let groups = {};
    document.querySelectorAll('.group-name').forEach((input, index) => {
        groups[index] = input.value;
    });

    fetch('/export', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(groups)
    }).then(response => response.json())
      .then(data => {
          if (data.success) {
              window.location.href = '/download';
          } else {
              alert('Failed to export CSV');
          }
      });
});
