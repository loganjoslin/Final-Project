let Fronts = [];
let HIncomps = [];
let Comps = [];
let Incomps = [];

//--
// Flipping through the first three pages without backend communication (First Half)
function first_page_change() {
    document.querySelector('#titleOverall').style.display = 'none';
    document.querySelector('#dimensions').style.display= 'block';
}

// Uses "get_dimensions" function to save height/width
function second_page_change() {
    get_dimensions();
    document.querySelector('#dimensions').style.display= 'none';
    ClassContainer = document.querySelector('.CLASSCONTAINER');
    console.log(ClassContainer);
    document.querySelector('#NameList').style.display= 'block';
}

function get_dimensions() {
    // Get height and width
    let height = document.querySelectorAll(".CLASSROW").length;
    let row = document.querySelector(".CLASSROW");
    let width = row.querySelectorAll(".col").length;
    // Double width if partnered mode
    if (document.querySelector(".desk").style.height == "50%") {
        width *= 2;
    }
    document.querySelector('#InputWidth').value = width;
    document.querySelector('#InputHeight').value = height;
}


//--
// Flipping through the last three pages without backend communication (Second Half)
// First flip.
function comps_to_fronts() {

    // Save comps + incomps. Copy incomp nodes to Hincomp table.
    document.querySelector("#InfoTitle").style.display = 'none';
    let FinalTableBody = document.querySelector("#FinalTableBody");
    let redRows = document.querySelectorAll(".redRow");
    let greenRows = document.querySelectorAll(".greenRow");
    let Rows = [redRows, greenRows];
    for (let x = 0; x < Rows.length; x++) {
        for (let y = 0; y < Rows[x].length; y++) {
            pair = Rows[x][y].querySelectorAll(".S")
            let cleanPair = [pair[0].innerHTML, pair[1].innerHTML];
            if (x == 0) {
                Incomps.push(cleanPair);
            } else {
                Comps.push(cleanPair);
            }

            // Saving red rows to Hincomp table
            if (x == 0) {
                let RowDup = Rows[x][y].cloneNode(true);
                RowDup.classList.add("FinalRow");
                FinalTableBody.appendChild(RowDup);
            }
        }
    }

    // Animations
    document.querySelector("#compTables").style.display = 'none';
    document.querySelector("#NextButton").style.display = 'none';
    document.querySelector("#StudentSelection").style.marginTop = '265px';
    document.querySelector("#StudentSelection").style.animation = 'topSlide 1s';
    document.querySelector(".FrontDesc").style.display = "block";
    document.querySelector(".FrontDesc").style.animation = "fadeIn 1s";
    setTimeout(function() {
        document.querySelector("#StudentSelection").style.marginTop = '25px';
        document.querySelector("#StudentSelection").style.backgroundColor = 'rgba(255, 222, 173, 0.5)';
        document.querySelector("#StudentSelection").style.border = '2px solid rgba(255, 222, 173, 1.0)';
        document.querySelector(".FrontDesc").style.opacity = "1";
    }, 950);
}

// Second Flip. Save Fronts.
// Some of this code is in the HTML
function save_fronts(SelectedStudents) {
    for (let x = 0; x < SelectedStudents.length; x++) {
        Fronts.push(SelectedStudents[x].innerHTML);
    }
    console.log("Fronts: " + Fronts);
}

// Third Flip. Save HIncomp.
function HI_to_loading() {
    for (let n = 0; n < SelectedRows.length; n++) {
        pair = SelectedRows[n].querySelectorAll(".S");
        cleanPair = [pair[0].innerHTML, pair[1].innerHTML];
        HIncomps.push(cleanPair);
    }
    document.querySelector('#FinalTable').style.animation = "fadeOut 0.5s"
    setTimeout(function() {
        document.querySelector('#FinalTable').style.display = 'none';
        document.querySelector('#LoadingScreen').style.display = 'block';
        document.querySelector('#LoadingScreen').style.animation = 'fadeIn 0.5s';
        setTimeout(function() {
            document.querySelector('#LoadingScreen').style.opacity = '1';
            send_lists();
        }, 450);
    }, 450);
}

// Send all our data to the backend with JSON
function send_lists() {
    // Store all lists
    let lists = {
        HIncomps: HIncomps,
        Incomps: Incomps,
        Comps: Comps,
        Fronts: Fronts
    };

    // Start an AJAX request
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/generate', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                response = JSON.parse(xhr.responseText);
                load_plan(response);
            } else {
                console.error("Error Sending");
            }
        }
    };

    xhr.send(JSON.stringify(lists));
}

