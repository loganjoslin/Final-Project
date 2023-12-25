// Key user input data to be processed in "seating.py" algorithm
let Fronts = [];
let HIncomps = [];
let Comps = [];
let Incomps = [];


// == ==
//// Seamless movement through "index.html" (Page1) == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
// == ==

function title_to_dimensions() {
    let ElementsToFadeOut = ["#titleOverall"];
    let ElementsToFadeIn = ["#dimensions"];
    fade(ElementsToFadeOut, ElementsToFadeIn);
}

function dimensions_to_namelist() {
    // Save height/width of grid
    let rows = document.querySelectorAll(".CLASSROW")
    let height = rows.length;
    let width = rows[0].querySelectorAll(".col").length;
    // Double width if partnered mode
    if (document.querySelector(".desk").style.height == PartnerModeDeskHeight) {
        width *= 2;
    }
    if ((width >= 4) && (height * width >= 16)) {
        document.querySelector('#InputWidth').value = width;
        document.querySelector('#InputHeight').value = height;
        // Animation
        let ElementsToFadeOut = ['#dimensions'];
        let ElementsToFadeIn = ['#NameList'];
        fade(ElementsToFadeOut, ElementsToFadeIn);
    } else {
        alert("Class must be at least 4 single desks wide and have space for at least 16 students!")
    }
}


// == ==
//// "index.html" buttons/functionality (Page1) == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
// == ==

const max_height = 6
const min_height = 3
const max_width = 8
const min_width = 3
const PrcntgeOfHeight = 95;
const PartnerModeDeskHeight = "60%";
const FullHeight = "100%";

function increase_width() {
    let rows = document.querySelectorAll(".CLASSROW");
    let curWidth = rows[0].querySelectorAll(".col").length
    let col = rows[0].querySelector(".col");
    if (curWidth < max_width) {
        for (let x = 0; x < rows.length; x++) {
            ColumnClone = col.cloneNode(true);
            rows[x].appendChild(ColumnClone);
        }
    }
}

function decrease_width() {
    let rows = document.querySelectorAll(".CLASSROW");
    let curWidth = rows[0].querySelectorAll(".col").length
    if (curWidth > min_width) {
        for (let x = 0; x < rows.length; x++) {
            let col = rows[x].querySelector(".col");
            rows[x].removeChild(col);
        }
    }
}

// The rows should only take "PrcntgeOfHeight" % 
// of the total container height. 
// See "Dimension Selection Page" in "index.html"

function increase_height() {
    let rows = document.querySelectorAll(".CLASSROW");
    if (rows.length < max_height) {
        rowClone = rows[0].cloneNode(true);
        rowsContainer = document.querySelector(".CLASSCONTAINER");
        rowsContainer.appendChild(rowClone);
        rows = document.querySelectorAll(".CLASSROW");
        for (let x = 0; x < rows.length; x++) {
            rows[x].style.height = (PrcntgeOfHeight / rows.length) + "%";
        }
    }
}

function decrease_height() {
    let rows = document.querySelectorAll(".CLASSROW");
    if (rows.length > min_height) {
        rowsContainer = document.querySelector(".CLASSCONTAINER");
        row = document.querySelector(".CLASSROW");
        rowsContainer.removeChild(row);
        rows = document.querySelectorAll(".CLASSROW");
        for (let x = 0; x < rows.length; x++) {
            rows[x].style.height = (PrcntgeOfHeight / rows.length) + "%";
        }
    }       
}

// Change between single/partnered desk mode.
// This affects the algorithm along with class width/layout.
function toggle_partners() {
    let desks = document.querySelectorAll(".desk")
    for (let x = 0; x < desks.length; x++) {
        icon = desks[x].querySelector(".bi-emoji-smile");
        iconDUP = icon.cloneNode(true)
        if (desks[x].style.height == PartnerModeDeskHeight) {
            desks[x].style.height = FullHeight;
            desks[x].classList.remove("justify-content-around");
            desks[x].classList.add("justify-content-center");
            desks[x].removeChild(icon);
            document.querySelector('#InputPartners').value = "False";
        } else {
            desks[x].style.height = PartnerModeDeskHeight;
            desks[x].classList.remove("justify-content-center");
            desks[x].classList.add("justify-content-around");
            desks[x].appendChild(iconDUP);
            document.querySelector('#InputPartners').value = "True";
        }
    }
}

