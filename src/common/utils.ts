export function sendCommonRequest(requestURL: string, body: string, setImageURL: (url: string) => void) {
  fetch(requestURL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': 'http://localhost:3000'
    },
    body: body,
  })
    .then((response) => response.json())
    .then((data) => {
      setImageURL(data.url);
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}
