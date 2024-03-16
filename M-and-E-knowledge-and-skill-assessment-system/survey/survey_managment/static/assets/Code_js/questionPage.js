
const addDivBtn = document.getElementById('add-div-btn');
// Get a reference to your specific button
const rmvDivBtn = document.getElementById('rmv-div');
let count = 1;
let myCheckbox = document.querySelector('input[name="weightCHK"]');
let weightInput = document.getElementsByName('weightInput')[0];
let DocCheck = document.querySelector('input[name="docCHk"]');
let Doclable = document.getElementsByName('Doclable')[0];
myCheckbox.addEventListener('change', function (event) {
    checkWeight(event, myCheckbox, weightInput);
    console.log("Clicked");

});

DocCheck.addEventListener('change', function (event) {
    checkDoc(event, DocCheck, Doclable);
    console.log("Clicked");

});

let add_option_btn = document.getElementsByName('add-option-btn')[0];
const questionTypeDropdown = document.getElementsByName('question_type')[0];
const questionCardBody = document.getElementsByName('questionCardBody')[0];
let optionList = document.getElementsByName('optionList')[0];
let optionsContainer = document.getElementsByName('options-container')[0];


// cards.addEventListener('click', function (event) {
//     getCardId(event);
//     console.log(" getCardId Clicked form origin");

// });
// Get the optionList container
let needOptions = ['Checkbox', 'Radio'];

questionTypeDropdown.addEventListener('change', function (event) {
    handleQuestionTypeChange(event, questionTypeDropdown, questionCardBody, optionList, optionsContainer);
});

function handleQuestionTypeChange(event, questionTypeDropdown, questionCardBody, optionList, optionsContainer) {
    let selectedType = questionTypeDropdown.value;
    console.log(selectedType);
    // Remove any existing input elements
    let existingInput = questionCardBody.querySelector('.form-group');
    if (existingInput) {
        existingInput.remove();
    }
    console.log("questionCardBody");
    console.log(questionCardBody);
    if (selectedType === 'text') {
        clearOptions();
        add_option_btn.style.display = 'none';
        const inputElement = document.createElement('input');
        inputElement.type = 'text';
        inputElement.classList.add('form-control');
        inputElement.id = 'username';
        inputElement.name = 'username';
        inputElement.placeholder = 'Type text';
        inputElement.required = true;

        const formGroup = document.createElement('div');
        formGroup.classList.add('form-group');
        formGroup.appendChild(inputElement);

        questionCardBody.appendChild(formGroup);
    }
    else if (selectedType === 'number') {
        clearOptions();
        add_option_btn.style.display = 'none';
        const inputElement = document.createElement('input');
        inputElement.type = 'number';
        inputElement.classList.add('form-control');
        inputElement.id = 'number';
        inputElement.name = 'number';
        inputElement.placeholder = 'Type number';
        inputElement.required = true;

        const formGroup = document.createElement('div');
        formGroup.classList.add('form-group');
        formGroup.appendChild(inputElement);

        questionCardBody.appendChild(formGroup);
    }
    else if (selectedType === 'checkbox') {
        clearOptions();
        add_option_btn.style.display = 'block';

        optionList.style.display = 'block';

        // Create default options
        for (var i = 1; i <= 2; i++) {
            var newOption = document.createElement('div');
            newOption.classList.add('form-group');

            var label = document.createElement('label');
            label.textContent = 'Option ' + i + ':';

            var input = document.createElement('input');
            input.setAttribute('type', 'text');
            input.setAttribute('name', 'option');
            input.classList.add('form-control');
            input.required = true;

            var anchor = document.createElement('a');
            anchor.setAttribute('href', '#');
            anchor.textContent = 'Remove';
            anchor.addEventListener('click', function (event) {
                event.preventDefault();
                newOption.remove();
            });

            newOption.appendChild(label);
            newOption.appendChild(input);
            newOption.appendChild(anchor);


            optionsContainer.appendChild(newOption);
        }


    }

    else if (selectedType === 'radio') {
        clearOptions();
        add_option_btn.style.display = 'block';
        optionList.style.display = 'block';
        // Create default options
        for (var i = 1; i <= 2; i++) {
            var newOption = document.createElement('div');
            newOption.classList.add('form-group');

            var label = document.createElement('label');
            label.textContent = 'Option ' + i + ':';

            var input = document.createElement('input');
            input.setAttribute('type', 'text');
            input.setAttribute('name', 'option');
            input.classList.add('form-control');
            input.required = true;

            var anchor = document.createElement('a');
            anchor.setAttribute('href', '#');
            anchor.textContent = 'Remove';
            anchor.addEventListener('click', function (event) {
                event.preventDefault();
                newOption.remove();
            });

            newOption.appendChild(label);
            newOption.appendChild(input);
            newOption.appendChild(anchor);


            optionsContainer.appendChild(newOption);
        }

    }
}

