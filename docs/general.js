function loadHeader() {
    fetch('/header.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('header').innerHTML = data;
        });
}

function fillTime() {
    const timeElement = document.getElementById("date");
    const datetimeValue = timeElement.getAttribute("datetime") + "T12:00:00";

    // Convert the datetime value into a human-readable format
    const formattedDate = new Date(datetimeValue).toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric"
    });

    // Update the content of the <time> element
    timeElement.textContent = formattedDate;
}