// Ensure user inputted name list is not too long
const MinimumNames = 8;
function check_namelist() {
    let names = document.querySelector("#nameList").value.split(/[;,\s\n]+/);
    let numlist = []
    // Remove empty names
    for (let x = 0; x < names.length; x++) {
        if (names[x] == '') {
            numlist.push(x)
        }
    }
    for (let y = 0; y < numlist.length; y++) {
        names.splice(numlist[y], 1);
    }
    let width = parseInt(document.querySelector("#InputWidth").value);
    let height = parseInt(document.querySelector("#InputHeight").value);
    if (names.length > height * width) {
        alert("There are not enough seats for this many students!");
        return false;
    } else if (names.length < MinimumNames) {
        alert("You must input at least " + MinimumNames + " names!");
        return false;
    }
    let counts = {};
    for (let z = 0; z < names.length; z++) {
        if (!counts[names[z]]) {
            counts[names[z]] = 1;
        } else {
            alert("You inputted '" + names[z] + "' more than once! Try adding this student's lastname with a dot.");
            return false;
        }
        if (names[z].length > 10) {
            alert("' " + names[z] + " ' is too long. Try to abbreviate names that are longer than 10 characters.");
            return false;
        }
    }
    return true;
}


// == ==
//// Seamless movement through "compatibles.html" (page2) == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
// == ==

function comps_to_fronts() {
    // Save Comp/Incomp pairs.
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
            // Copy Incomp pairs to HI selection table.
            if (x == 0) {
                let RowDup = Rows[x][y].cloneNode(true);
                RowDup.classList.add("FinalRow");
                FinalTableBody.appendChild(RowDup);
            }
        }
    }
    // Custom Animation
    comps_to_fronts_animation();
}

function fronts_to_HI() {
    // Save Fronts
    for (let x = 0; x < SelectedStudents.length; x++) {
        Fronts.push(SelectedStudents[x].innerHTML);
    }
    // Fade Animations
    let ElementsToFadeOut = ["#StudentSelectionRow", ".FrontDesc"];
    let ElementsToFadeIn = ["#FinalTable"];
    fade(ElementsToFadeOut, ElementsToFadeIn);
    // Add row selection functionality
    IncompTableRows = document.querySelectorAll(".FinalRow");
    for (let x = 0; x < IncompTableRows.length; x++) {
        IncompTableRows[x].addEventListener("click", select_HI_pair);
        IncompTableRows[x].addEventListener("mouseover", mouse_over_HI_pair);
        IncompTableRows[x].addEventListener("mouseout" , mouse_out_HI_pair);
    }
}

function HI_to_loading() {
    // Save HI
    for (let n = 0; n < SelectedHIRows.length; n++) {
        let pair = SelectedHIRows[n].querySelectorAll(".S");
        let cleanPair = [pair[0].innerHTML, pair[1].innerHTML];
        HIncomps.push(cleanPair);
    }
    // Fade Animations to loading screen
    let ElementsToFadeOut = ['#FinalTable'];
    let ElementsToFadeIn = ['#LoadingScreen'];
    fade(ElementsToFadeOut, ElementsToFadeIn);
    // Start AJAX request
    setTimeout(function() {
        send_lists();
    }, 500);
}


// == ==
//// "compatibles.html" buttons/functionality (Page2) == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
// == ==

const IncompBG = 'rgba(220, 20, 60, 0.1)';
const CompBG = 'rgba(34, 139, 34, 0.1)';
const DarkBG = 'rgb(80, 172, 203)';
const LightBG = 'rgb(173, 216, 230)';
const DBLclickBorder = '2px solid crimson'

const FrontLimit = 3;
const MaxIncompPairAreaDivisor = 2;
const MaxCompPairAreaDivisor = 1.5;
const NxtBtnDivisor = 2.5;

let maxChoices = 2;
let FirstPage = true;
let IsolateMode = false;
let SelectedStudents = [];
let DBLclickSelected = null;