// Load the final seating plan based on response from backend
function load_plan(response) {
    let PlanContainer = document.querySelector('#plan');
    let Assignments = response['Ass'];
    let Height = response['Height'];
    let Width = response['Width'];
    let Partners = response['Partners'];
    let F = response["Fronts"];
    let HI = response["HI"];
    let rowHeight = (95 / Height) + "%"
    console.log("HI:" + HI);

    let DeskHeight = '100%';
    let DeskNameJustify = 'justify-content-center';
    let jump = 1;
    if (Partners) {
        jump = 2;
        DeskHeight = '50%';
        DeskNameJustify = 'justify-content-around';
        console.log("Adjusted settingd for partners mode")
    }

    for (let y = 0; y < Height; y++) {
        row = document.createElement('div');
        row.classList.add('row');
        row.style.height = rowHeight;
        for (let x = 0; x < Width; x += jump) {
            let col = document.createElement('div');
            col.classList.add('col', 'd-flex', 'align-items-center', 'justify-content-center', 'p-2', 'p-lg-3');

            let desk = document.createElement('div');
            desk.classList.add('d-flex', 'align-items-center', DeskNameJustify);
            desk.style.width = '100%';
            desk.style.backgroundColor = 'rgba(173, 216, 230, 0.5)';
            desk.style.borderRadius = '10px';
            desk.style.height = DeskHeight;

            let NameBox2;
            let NameBox = document.createElement('span');
            NameBox.classList.add("NameBox");
            if (Partners) {
                NameBox2 = document.createElement('span');
                NameBox2.classList.add("NameBox");
            }

            // Find corresponding coordinates in Assignments. If not found, name=empty.
            for (let n = 0; n < jump; n++) {
                let found = false;
                for (let name in Assignments) {
                    let coords = Assignments[name];
                    if (coords[0] == x + n && coords[1] == y) {
                        found = true;
                        if (n == 0) {
                            NameBox.innerHTML = name;
                            for (let v = 0; v < F.length; v++) {
                                if (name == F[v]) {
                                    NameBox.style.backgroundColor = 'rgba(255, 222, 173, 0.7)';
                                }
                            }
                        } else {
                            NameBox2.innerHTML = name;
                            for (let v = 0; v < F.length; v++) {
                                if (name == F[v]) {
                                    NameBox.style.backgroundColor = 'rgba(255, 222, 173, 0.7)';
                                }
                            }
                        }
                        break;
                    }
                }
                if (!found) {
                    if (n == 0) {
                        NameBox.innerHTML = 'empty';
                    } else {
                        NameBox2.innerHTML = 'empty';
                    }
                }
                desk.appendChild(NameBox);
                if (Partners) {
                    desk.appendChild(NameBox2);
                }
            }
            col.appendChild(desk);
            row.appendChild(col);
        }
        PlanContainer.appendChild(row);
    }

    // When all elements are created, display plan==block and display loadingscreen==none
    document.querySelector('#LoadingScreen').style.display = "none";
    PlanContainer.style.display = 'block';
    document.querySelector("#compTables").style.display = "block";
    document.querySelector("#redPlusButton").style.display = "none";
    document.querySelector("#greenPlusButton").style.display = "none";

    // Hover to highlight functionality
    redRows = document.querySelectorAll(".redRow");
    greenRows = document.querySelectorAll(".greenRow");
    rows = [redRows, greenRows];
    for (let t = 0; t < rows.length; t++) {
        for (let u = 0; u < rows[t].length; u++) {
            rows[t][u].addEventListener("mouseover", Highlight);
            rows[t][u].addEventListener("mouseout", function(event) {
                unHighlight(event, F);
            });
            rows[t][u].removeEventListener("click", remove_row);

            // + Highlight HI rows in RED
            if (t == 0) {
                let students = rows[t][u].querySelectorAll(".S");
                for (let k = 0; k < HI.length; k++) {
                    if ((students[0].innerHTML == HI[k][0] || students[0].innerHTML == HI[k][1]) && (students[1].innerHTML == HI[k][0] || students[1].innerHTML == HI[k][1])) {
                        rows[t][u].style.backgroundColor = "rgba(220, 20, 60, 0.5)";
                    }
                }
            }
        }
    }
}

function Highlight(event) {
    let HoveredRow = event.currentTarget;
    let StudentPair = HoveredRow.querySelectorAll(".S");

    let NameBoxes = document.querySelectorAll(".NameBox");
    for (let n = 0; n < NameBoxes.length; n++) {
        if ((StudentPair[0].innerHTML == NameBoxes[n].innerHTML) || (StudentPair[1].innerHTML == NameBoxes[n].innerHTML)) {
            if (HoveredRow.classList.contains("redRow")) {
                NameBoxes[n].style.backgroundColor = "rgba(220, 20, 60, 0.5)";
            } else {
                NameBoxes[n].style.backgroundColor = "rgba(34, 139, 34, 0.5)";
            }
        }
    }
}
function unHighlight(event, F) {
    let UnHoveredRow = event.currentTarget;
    let StudentPair = UnHoveredRow.querySelectorAll(".S");

    let NameBoxes = document.querySelectorAll(".NameBox");
    for (let n = 0; n < NameBoxes.length; n++) {
        if ((StudentPair[0].innerHTML == NameBoxes[n].innerHTML) || (StudentPair[1].innerHTML == NameBoxes[n].innerHTML)) {
            NameBoxes[n].style.backgroundColor = "rgba(173, 216, 230, 0.2)";
            for (let z = 0; z < F.length; z++) {
                if (NameBoxes[n].innerHTML == F[z]) {
                    NameBoxes[n].style.backgroundColor = 'rgba(255, 222, 173, 0.7)';
                }
            }
        }
    }
}


