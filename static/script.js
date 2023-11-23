// All JS for Classroom Dimensions selection page-------

const max_height = 6
const min_height = 2
const max_width = 8
const min_width = 3

function increase_width() {
    let Rows = document.querySelectorAll(".CLASSROW");
    let curWidth = Rows[0].querySelectorAll(".col").length
    let Column = Rows[0].querySelector(".col");
    if (curWidth < max_width) {
        for (let x = 0, numRows = Rows.length; x < numRows; x++) {
            ColumnClone = Column.cloneNode(true);
            Rows[x].appendChild(ColumnClone);
        }
    }
}

function decrease_width() {
    let Rows = document.querySelectorAll(".CLASSROW");
    let curWidth = Rows[0].querySelectorAll(".col").length
    if (curWidth > min_width) {
        for (let x = 0, numRows = Rows.length; x < numRows; x++) {
            column = Rows[x].querySelector(".col");
            Rows[x].removeChild(column);
        }
    }
}

function increase_height() {
    let rows = document.querySelectorAll(".CLASSROW");
    let listLength = rows.length;
    if (listLength < max_height) {
        // Add another row
        row = document.querySelector(".CLASSROW");
        rowClone = row.cloneNode(true);
        rowsContainer = document.querySelector(".CLASSCONTAINER");
        rowsContainer.appendChild(rowClone);
        // New list length
        rows = document.querySelectorAll(".CLASSROW");
        listLength = rows.length;
        // Adjust row height
        for (let x = 0; x < listLength; x++) {
            rows[x].style.height = (95 / listLength) + "%";
        }
    }
}

function decrease_height() {
    let rows = document.querySelectorAll(".CLASSROW");
    let listLength = rows.length;
    if (listLength > min_height) {
        // Remove row
        rowsContainer = document.querySelector(".CLASSCONTAINER");
        row = document.querySelector(".CLASSROW");
        rowsContainer.removeChild(row);
        // New list length
        rows = document.querySelectorAll(".CLASSROW");
        listLength = rows.length;
        // Adjust row height
        for (let x = 0; x < listLength; x++) {
            rows[x].style.height = (95 / listLength) + "%";
        }
    }       
}

// Change between partnered desk/single desk mode
function toggle_partners() {
    let desks = document.querySelectorAll(".desk")
    for (let x = 0, len = desks.length; x < len; x++) {
        icon = desks[x].querySelector(".bi-emoji-smile");
        iconDUP = icon.cloneNode(true)
        if (desks[x].style.height == "50%") {
            desks[x].style.height = "100%";
            desks[x].classList.remove("justify-content-around");
            desks[x].classList.add("justify-content-center");
            desks[x].removeChild(icon);
        } else {
            desks[x].style.height = "50%";
            desks[x].classList.remove("justify-content-center");
            desks[x].classList.add("justify-content-around");
            desks[x].appendChild(iconDUP);
        }
    }
}

// Return selected dimensions to the server for processing
function get_dimensions() {
    // Get height and width
    let height = document.querySelectorAll(".CLASSROW").length;
    let row = document.querySelector(".CLASSROW");
    let width = row.querySelectorAll(".col").length;
    // Double width if partnered mode
    if (document.querySelector(".desk").style.height == "50%") {
        width *= 2;
    }
    document.querySelector("#submitWidth").value = width;
    document.querySelector("#submitHeight").value = height;
    if (width < min_width || width > max_width || height > max_height || height < min_height) {
        return false;
    }
    return true;
}


// All JS for incomp/compatible student selection page.
// Some script is stored in the HTML

// Background colours for student selection area
function bg_green() {
    Container = document.querySelector("#StudentSelection");
    Container.style.backgroundColor = "rgba(34, 139, 34, 0.1)";
    Container.style.border = "2px solid forestgreen";
}
function bg_red() {
    Container = document.querySelector("#StudentSelection");
    Container.style.backgroundColor = "rgba(220, 20, 60, 0.1)";
    Container.style.border = "2px solid crimson";
}

// Store selected student pair in table
function save_pair(S1, S2) {
    // Create table content
    let Name1_cell = document.createElement('td');
    Name1_cell.textContent = S1.innerHTML;

    let Plus = document.createElement('td');
    Plus.textContent = "+";

    let Name2_cell = document.createElement('td');
    Name2_cell.textContent = S2.innerHTML;

    let row = document.createElement('tr')
    row.appendChild(Name1_cell);
    row.appendChild(Plus);
    row.appendChild(Name2_cell);
    row.addEventListener('click', remove_row);

    // Find current selecction area background color to appoint students properly.
    SelectionArea = document.querySelector('#StudentSelection');
    let backgroundColor = window.getComputedStyle(SelectionArea).getPropertyValue('background-color');

    // Add students to table
    let GreenBody = document.querySelector('#greenTable');
    let RedBody = document.querySelector('#redTable');

    console.log(backgroundColor + " this color")
    if (backgroundColor == 'rgba(220, 20, 60, 0.1)') {
        RedBody.appendChild(row);
    } else {
        GreenBody.appendChild(row);
    }

    let rowNum = document.querySelectorAll('tr').length;
    if (rowNum == 10) {
        document.querySelector('.NextButton').style.display = 'block';
        document.querySelector('.tables').style.marginTop = '10px'
    }
}

function remove_row(event) {
    event.currentTarget.remove();
}