// Give SHORT, MEDIUM, and LONG classes to student names for responsiveness
function give_name_size() {
    let students = document.querySelectorAll(".student")
    for (let x = 0; x < students.length; x++) {
        let nameLength = students[x].innerHTML.length;
        if (nameLength > 7) {
            students[x].classList.add("LONG");
        } else if (nameLength > 5 && nameLength <= 7) {
            students[x].classList.add("MEDIUM");
        } else {
            students[x].classList.add("SHORT");
        }
    }
}

// Reconfigures "select_student()" function for F selection area
function FrontSwitch() {
    IsolateMode = false;
    FirstPage = false;
    for (let n = 0; n < SelectedStudents.length; n++) {
        SelectedStudents[n].style.backgroundColor = LightBG;
    }
    SelectedStudents = [];
    DBLclickSelected = null;
    maxChoices = FrontLimit;
    comps_to_fronts();
}

// Selecting Students for C, I, and F.
function select_student(event) {
    let selected = event.target;
    let index = SelectedStudents.indexOf(selected);
    if (index === -1 && SelectedStudents.length < maxChoices) {
        selected.style.backgroundColor = DarkBG;
        SelectedStudents.push(selected);
    } else if (index !== -1) {
        selected.style.backgroundColor = LightBG;
        selected.style.border = "none";
        SelectedStudents.splice(index, 1);
            if (selected == DBLclickSelected) {
            IsolateMode = false;
            DBLclickSelected = null;
            }
    }
    if (FirstPage && SelectedStudents.length == 2) {
        save_pair(SelectedStudents[0], SelectedStudents[1]);
        // Keep the first student selected if in Isolate Mode
        if (IsolateMode) {
            SelectedStudents.splice(1, 1);
        } else {
            SelectedStudents[0].style.backgroundColor = LightBG;
            SelectedStudents = [];
        }
    }
}

