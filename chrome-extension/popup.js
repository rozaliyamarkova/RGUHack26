// Check if name is already saved, skip form if so
chrome.storage.sync.get('userName', (data) => {
  if (data.userName) {
    showGreeting(data.userName);
  }
});

document.getElementById('saveBtn').addEventListener('click', () => {
  const name = document.getElementById('nameInput').value;
  if (!name) {
    alert("Please enter a name.");
    return; // don't save if empty
  }

  chrome.storage.sync.set({ userName: name }, () => {
    showGreeting(name);
  });
});

function showGreeting(name) {
  document.getElementById('nameForm').style.display = 'none';
  document.getElementById('greeting').style.display = 'block';
  document.getElementById('greetingText').textContent = "Hello, " + name + "!";
}