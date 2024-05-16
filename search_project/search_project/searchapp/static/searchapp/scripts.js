// scripts.js

// Update the color function of the selection box
function updateSelectColor(selectElement) {
    // Check if the default placeholder option is selected
    if (selectElement.value) {
        selectElement.style.color = '#000'; // Option selected, color set to black
    } else {
        selectElement.style.color = '#ccc'; // No options are selected and the color is set to gray
    }
}



// Save the current scroll position before submitting the form
function saveScrollPosition() {
    localStorage.setItem('scrollPosition', window.scrollY || document.documentElement.scrollTop);
}



// Restore the scroll position if it was saved before
function restoreScrollPosition() {
    // Check if there is a saved scroll position in localStorage
    const savedPosition = localStorage.getItem('scrollPosition');
    if (savedPosition) {
        window.scrollTo(0, parseInt(savedPosition, 10));
        localStorage.removeItem('scrollPosition'); // 清除存储的位置，以免影响后续使用
    }

    // Existing URL hash based scrolling code
    const hash = window.location.hash;
    if (hash) {
        const section = document.querySelector(hash);
        if (section) {
            section.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }
}

// Trigger this before submitting the form
function prepareForSearch() {
  if (validateForm()) {
        const currentPage = getCurrentPageFromURL();
        const form = document.getElementById('searchForm');
        const actionURL = new URL(window.location.href);

        actionURL.searchParams.set('page', currentPage);
        form.action = actionURL.toString(); // Setting form's action to include the current page

        // scrollToResults();
        saveScrollPosition();
    }
}

function validateForm() {
    var searchInput = document.getElementById("searchInput").value;
    var queryType = document.getElementById("queryType").value;
    var resultsPerPage = document.getElementById("results_per_page").value;
    var formIsValid = true; // Assume form is valid initially

    // Check for keyword input
    if (!searchInput) {
        alert("Please enter search keywords");
        formIsValid = false; // Set to false if validation fails
    }

    // Check for query type selection
    if (!queryType) {
        alert("Please select a query type");
        formIsValid = false; // Set to false if validation fails
    }

    // Additional validation for 'spousal' query type
    if (queryType === 'spousal') {
        var allowedInputs = ['wife', 'husband', 'spouse'];
        if (!allowedInputs.includes(searchInput.toLowerCase())) {
            alert("For 'spousal' type, please enter one of the following options: wife, husband, spouse.");
            formIsValid = false; // Set to false if validation fails
        }
    }

    // Check for results per page input
    if (!resultsPerPage || resultsPerPage < 1) {
        alert("Please enter a valid number of results per page.");
        formIsValid = false; // Set to false if validation fails
    }

    // Scroll to results and save the scroll position if form is valid
    if (formIsValid) {
        scrollToResults();
        saveScrollPosition();
        restoreScrollPosition()
    }
    return formIsValid; // Return the final validity of the form
}



document.getElementById('searchForm').addEventListener('submit', saveScrollPosition);


function getCurrentPageFromURL() {
    // 假设URL中的页码参数是 'page'
    const urlParams = new URLSearchParams(window.location.search);
    return parseInt(urlParams.get('page') || "1", 10); // 如果没有page参数，默认是第1页
}

// Call restoreScrollPosition on page load
window.onload = function (){
    // Check if we need to scroll to results
    if (localStorage.getItem('scrollAfterLoad') === 'true') {
        scrollToResults();
        localStorage.removeItem('scrollAfterLoad'); // Clear the flag
    }

}


function clearForm() {
    document.getElementById('searchInput').value = '';
    document.getElementById('queryType').selectedIndex = 0;
    document.getElementById('results_per_page').value = '10';
    updateSelectColor(document.getElementById('queryType')); // Update the color to the default
    // Scroll to the top of the page
    window.scrollTo({ top: 0, behavior: 'smooth' });
    // Consider resetting any other relevant fields
}


function scrollToResults() {
    const resultsDiv = document.getElementById('results_page');
    if (resultsDiv) {
        resultsDiv.scrollIntoView({behavior: 'smooth', block: 'start'});
    }
}




document.addEventListener('DOMContentLoaded', function() {
    const sections = document.querySelectorAll('section');
    const navDots = document.querySelectorAll('#dot-nav ul li a');
    const currentPage = getCurrentPageFromURL() || 0;

    function getCurrentPageFromURL() {
        // Assume that the page number parameter in the URL is 'page'
        const urlParams = new URLSearchParams(window.location.search);
        return parseInt(urlParams.get('search'), 10);
    }

    function setActiveDot(index) {
        navDots.forEach((dot, idx) => {
            dot.classList.toggle('active', idx === index);
        });
    }

    setActiveDot(currentPage - 1);

    // Update navigation point highlight state based on scroll position
    function changeDotNav() {
        let index = sections.length;

        // Subtract the window scroll position to find the current section
        while(--index && window.scrollY + 50 < sections[index].offsetTop) {}

        navDots.forEach((dot) => { dot.classList.remove('active'); });
        if (navDots[index]) {
            navDots[index].classList.add('active');
        }
    }

    // Add click events to each navigation point for smooth scrolling to the corresponding page section
    navDots.forEach((dot) => {
        dot.addEventListener('click', function(e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);

            if (targetSection) {
                window.scrollTo({
                    top: targetSection.offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Listen to scroll events to update the navigation point's highlighted state
    window.addEventListener('scroll', changeDotNav);
    changeDotNav();
});



window.addEventListener('DOMContentLoaded', (event) => {
    document.querySelectorAll('select').forEach(function(select) {
        updateSelectColor(select);
        select.addEventListener('change', function() {
            updateSelectColor(this);
        });
    });
});