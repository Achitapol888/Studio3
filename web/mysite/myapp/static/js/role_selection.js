function selectRole(figureElement) {
    const button = document.getElementById('nextButton');

    // Get the URL of the clicked figure
    const newUrl = figureElement.getAttribute('data-url');

    // Check if the clicked figure is already selected
    const isAlreadyClicked = figureElement.classList.contains('clicked');

    // Remove the clicked class from all figures and add unclicked class
    const figures = document.querySelectorAll('figure');
    figures.forEach((figure) => {
        figure.classList.remove('clicked');
        figure.classList.add('unclicked');
    });
    button.classList.remove("disabled")
    button.classList.add("active")


    // If it was already clicked, reset the button URL
    if (isAlreadyClicked) {
        button.href = ''; // Reset the button URL
        button.classList.remove("active")
        button.classList.add("disabled")
        return; // Exit the function
    }

    // Set the href of the button to the new URL and add the clicked class to the current figure
    button.href = newUrl;
    figureElement.classList.remove('unclicked'); // Remove unclicked state for the new selection
    figureElement.classList.add('clicked'); // Add clicked class to the currently selected figure

}



