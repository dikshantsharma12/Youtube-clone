if (window.history.replaceState) {
  window.history.replaceState(null, null, window.location.href);
}

async function saveVideo() {
  data = JSON.stringify({

    videoId: document.getElementById('save-button').getAttribute('videoId'),
    userId: document.getElementById('save-button').getAttribute('currUser')
  });
  console.log(data)
  await fetch('/savevideo/', {
    method: 'POST',
    body: data,
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': document.querySelector('[name = csrfmiddlewaretoken]').value
    }
  })
    .then(response => response.json())
    .then(output => {
      console.log(output)
      return output;
    })
    .catch(error => console.error(error));

}
async function toggleLike(option) {
  data = JSON.stringify({

    videoId: document.getElementById("uploader-buttons").getAttribute('videoId'),
    userId: document.getElementById("uploader-buttons").getAttribute('currUser'),
    option: option
  });
  console.log(data)
  await fetch('/togglelike/', {
    method: 'POST',
    body: data,
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': document.querySelector('[name = csrfmiddlewaretoken]').value
    }
  })
    .then(response => response.json())
    .then(output => {
      console.log(output)
      return output;
    })
    .catch(error => console.error(error));

}