add_option_btn.addEventListener('click', function (event) {
    console.log("Add button clicked");
    addOptions(event, optionsContainer);
});


// let cards = document.querySelector('[id*="card"]');
let cards = document.querySelectorAll('.mycard');


// Function to clear the options container
function clearOptions() {
    // Remove all child elements from the options container
    while (optionsContainer.firstChild) {
        optionsContainer.firstChild.remove();
    }
}
let storeCards = ['card-0'];
function addEventListenersToCard(card) {
    let questionTypeDropdown = card.querySelector('[name="question_type"]');
    let questionCardBody = card.querySelector('[name="questionCardBody"]');
    let optionList = card.querySelector('[name="optionList"]');
    let optionsContainer = card.querySelector('[name="options-container"]');
    let myCheckbox = card.querySelector('[name="weightCHK"]');
    let weightInput = card.querySelector('[name="weightInput"]');
    let DocCheck = card.querySelector('[name="docCHk"]');
    let Doclable = card.querySelector('[name="Doclable"]');
    let add_option_btn = card.querySelector('[name="add-option-btn"]');
    let remove_btn = card.querySelector('[name="remove_btn"]');
    if (questionTypeDropdown) {
        questionTypeDropdown.addEventListener('change', function (event) {
            handleQuestionTypeChange(event, questionTypeDropdown, questionCardBody, optionList, optionsContainer);
        });
        console.log("called");
        console.log(questionTypeDropdown);
    }
    DocCheck.addEventListener('change', function (event) {
        checkDoc(event, DocCheck, Doclable);
        console.log(" DocCheck Clicked");

    });
    myCheckbox.addEventListener('change', function (event) {
        checkWeight(event, myCheckbox, weightInput);
        console.log(weightInput);
        console.log("myCheckbox Clicked");

    });

    add_option_btn.addEventListener('click', function (event) {
        console.log("Add button clicked");
        addOptions(event, optionsContainer);
    });
    card.addEventListener('click', function (event) {
        console.log('Clicked Card**:', card.id);
    });
remove_btn.addEventListener('click', function (event) {
console.log(card);
const cardId = card.id;
const cardToRemove = document.getElementById(cardId);
if (cardToRemove) {
cardToRemove.remove();
}
});
}
function addCardAfter(event) {
    const clickedButton = event.target;
    const card = clickedButton.parentNode;
    const newCard = document.createElement("div");
    const cardId = `card-${count}`;
    newCard.id = cardId;
    newCard.classList.add('mycard');
    newCard.innerHTML =`
    <div class="custom-div">
                                <div class="row mt-4 ">
                                    <div class="col-md-10">
                                        <div class="card card-outline" style="border-left: 4px solid #46b583;">
                                            <div class="card-header">
<div class="dropdown">
    <button class="btn dropdown-toggle" type="button" id="dropdown" arial-haspopup="true" aria-expanded="false" style="float: right;"
    data-toggle="collapse" href="#card_body" role="button" aria-controls="collapseExample"></button></button>
</div>
                                                <h3 class="card-title form-group" style="width: 75%;">
                                                    <div class="form-controls" style="width: 100%;">
                                                        <input type="text" class="wide-input" name="question_title"
                                                            class="question_title" placeholder="Untitled question" />
                                                    </div>
                                                    <div class="form-controls" style="width: 100%;display: none;">
                                                        <input type="text" class="wide-input"
                                                            placeholder="Description" />
                                                    </div>
                                                </h3>

                                                <div class="card-tools mt-3">
                                                    <select class="form-control" class="questionTypeDropdown"
                                                        name="question_type">
                                                        <option value="" selected disabled>Select an option</option>
                                                        <option value="text">
                                                            <span class="icon"><i class="bi bi-textarea-t"></i></span>
                                                            Text
                                                        </option>
                                                        <option value="number">
                                                            <span class="icon"><i class="bi bi-123"></i></span> Numbers
                                                        </option>
                                                        <option value="checkbox">
                                                            <span class="icon"><i class="bi bi-check-all"></i></span>
                                                            Multi-select
                                                        </option>
                                                        <option value="radio">
                                                            <span class="icon"><i
                                                                    class="bi bi-check2-circle"></i></span>
                                                            Uni-select
                                                        </option>
                                                        <option value="textarea">
                                                            <span class="icon"><i class="bi bi-card-text"></i></span>
                                                            Description
                                                        </option>
                                                    </select>
                                                </div>

                                            </div>
                                            <div class="row m-3" >
                                                <div class="form-group col-lg-3">
                                                    <select class="form-control category" name="category">
                                                        {%for category in categories%}
                                                        <option value="{{category.id}}">{{category.name}}</option>
                                                        {%endfor%}
                                                    </select>
                                                </div>
                                                <div class="form-group col-lg-2">
                                                    <label for="myCheckbox">
                                                        <input type="checkbox" class="myCheckbox" name="weightCHK">
                                                        Weight
                                                    </label>
                                                </div>
                                                <div class="form-group col-lg-2" name="weightInput"
                                                    style="display: none;">
                                                    <input class="form-control" type="number" name="weight_input"
                                                        id="" />
                                                </div>
                                                <div class="form-group col-lg-2">
                                                    <label for="">
                                                        <input type="checkbox" class="doclable" name="docCHk">
                                                        Document
                                                    </label>
                                                </div>
                                                <div class="form-group col-lg-3" name="Doclable" style="display: none;">
                                                    <input class="form-control" type="text" name="doclable" value="" />
                                                </div>
                                            </div>
                                            <div class="card-body questionCardBody" name="questionCardBody" id="card_body" >
                                                <!-- Initial content of the card body -->
                                                <div class="row">
                                                    <div class="col-lg-8">
                                                        <div class="form-group">
                                                        </div>
                                                        <div name="optionList" style="display: none;">
                                                            <div class="options-container" name="options-container">
                                                                <!--  options will be added here -->
                                                            </div>
                                                            <!-- Add Option Button -->
                                                            <button type="button" name="add-option-btn"
                                                                class="btn btn-secondary add-option-btn">Add
                                                                Option</button>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="card-footer">
                                                <div class="row">
                                                    <div class="col-sm-8">
                                                    </div>
                                                    <div class="col-sm-4">
                                                        <i class="bi bi-copy" style="margin-left:15px ;"></i>
                                                        <span>
                                                            <button type="button" name="remove_btn"
                                                                class="btn btn-secondary add-option-btn">Remove</button>
                                                            <i class="bi bi-trash3" style="margin-left:35px ;"></i>
                                                        </span>
                                                        <!-- <input type="radio" name="required" required
                                                            style="margin-left:25px ;" /> -->
                                                        <label> Required</label>
                                                        <i class="bi bi-three-dots-vertical"></i>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-lg-1">
                                        <button class="add-button">Add</button>

                                        <div class="option">
                                            <span id="add-div-btn">
                                                <i class="bi bi-plus-circle"></i>
                                            </span>
                                            <br>
                                            <span id="import-btn">
                                                <i class="fas fa-file-import"></i>
                                            </span>
                                        </div>
                                    </div>
                                </div>

                            </div>`;
    
    console.log(cardId);
    card.parentNode.insertBefore(newCard, card.nextSibling);
    const newAddButton = newCard.querySelector(".add-button");
    newAddButton.addEventListener("click", addCardAfter);
    console.log("storeNew");
    console.log(storeCards);
    addEventListenersToCard(newCard);
    let cards = document.querySelectorAll('.mycard')
    storeCards.push(cardId);
    count++;
}