// Store selected pair in COMP/INCOMP table.
function save_pair(S1, S2) {

    // Create row with names
    let Name_cell_1 = document.createElement('td');
    Name_cell_1.textContent = S1.innerHTML;
    Name_cell_1.classList.add("S");
    Name_cell_1.style.width = "33%";
    let Name_cell_2 = document.createElement('td');
    Name_cell_2.textContent = S2.innerHTML;
    Name_cell_2.classList.add("S");
    Name_cell_2.style.width = "33%";
    let Plus = document.createElement('td');
    Plus.textContent = "+";
    Plus.style.width = "33%";
    let row = document.createElement('tr');
    row.appendChild(Name_cell_1);
    row.appendChild(Plus);
    row.appendChild(Name_cell_2);
    row.addEventListener('click', remove_row);

    // Get current background color to determine whether we are in COMPATIBLE or INCOMPATIBLE mode
    let SelectionGrid = document.querySelector('#StudentSelection');
    let backgroundColor = window.getComputedStyle(SelectionGrid).getPropertyValue('background-color');

    // Adjust values depending on COMPATIBLE or INCOMPATIBLE selection mode
    let TableBody;
    let ThisTableRows;
    let ClassName;
    let BottomBorderColor;
    let OtherTableRows;
    if (backgroundColor == IncompBG) {
        ClassName = "redRow";
        TableBody = document.querySelector('#redTable');
        ThisTableRows = document.querySelectorAll(".redRow");
        OtherTableRows = document.querySelectorAll(".greenRow");
        BottomBorderColor = "1px solid rgba(220,20,60,0.2)";      
    } else {
        ClassName = "greenRow";
        TableBody = document.querySelector('#greenTable');
        ThisTableRows = document.querySelectorAll(".greenRow");
        OtherTableRows = document.querySelectorAll(".redRow");
        BottomBorderColor = "1px solid rgba(34,139,34,0.2)";
    }

    // Filter 1:
    // If COMPS: Block inputs that already exist in either of the tables
    let counts = {}
    counts[S1.innerHTML] = 1
    counts[S2.innerHTML] = 1
    let AddPair = true;
    let Both = [ThisTableRows, OtherTableRows];
    for (let m = 0; m < Both.length; m++) {
        for (let n = 0; n < Both[m].length; n++) {
            let contents = Both[m][n].querySelectorAll(".S");
            if ((S1.textContent == contents[0].textContent || S1.textContent == contents[1].textContent)
            && (S2.textContent == contents[0].textContent || S2.textContent == contents[1].textContent)) {
                if (m == 0) {
                    alert("This pair already exists in your table!");
                } else {
                    alert("This pair already exists in the other table. Students cannot be both compatible AND incompatible!");
                }
                AddPair = false;
                break;
            }
            // Count each student in this table for Filter 2
            // S1 and S2 aren't in the table yet, so I manually added them to the counts
            // dictionary after initializing it.
            if (m==0) {
                for (let o = 0; o < contents.length; o++) {
                    let name = contents[o].innerHTML.trim();
                    if (counts[name]) {
                        counts[name]++;
                    } else {
                        counts[name] = 1;
                    }
                }
            }
        }
    }
    // Filter 2:
    // If COMPS: Block inputs that exceed the partner limit
    // Limit user inputs
    let PartnerLimit = 2;
    let StudentListLength = document.querySelectorAll(".student").length;
    if (document.querySelector('#PartnerMode').innerHTML.trim() == "True") {
        PartnerLimit = 1;
    }
    // If INCOMPS: Block inputs that exceed "AREA / MaxIncompPairAreaDivisor" (Arbitrary)
    let IncompLimit = StudentListLength / MaxIncompPairAreaDivisor;

    if (AddPair) {
        for (let name in counts) {
            console.log("Counts: " + name + ": " + counts[name]);
            if (counts[name] > PartnerLimit && ClassName == "greenRow") {
                if (PartnerLimit == 1) {
                    alert("Each student may only have 1 compatible partner if the desks are partnered!");
                } else {
                    alert("Each student may only have 2 compatible partners");
                }
                AddPair = false;
                break;
            }
            else if (counts[name] > IncompLimit && ClassName == "redRow") {
                alert(name + " appears too often in your incomp table!");
                AddPair = false;
            }
        }
    }
    // Filter 3:
    // IF COMPS: Limit the amount of COMP pairs allowed
    if (ClassName == "greenRow" && (ThisTableRows.length >= StudentListLength / MaxCompPairAreaDivisor)) {
        alert("You have inputted too many COMP pairs! Remove a pair from the green table to select another pair.");
        AddPair = false;
    }


    // Save pair if it passed all the checks
    if (AddPair) {
        row.classList.add(ClassName);
        row.style.borderBottom = BottomBorderColor;
        TableBody.appendChild(row);    
    }

    // Display the "next" button once user has made "RevealNextBtnAt" selections
    let rowNum = document.querySelectorAll('tr').length;
    let RevealNextBtnAt = (StudentListLength / NxtBtnDivisor);
    if (rowNum >= RevealNextBtnAt) {
        document.querySelector('#NextButton').style.display = 'block';
        document.querySelector('.tables').style.marginTop = '10px';
    }
}


// Double click to permanently select a student when chosing INCOMPS
function isolate_mode(event) {
    let backgroundColor = window.getComputedStyle(document.querySelector('#StudentSelection')).getPropertyValue('background-color');
    if (FirstPage && (backgroundColor == IncompBG) && !IsolateMode) {
        IsolateMode = true;
        DBLclickSelected = event.target;
        DBLclickSelected.style.border = DBLclickBorder;
        DBLclickSelected.style.backgroundColor = DarkBG;
        SelectedStudents.push(DBLclickSelected);
    }
}

// Highlight in dark blue when hovering over student
function mouse_over_student(event) {
    let selected = event.target;
    if (SelectedStudents.indexOf(selected) === -1) {
        selected.style.backgroundColor = DarkBG;
    }
}
function mouse_out_student(event) {
    let selected = event.target;
    if (SelectedStudents.indexOf(selected) === -1) {
        selected.style.backgroundColor = LightBG;
    }
}

// Deselect all students when user clicks away from grid
function deselect_all(event) {
    let buttons = document.querySelectorAll('.student');
    let ClickedOnButton = false;
    for (let x = 0; x < buttons.length; x++) {
        if (buttons[x].contains(event.target)) {
            ClickedOnButton = true;
        }
    }
    if (!ClickedOnButton) {
        IsolateMode = false;
        DBLclickSelected = null;
        SelectedStudents = [];
        for (let x = 0; x < buttons.length; x++) {
            buttons[x].style.backgroundColor = LightBG;
            buttons[x].style.border = "none";
        }
    }
}

