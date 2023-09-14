// Add click event listener to the "View Barchart" button
document.getElementById("view-barchart-button").addEventListener("click", function () {
    const selectedBox = document.querySelector(".snail-box.expanded");
    if (selectedBox) {
        const selectedBoxId = selectedBox.getAttribute("data-bed-id");
        // Redirect to the correlation chart view with the selected SnailBed ID
        window.location.href = `/barchart/${selectedBoxId}`;
    } else {
        alert("Select a Snail Bed first");
    }
});


// make sure that a Snail Bed is selected when Log Data button is clicked
document.addEventListener("DOMContentLoaded", function () {
    // Get the button element
    var logDataButton = document.getElementById("logDataButton");
    // Add a click event listener to the button
    logDataButton.addEventListener("click", function () {
        const selectedBox = document.querySelector(".snail-box.expanded");
        console.log(selectedBox)
        if (!selectedBox) {
            // If no box is selected, show an alert
            alert("Select a Snail Bed first");
        } else {
            // Show the modal with the specified ID when the button is clicked
            var logDataModal = new bootstrap.Modal(document.getElementById("logDataModal"));
            logDataModal.show();
        }
    });
});

// Toggle the selected snail bed. Unselect the previously selected, then select the clicked on.
// get all its object fields and repopulate the stats box
document.addEventListener("DOMContentLoaded", function () {
    const rectangle = document.querySelector(".rectangle");

    // Toggle box border and display selected data
    function toggleBox(box) {
        const selectedBox = rectangle.querySelector(".snail-box.expanded");
        if (selectedBox) {
            selectedBox.classList.remove("expanded");
        }
        if (box !== selectedBox) {
            box.classList.add("expanded");
            const boxName = box.getAttribute("data-bed-name");
            const boxEmployees = box.getAttribute("data-bed-employee");
            const boxId = box.getAttribute("data-bed-id");
            const boxHatch = box.getAttribute("data-bed-hatch");
            const boxMortality = box.getAttribute("data-bed-mortality");
            const boxMaturity = box.getAttribute("data-bed-maturity");
            const boxFeed = box.getAttribute("data-bed-feed");
            const boxSnails = box.getAttribute("data-bed-snails");

            document.getElementById("box-name").innerText = "Name: " + boxName;

            if ( boxEmployees != "None") { 
                document.getElementById("box-employee").innerHTML = 
                `<p id="box-employee-text"></p>
                <a id="box-unassign-employee" class="btn btn-primary btn-sm">Unassign employee</a>`
                document.getElementById("box-unassign-employee").href = "/unassign_employee/" + boxId;
                document.getElementById("box-employee-text").innerText = "Assigned employee: " + boxEmployees;
            } else { document.getElementById("box-employee").innerText = "Assigned employee: Not assigned";}


            if (boxHatch != "None") { 
                document.getElementById("box-hatch").innerHTML = 
                `<p id="box-hatch-text"></p>
                <a id="box-hatch-history" class="btn btn-primary btn-sm">View Hatch History</a>`
                document.getElementById("box-hatch-history").href = "/view_hatch_rate_history/" + boxId;
                document.getElementById("box-hatch-text").innerText = "Latest Hatch rate: " + boxHatch;
            } else { document.getElementById("box-hatch").innerText = "Latest Hatch rate: No data available"; }



            if (boxMortality != "None") { 
                document.getElementById("box-mortality").innerHTML = 
                `<p id="box-mortality-text"></p>
                <a id="box-mortality-history" class="btn btn-primary btn-sm">View Mortality History</a>`
                document.getElementById("box-mortality-history").href = "/view_mortality_rate_history/" + boxId;
                document.getElementById("box-mortality-text").innerText = "Latest Mortality rate: " + boxMortality;
            } else { document.getElementById("box-mortality").innerText = "Latest Mortality rate: No data available";}


            
            if (boxMaturity != "None") { 
                document.getElementById("box-maturity").innerHTML = 
                `<p id="box-maturity-text"></p>
                <a id="box-maturity-history" class="btn btn-primary btn-sm">View Maturity History</a>`
                document.getElementById("box-maturity-history").href = "/view_maturity_rate_history/" + boxId;
                document.getElementById("box-maturity-text").innerText = "Latest Maturity rate: " + boxMaturity; 
            } else { document.getElementById("box-maturity").innerText = "Latest Maturity rate: No data available";}

            //  Generate Snail Feed statistics and History button
            if (boxFeed != "None") { 
                document.getElementById("box-feed").innerHTML = 
                `<p id="box-feed-text"></p>
                <a id="box-feed-history" class="btn btn-primary btn-sm">View Feed History</a>`
                document.getElementById("box-feed-history").href = "/view_feed_history/" + boxId;
                document.getElementById("box-feed-text").innerText = "Latest Feed given: " + boxFeed;
            } else { document.getElementById("box-feed").innerText = "Latest Feed given: No data available"; }

            //  generate Bed Performance button
            document.getElementById("box-details").innerHTML = 
            `<a class="btn btn-success" id="box-details-link">View Performance</a>`;
            document.getElementById("box-details-link").href = "/bed_performance/" + boxId;

            // generate API button for snail bed details
             document.getElementById("box-api").innerHTML = 
            `<a class="btn btn-warning btn-sm" id="box-api-link" target="_blank">Export as JSON</a>`;
            document.getElementById("box-api-link").href = "/api/specific-snail-bed/" + boxId;
            
            
            document.getElementById("box-snails").innerText = "Snails: " + boxSnails;

            document.getElementById("box-hatch-link").href = "/log_hatch_rate/" + boxId;
            document.getElementById("box-mortality-link").href = "/log_mortality_rate/" + boxId;
            document.getElementById("box-maturity-link").href = "/log_maturity_rate/" + boxId;
            document.getElementById("box-feed-link").href = "/log_snail_feed/" + boxId;

            document.getElementById("selected-box-data").style.display = "block";
        } else {
            document.getElementById("selected-box-data").style.display = "none";
        }
    }

    // Add click event listeners to all snail-box elements
    const snailBoxes = rectangle.querySelectorAll(".snail-box");
    snailBoxes.forEach(function (box) {
        box.addEventListener("click", function () {
            toggleBox(box);
        });
    });
});


//  handle the Delete selected snail bed button
document.addEventListener("DOMContentLoaded", function () {
    // Get the delete button element
    var deleteButton = document.getElementById("delete-snail-bed-button");
    var deleteAllButton = document.getElementById("delete-all-boxes-button");

    // Add a click event listener to the delete button
    deleteButton.addEventListener("click", function () {
        const selectedBox = document.querySelector(".snail-box.expanded");
        if (selectedBox) {
            const selectedBoxId = selectedBox.getAttribute("data-bed-id");
            // Confirm the deletion with a confirmation dialog
            if (confirm("Are you sure you want to delete this Snail Bed?")) {
                // Redirect to the delete view with the selected SnailBed ID
                window.location.href = `/delete_snailbed/${selectedBoxId}`;
            }
        } else {
            alert("Select a Snail Bed first");
        }
    });

    // Add a click event listener to the delete button
    deleteAllButton.addEventListener("click", function () {
        // Confirm the deletion with a confirmation dialog
        if (confirm("Are you sure you want to delete all Snail Beds?")) {
            // Redirect to the delete view with the selected SnailBed ID
            window.location.href = `/delete_all_snailbeds/`;
        }
    });
});