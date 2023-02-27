window.onload = (event) => {
console.log("some")
const apiUrl = 'http://127.0.0.1:5000/get_events_by_date/123';


fetch(apiUrl, {
    method: "GET",})
  .then(response => response.json())
  .then(data => {
    console.log(data); // вивести дані в консоль
  })
  .catch(error => {
    console.error('Помилка:', error);
  });
}