const addButtons = document.querySelectorAll(".add-button");
addButtons.forEach((button) => {
    button.addEventListener("click", addCardAfter);
});

function checkWeight(event, weightCheck, weightInput) {

    if (weightCheck.checked) {
        weightInput.style.display = 'block'
    }
    else
        weightInput.style.display = 'none'

}

function checkDoc(event, DocCheck, Doclable) {

    if (DocCheck.checked) {
        console.log("Working");
        Doclable.style.display = 'block'
    }
    else
        Doclable.style.display = 'none'
}

function addOptions(event, optionsContainer) {
    let optionCount = optionsContainer.getElementsByClassName('form-group').length;
    let newOption = document.createElement('div');
    newOption.classList.add('form-group');
    let label = document.createElement('label');
    label.textContent = 'Option ' + (optionCount + 1) + ':';
    let input = document.createElement('input');
    input.setAttribute('type', 'text');
    input.setAttribute('name', 'option');
    input.classList.add('form-control');
    input.required = true;
    let anchor = document.createElement('a');
    anchor.setAttribute('href', '#');
    anchor.textContent = 'Remove';
    anchor.addEventListener('click', function (event) {
        event.preventDefault();
        newOption.remove();
    });
    newOption.appendChild(label);
    newOption.appendChild(input);
    newOption.appendChild(anchor);
    optionsContainer.appendChild(newOption);
}
function getCardId(event) {
    const clickedCardId = event.currentTarget.id;
    console.log('Cl ID:', clickedCardId);
}