// Remove pair when clicked
function remove_row(event) {
    event.currentTarget.remove();
    let rowNum = document.querySelectorAll('tr').length;
    let StudentListLength = document.querySelectorAll(".student").length;
    let RevealNextBtnAt = (StudentListLength / NxtBtnDivisor);
    if (rowNum < RevealNextBtnAt) {
        document.querySelector('#NextButton').style.display = 'none';
        document.querySelector('.tables').style.marginTop = '35px';
    }
}

// Selecting students in the Final Table
let SelectedHIRows = [];
const SelectedHIpairBG = "rgba(220, 20, 60, 0.2)";
const UnSelectedBG = "rgba(220, 20, 60, 0.0)";
function select_HI_pair(event) {
    row = event.currentTarget;
    if (SelectedHIRows.indexOf(row) === -1 && SelectedHIRows.length < 2) {
        row.style.backgroundColor = SelectedHIpairBG;
        SelectedHIRows.push(row);
    } else if (SelectedHIRows.indexOf(row) !== -1) {
        row.style.backgroundColor = UnSelectedBG;
        index = SelectedHIRows.indexOf(row);
        SelectedHIRows.splice(index, 1);
    }
}
function mouse_over_HI_pair(event) {
    console.log("Triggered");
    row = event.currentTarget
    if (SelectedHIRows.indexOf(row) === -1) {
        row.style.backgroundColor = SelectedHIpairBG;
    }
}
function mouse_out_HI_pair(event) {
    row = event.currentTarget
    if (SelectedHIRows.indexOf(row) === -1) {
        row.style.backgroundColor = UnSelectedBG;
    }
}

// Switching background colour
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


// == ==
//// AJAX request and final seating plan generation == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
// == ==

function send_lists() {
    // Store user inputted data
    let lists = {
        HIncomps: HIncomps,
        Incomps: Incomps,
        Comps: Comps,
        Fronts: Fronts
    };
    console.log("HIncomps: " + HIncomps.length)
    console.log("Incomps: " + Incomps.length)
    console.log("Comps: " + Comps.length)
    console.log("Fronts: " + Fronts.length)
    // Start an AJAX request
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/generate', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                console.log("IMPORTANT: " + xhr.responseText);
                response = JSON.parse(xhr.responseText);
                load_plan(response);
            } else {
                console.error("Error Sending");
                // TODO: redirect user if request was unsuccesful
            }
        }
    };
    xhr.send(JSON.stringify(lists));
}

