const BASE_URL = "http://127.0.0.1:8000/api/v1"

function getUserIdToken() {
    return new Promise((resolve) => {
      chrome.storage.sync.get('user_id', (data) => {
        resolve(data.user_id)
      })
    })
  }

export async function getRequest(path) {  
    try {
        const response = await fetch(`${BASE_URL}${path}`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${await getUserIdToken()}` },
        })
    
        if (!response.ok) {
            throw new Error('Failed to register student')
        }
    
        const data = await response.json()
        return data
    } catch (err) {
        console.error(err)
        error.value = 'Please use letters only (A-Z).'
    }
}

export async function postRequest(path, payload) {  
    try {
        const response = await fetch(`${BASE_URL}${path}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${await getUserIdToken()}` },
            body: JSON.stringify(payload)
        })

        const data = await response.json()
        return data
    } catch (err) {
        console.error(err)
    }
}

export async function deleteRequest(path) {
    try {
        const response = await fetch(`${BASE_URL}${path}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${await getUserIdToken()}` },
        })

        const data = await response.json()
        return data
        
    } catch (err) {
        console.error(err)
    }
}