document.addEventListener('DOMContentLoaded', function () {
    const addButton = document.getElementsByName('add_objects')[0];
    addButton.addEventListener('click', handleCardSubmit);

});
function handleCardSubmit() {
    const cardList = document.getElementsByClassName('mycard');
    let question_objects = [];
    console.log(cardList);
    for (let i = 0; i < cardList.length; i++) {
        const card = cardList[i];
        const cardId = card.id;
        console.log(cardId);
        // const optionInputs = card.querySelectorAll('input[name="option"]');
        // optionInputs.forEach(function(optionInput) {
        // options.push(optionInput.value);
        // });
// console.log("Helsdgh");
// console.log(options);
let optionValues = [];
let optionsContainer = card.querySelector('[name="options-container"]');
let optionInputs = optionsContainer.querySelectorAll('input[name="option"]');
optionInputs.forEach(function(input) {
    optionValues.push(input.value);
});
console.log("input")
console.log(optionInputs)
// Print the option values
console.log(optionValues);

const questionData = {
            question: card.querySelector('input[name="question_title"]').value,
            questionType: card.querySelector('[name="question_type"]').value,
            category: card.querySelector('[name="category"]').value,
            hasWeight: card.querySelector('input[name="weightCHK"]').value,
            weight: card.querySelector('input[name="weight_input"]').value,
            hasDoc: card.querySelector('input[name="docCHk"]').value,
            Doclable: card.querySelector('input[name="doclable"]').value,
            options: optionValues
        };
        // console.log(card);
        // console.log('Card:', card);
        // console.log('Card ID:', cardId);       
        question_objects.push(questionData);

        
        console.log('Question Data:', question_objects);
        let jsonObjects = JSON.stringify(question_objects);
        document.getElementById('objects-input').value = jsonObjects;
        console.log("done");

    }
}
// JavaScript code
// const defaultCard= document.getElementById('card-0');

//     defaultCard.addEventListener('click', function(event) {
//       console.log('Clicked ID:', defaultCard.id);
//     });

