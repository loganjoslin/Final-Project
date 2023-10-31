const max_height = 6
const min_height = 2
const max_width = 8
const min_width = 3

function increase_width() {
    Rows = document.querySelectorAll(".CLASSROW");
    curWidth = Rows[0].querySelectorAll(".col").length
    Column = Rows[0].querySelector(".col");
    if (curWidth < max_width) {
        for (let x = 0, numRows = Rows.length; x < numRows; x++) {
            ColumnClone = Column.cloneNode(true);
            Rows[x].appendChild(ColumnClone);
        }
    }
}

function decrease_width() {
    Rows = document.querySelectorAll(".CLASSROW");
    curWidth = Rows[0].querySelectorAll(".col").length
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

function toggle_partners() {
    desks = document.querySelectorAll(".desk")
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