//--
// Classroom Dimensions selection page
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
        row = document.querySelector(".CLASSROW");
        rowClone = row.cloneNode(true);
        rowsContainer = document.querySelector(".CLASSCONTAINER");
        rowsContainer.appendChild(rowClone);
        rows = document.querySelectorAll(".CLASSROW");
        listLength = rows.length;
        for (let x = 0; x < listLength; x++) {
            rows[x].style.height = (95 / listLength) + "%";
        }
    }
}

function decrease_height() {
    let rows = document.querySelectorAll(".CLASSROW");
    let listLength = rows.length;
    if (listLength > min_height) {
        rowsContainer = document.querySelector(".CLASSCONTAINER");
        row = document.querySelector(".CLASSROW");
        rowsContainer.removeChild(row);
        rows = document.querySelectorAll(".CLASSROW");
        listLength = rows.length;
        for (let x = 0; x < listLength; x++) {
            rows[x].style.height = (95 / listLength) + "%";
        }
    }       
}

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
            document.querySelector('#InputPartners').value = "False";
        } else {
            desks[x].style.height = "50%";
            desks[x].classList.remove("justify-content-center");
            desks[x].classList.add("justify-content-around");
            desks[x].appendChild(iconDUP);
            document.querySelector('#InputPartners').value = "True";
        }
    }
}



//--
// Incomp/compatible student selection page.
// Some script is stored in the HTML
const IncompBG = 'rgba(220, 20, 60, 0.1)';
const CompBG = 'rgba(34, 139, 34, 0.1)';

function bg_green() {
    Container = document.querySelector("#StudentSelection");
    Container.style.backgroundColor = CompBG;
    Container.style.border = "2px solid forestgreen";
}
function bg_red() {
    Container = document.querySelector("#StudentSelection");
    Container.style.backgroundColor = IncompBG;
    Container.style.border = "2px solid crimson";
}

// CLEAN THIS FUNCTION
function save_pair(S1, S2) {
    let Name1_cell = document.createElement('td');
    Name1_cell.textContent = S1.innerHTML;
    Name1_cell.classList.add("S");
    Name1_cell.style.width = "33%";

    let Plus = document.createElement('td');
    Plus.textContent = "+";
    Plus.style.width = "33%";

    let Name2_cell = document.createElement('td');
    Name2_cell.textContent = S2.innerHTML;
    Name2_cell.classList.add("S");
    Name2_cell.style.width = "33%";

    let row = document.createElement('tr')
    row.appendChild(Name1_cell);
    row.appendChild(Plus);
    row.appendChild(Name2_cell);
    row.addEventListener('click', remove_row);

    // Find current selecction area background color to appoint students properly.
    SelectionArea = document.querySelector('#StudentSelection');
    let backgroundColor = window.getComputedStyle(SelectionArea).getPropertyValue('background-color');

    // Add students to proper tables
    let GreenBody = document.querySelector('#greenTable');
    let RedBody = document.querySelector('#redTable');

    if (backgroundColor == IncompBG) {
        row.classList.add("redRow");
        row.style.borderBottom = "1px solid rgba(220,20,60,0.2)";
        RedBody.appendChild(row);
    } else {
        row.classList.add("greenRow");
        row.style.borderBottom = "1px solid rgba(34,139,34,0.2)";
        GreenBody.appendChild(row);
    }
    let rowNum = document.querySelectorAll('tr').length;
    if (rowNum == 10) {
        document.querySelector('#NextButton').style.display = 'block';
        document.querySelector('.tables').style.marginTop = '10px';
    }
}
// Remove incomp pair in Student Selection page
function remove_row(event) {
    event.currentTarget.remove();
}



//--
// Selecting students in the Final Table
SelectedRows = [];
function select_incomp_pair(event) {
    row = event.currentTarget;
    if (SelectedRows.indexOf(row) === -1 && SelectedRows.length < 2) {
        row.style.backgroundColor = "rgba(220,20,60,0.2)";
        SelectedRows.push(row);
    } else if (SelectedRows.indexOf(row) !== -1) {
        row.style.backgroundColor = "rgba(220,20,60,0.0)";
        index = SelectedRows.indexOf(row);
        SelectedRows.splice(index, 1);
    }
}
function mouse_over_incomp(event) {
    row = event.currentTarget
    if (SelectedRows.indexOf(row) === -1) {
        row.style.backgroundColor = "rgba(220,20,60,0.2)";
    }
}
function mouse_out_incomp(event) {
    row = event.currentTarget
    if (SelectedRows.indexOf(row) === -1) {
        row.style.backgroundColor = "rgba(220,20,60,0.0)";
    }
}