// Load the final seating plan based on response from backend
const DESK_MINWIDTH = 150;
function load_plan(response) {
    // Check for Timeout
    if (response['Timeout']) {
        console.log("timout")
        document.querySelector('#LoadingScreen').style.display = "none";
        document.querySelector('#Timeout').style.display = "block";
        return
    }
    console.log("no timeout")
    // Backend response data
    let Assignments = response['Ass'];
    let Height = response['Height'];
    let Width = response['Width'];
    let Partners = response['Partners'];
    let F = response["Fronts"];
    let HI = response["HI"];

    let PlanContainer = document.querySelector('#plan');
    let rowHeight = (PrcntgeOfHeight / Height) + "%";

    // Adjust settings if PARTNERS mode
    let DeskHeight = '100%';
    let DeskNameJustify = 'justify-content-center';
    let jump = 1;
    if (Partners) {
        jump = 2;
        DeskHeight = PartnerModeDeskHeight;
        DeskNameJustify = 'justify-content-around';
        console.log("Adjusted settings for partners mode")
    }

    // Aesthetic adjustment
    document.querySelector("#FrontLabel").style.minWidth = (DESK_MINWIDTH * (Width / jump)) + "px";

    // Recreate seating plan in "index.html"
    for (let y = 0; y < Height; y++) {
        let row = document.createElement('div');
        row.classList.add('row', 'planRow', "flex-nowrap");
        row.style.height = rowHeight;
        for (let x = 0; x < Width; x += jump) {
            // Col element to contain a desk
            let col = document.createElement('div');
            col.classList.add('col', 'd-flex', 'align-items-center', 'justify-content-center', 'p-2', 'p-lg-3');
            col.style.minWidth = DESK_MINWIDTH + "px";

            // Desk element inside
            let desk = document.createElement('div');
            desk.classList.add('d-flex', 'align-items-center', DeskNameJustify);
            desk.style.width = '100%';
            desk.style.backgroundColor = 'rgba(173, 216, 230, 0.7)';
            desk.style.borderRadius = '10px';
            desk.style.height = DeskHeight;

            // Names in desk (2 names if partnered mode)
            let NameBox2;
            let NameBox = document.createElement('span');
            NameBox.classList.add("NameBox");
            NameBox.style.maxWidth = "90%";
            NameBox.style.overflow = "hidden";
            if (Partners) {
                NameBox2 = document.createElement('span');
                NameBox2.classList.add("NameBox");
                NameBox2.style.maxWidth = "90%";
                NameBox2.style.overflow = "hidden";
            }

            // Find name for this coordinate in assignments. If not found, then name="empty".
            for (let n = 0; n < jump; n++) {
                let found = false;
                for (let name in Assignments) {
                    let coords = Assignments[name];
                    if (coords[0] == x + n && coords[1] == y) {
                        found = true;
                        if (n == 0) {
                            NameBox.innerHTML = name;
                        } else {
                            NameBox2.innerHTML = name;
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

    // Highlight F students in orange BG
    let allRows = PlanContainer.querySelectorAll(".planRow");
    for (let p = 0; p < allRows.length; p++) {
        let cols = allRows[p].querySelectorAll(".col");
        for (let q = 0; q < cols.length; q++) {
            let desk = cols[q].querySelector("div");
            let names = desk.querySelectorAll("span");
            for (let r = 0; r < names.length; r++) {
                    let nameText = names[r].innerHTML.trim()
                    if (F.includes(nameText)) {
                        names[r].style.backgroundColor = FrontsBG;
                    }
                }
            }
        }

    // When all elements are created, hide the loading screen and show the plan
    document.querySelector('#LoadingScreen').style.display = "none";
    PlanContainer.style.display = 'block';
    document.querySelector("#compTables").style.display = "block";
    document.querySelector("#redPlusButton").style.display = "none";
    document.querySelector("#greenPlusButton").style.display = "none";
    document.querySelector("#compTables").classList.add("mt-5", "mt-md-3");

    // Reconfigure+Regenerate buttons on bottom of page
    document.querySelector("#ResetButtons").style.display = "block";
    let CompRemoved = response["CompRemoved"];
    let IncompRemoved = response["IncompRemoved"];
    let lists = [CompRemoved, IncompRemoved];
    let pairList = document.querySelector("#pairList");
    let type = "Compatible";
    for (let z = 0; z < lists.length; z++) {
        if ( z == 1) {
            type = "Incompatible";
        }
        if (lists[z].length > 0) {
            document.querySelector("#RemovedPairsDesc").style.display = "block";
            for (let c = 0; c < lists[z].length; c++) {
                let li = document.createElement("li");
                li.innerHTML = lists[z][c][0] + " and " + lists[z][c][1] + " (" + type + ")";
                pairList.appendChild(li);
            }
        }
    }


    // Table aesthetic adjustments
    let RedTableTitle = document.querySelector("#RedTableTitle");
    let GreenTableTitle = document.querySelector("#GreenTableTitle");
    RedTableTitle.classList.remove("text-end");
    RedTableTitle.classList.add("text-center");
    GreenTableTitle.classList.remove("text-start");
    GreenTableTitle.classList.add("text-center");

    // Hover on row to highlight C and I students
    redRows = document.querySelectorAll(".redRow");
    greenRows = document.querySelectorAll(".greenRow");
    let rows = [redRows, greenRows];
    for (let t = 0; t < rows.length; t++) {
        for (let u = 0; u < rows[t].length; u++) {
            rows[t][u].addEventListener("mouseover", Highlight);
            rows[t][u].addEventListener("mouseout", function(event) {
                unHighlight(event, F);
            });
            rows[t][u].removeEventListener("click", remove_row);
            // Permanenly highlight HI rows in RED
            if (t == 0) {
                let students = rows[t][u].querySelectorAll(".S");
                for (let k = 0; k < HI.length; k++) {
                    if ((students[0].innerHTML == HI[k][0] || students[0].innerHTML == HI[k][1]) && (students[1].innerHTML == HI[k][0] || students[1].innerHTML == HI[k][1])) {
                        rows[t][u].style.backgroundColor = SelectedHIpairBG;
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
            // Darkened COMP/INCOMP BG colors
            if (HoveredRow.classList.contains("redRow")) {
                NameBoxes[n].style.backgroundColor = "rgba(220, 20, 60, 0.5)";
            } else {
                NameBoxes[n].style.backgroundColor = "rgba(34, 139, 34, 0.5)";
            }
        }
    }
}

const FrontsBG = "rgba(255, 222, 173, 0.7)";
function unHighlight(event, F) {
    let UnHoveredRow = event.currentTarget;
    let StudentPair = UnHoveredRow.querySelectorAll(".S");

    let NameBoxes = document.querySelectorAll(".NameBox");
    for (let n = 0; n < NameBoxes.length; n++) {
        if ((StudentPair[0].innerHTML == NameBoxes[n].innerHTML) || (StudentPair[1].innerHTML == NameBoxes[n].innerHTML)) {
            NameBoxes[n].style.backgroundColor = "rgba(0, 0, 0, 0)";
            for (let z = 0; z < F.length; z++) {
                if (NameBoxes[n].innerHTML == F[z]) {
                    NameBoxes[n].style.backgroundColor = FrontsBG;
                }
            }
        }
    }
}

function regenerate_plan() {
    // Delete old plan
    let PlanContainer = document.querySelector("#plan");
    let planRows = PlanContainer.querySelectorAll(".planRow");
    for (let p = 0; p < planRows.length; p++) {
        PlanContainer.removeChild(planRows[p]);
    }

    // Delete old impossible pair list
    let ul = document.querySelector("#pairList");
    let lis = ul.querySelectorAll("li");
    for (let p = 0; p < lis.length; p++) {
        ul.removeChild(lis[p]);
    }

    // Hide elements for loading screen
    PlanContainer.style.display = "none";
    document.querySelector("#RemovedPairsDesc").style.display = "none";
    document.querySelector("#ResetButtons").style.display = "none";
    document.querySelector("#compTables").style.display = "none";
    document.querySelector("#LoadingScreen").style.display = "block";

    // AJAX request
    send_lists();
}


// == ==
//// Animations == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
// == ==

const FadeOutSpecs = "fadeOut 0.10s";
const FadeInSpecs = "fadeIn 0.10s";
const TimeOut = 80;
// "Timeout" must be slightly shorter than animation time

function fade(ElementsOut, ElementsIn) {
    for (let w = 0; w < ElementsOut.length; w++) {
        document.querySelector(ElementsOut[w]).style.animation = FadeOutSpecs;
    }
    setTimeout(function() {
        for (let x = 0; x < ElementsOut.length; x++) {
            document.querySelector(ElementsOut[x]).style.display = "none";
        }
        for (let y = 0; y < ElementsIn.length; y++) {
            document.querySelector(ElementsIn[y]).style.opacity = "0";
            document.querySelector(ElementsIn[y]).style.display = "block";
            document.querySelector(ElementsIn[y]).style.animation = FadeInSpecs;
        }
        setTimeout(function() {
            for (let z = 0; z < ElementsIn.length; z++) {
                document.querySelector(ElementsIn[z]).style.opacity = "1";
            }
        }, TimeOut);
    }, TimeOut);
}

function comps_to_fronts_animation() {
    document.querySelector("#InfoTitle").style.display = 'none';
    document.querySelector("#compTables").style.display = 'none';
    document.querySelector("#NextButton").style.display = 'none';
    document.querySelector("#StudentSelection").style.marginTop = '265px';
    document.querySelector("#StudentSelection").style.animation = 'topSlide 0.5s';
    document.querySelector(".FrontDesc").style.display = "block";
    document.querySelector(".FrontDesc").style.animation = "fadeIn 0.5s";
    setTimeout(function() {
        document.querySelector("#StudentSelection").style.marginTop = '25px';
        document.querySelector("#StudentSelection").style.backgroundColor = 'rgba(255, 222, 173, 0.5)';
        document.querySelector("#StudentSelection").style.border = '2px solid rgba(255, 222, 173, 1.0)';
        document.querySelector(".FrontDesc").style.opacity = "1";
    }, 490);
}

function ScrollTop() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}