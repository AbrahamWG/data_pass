const dataRows = document.getElementsByClassName('data-rows');
const addButton = document.getElementById('add-button');
const duplicate = document.getElementById('dup-button');
const addProductToListButton = document.getElementById('add-product-to-list-button');
const dataTable = document.getElementById('data-table');
const scoreRows = document.getElementsByClassName('score-rows');
const addButtonScore = document.getElementById('add-button-score');

let currentRows = 2;
let currentRowsScore =2;
const productNames = [];

function toggleInputDisabled(){
  const parent = this.parentElement;
  const allInputs = parent.querySelectorAll('input');
  allInputs.forEach(input => {
    if (input.disabled) {
      input.disabled = false;
    }
    else input.disabled =true;
  })
}


function addRecipeRow(){
  // disable product terakhir
  
  //add new row for product
  const currentIngredientRow = this.parentElement.parentElement.parentElement.id;
  const template = `
  <li>
    <select name='ingredientProductName[${currentIngredientRow}]'>
    </select>
    <input class='col-sm-3' type='text' name='ingredientProductUnit[${currentIngredientRow}]' placeholder='product unit...'/>
    <button type='button' class='btn btn-danger btn-delete-product'>Delete</button>

  </li>
  <div id='empty-recipe-row'></div>
  `
  const currentEmptyRecipeRow = this.previousElementSibling;
  currentEmptyRecipeRow.outerHTML = template;
  const editButtons = document.getElementsByClassName('edit-button-recipe');
  Array.from(editButtons).forEach(button => {
    button.onclick = toggleInputDisabled;

  })

  const deleteProductButtons = document.getElementsByClassName('btn-delete-product');
  Array.from(deleteProductButtons).forEach(button => {
    button.onclick = deleteProductRow;
  })

  const myLi = this.previousElementSibling.previousElementSibling;
  const mySelect = myLi.querySelector('select');
  for(var i  =0 ; i<  productNames.length; i++){
    const currentOption = document.createElement('option');
    currentOption.value = productNames[i];
    currentOption.textContent = productNames[i];
    mySelect.appendChild(currentOption);
  }
}

addButton.onclick = function(){ 
  const template = `
  <tr id='ingredient-${currentRows}'>    
    <td>${currentRows}</td>
    <td>
        <input type='text' name='ingredient[]' placeholder='add an ingredient...'/>
    </td>
    <td>
        <input type='number' name='supply[]' placeholder='specify value...'/>
    </td>
    <td>
        <input type='text' name='price[]' placeholder='specify value...'/>
    </td>
    <td>
        <ol>
            <li>
                <select name='ingredientProductName[ingredient-${currentRows}]'>

                </select>
                <input class='col-sm-3' type='text' name='ingredientProductUnit[ingredient-${currentRows}]' placeholder='product unit...'/>
                <button type='button' class='btn btn-danger btn-delete-product'>Delete</button>
            </li>
            <div id='empty-recipe-row'></div>
            <button type="button" class="add-button-recipe btn btn-primary mt-4">Add product</button>
            <button type="button" class="edit-button-recipe col-sm-4 btn btn-secondary mt-4">Toggle Edit</button>
            <br>
            <button type="button" class="delete-button-ingredient col-sm-4 btn btn-danger mt-2" style='width: 60%'>Delete Ingredient</button>
            <hr>
        </ol>
    </td>
</tr>
    
<tr id='empty-row'></tr>
  `;
  currentRows += 1;
  const currentEmptyRow = document.getElementById('empty-row');
  currentEmptyRow.outerHTML = template;

  const editButtons = document.getElementsByClassName('edit-button-recipe');
  Array.from(editButtons).forEach(button => {
    button.onclick = toggleInputDisabled;
  })
  const addButtonsRecipe = document.getElementsByClassName('add-button-recipe');
  Array.from(addButtonsRecipe).forEach(button => {
    button.onclick = addRecipeRow;
  })

  const deleteProductButtons = document.getElementsByClassName('btn-delete-product');
  Array.from(deleteProductButtons).forEach(button => {
    button.onclick = deleteProductRow;
  })

  const deleteIngredientButtons = document.getElementsByClassName('delete-button-ingredient');
  Array.from(deleteIngredientButtons).forEach(button => {
    button.onclick = deleteIngredientRow;
  })

  const mySelect = this.parentElement.parentElement.previousElementSibling.previousElementSibling.querySelector('select');
  for(var i  =0 ; i<  productNames.length; i++){
    const currentOption = document.createElement('option');
    currentOption.value = productNames[i];
    currentOption.textContent = productNames[i];
    mySelect.appendChild(currentOption);
  }
}


duplicate.onclick = function() {

  //dapatkan tbody
  const tbody = document.getElementsByTagName('tbody')[0];
  //dapatkan children row table terakhir, -3 karena index
  var childrenLength = tbody.children.length;
  var template = tbody.children[childrenLength-3].outerHTML + '<tr id="empty-row"></tr>';
  // id kolom NO last row, misal ke5, row-number-5, ubah jadi row-number-5 id nya
  template = template.replace('row-number-' + (currentRows - 1), 'row-number-' + currentRows);
  // console.log(template);
  template = template.replaceAll('ingredient-' + (currentRows - 1), 'ingredient-' + currentRows);
  console.log(template);
  const currentEmptyRow = document.getElementById('empty-row');
  currentEmptyRow.outerHTML = template;
  console.log('row-number-' + currentRows)
  const currentRowNumber = document.getElementById('row-number-' + currentRows);
  currentRowNumber.textContent = currentRows;
  const editButtons = document.getElementsByClassName('edit-button-recipe');
  Array.from(editButtons).forEach(button => {
    button.onclick = toggleInputDisabled;
  })
  const addButtonsRecipe = document.getElementsByClassName('add-button-recipe');
  Array.from(addButtonsRecipe).forEach(button => {
    button.onclick = addRecipeRow;
  })

  const deleteProductButtons = document.getElementsByClassName('btn-delete-product');
  Array.from(deleteProductButtons).forEach(button => {
    button.onclick = deleteProductRow;
  })
  const deleteIngredientButtons = document.getElementsByClassName('delete-button-ingredient');
  Array.from(deleteIngredientButtons).forEach(button => {
    button.onclick = deleteIngredientRow;
  })


  //increment row
  currentRows += 1; 
  childrenLength = tbody.children.length;
  const lastTr = tbody.children[childrenLength-3];
  const secondLastTr = tbody.children[childrenLength-4];
  console.log(lastTr, secondLastTr)
  const allInputsLastTr = lastTr.querySelectorAll('input');
  const allInputsSecondLastTr = secondLastTr.querySelectorAll('input');
  for(var i = 0; i < allInputsLastTr.length; i+=1){
    allInputsLastTr[i].value = allInputsSecondLastTr[i].value; 
  }
}
addProductToListButton.onclick = function(){
  const myProductNameInput = document.getElementById('product-name');
  const name = myProductNameInput.value;
  productNames.push(name);
  const mySelects = document.getElementsByTagName('select');
  for(var i = 0; i < mySelects.length; i++){
    
      const currentOption = document.createElement('option');
      const productNamesLength = productNames.length;
      currentOption.value = productNames[productNamesLength - 1];
      currentOption.textContent = productNames[productNamesLength - 1];
      mySelects[i].appendChild(currentOption)
    
  }
}

function deleteProductRow(){
  const li = this.parentElement;
  li.outerHTML = '';
}

function deleteIngredientRow(){
  const tr = this.parentElement.parentElement.parentElement;
  tr.outerHTML = '';
}

const editButtons = document.getElementsByClassName('edit-button-recipe');
Array.from(editButtons).forEach(button => {
  button.onclick = toggleInputDisabled;
})

const addButtonsRecipe = document.getElementsByClassName('add-button-recipe');
Array.from(addButtonsRecipe).forEach(button => {
  button.onclick = addRecipeRow;
})

const deleteProductButtons = document.getElementsByClassName('btn-delete-product');
Array.from(deleteProductButtons).forEach(button => {
  button.onclick = deleteProductRow;
})

const deleteIngredientButtons = document.getElementsByClassName('delete-button-ingredient');
Array.from(deleteIngredientButtons).forEach(button => {
  button.onclick = deleteIngredientRow;
})

addButtonScore.onclick = function(){ 
  const template = `
  <tr id='ingredient-score-${currentRowsScore}'>  
    <td>${currentRowsScore}</td>  
    <td>
      <select name='scoreListName[]'>

      </select>
    </td>
    <td>
        <input type='number' name='demand[]' placeholder='specify value...'/>
    </td>
    <td>
        <input type='number' name='minimum[]'' placeholder='specify value...'/>
    </td>
    <td>
        <input type='number' name='maximum[]'' placeholder='specify value...'/>
    </td>
  </tr>

  <tr id='empty-row-score'></tr>
  `;
  currentRowsScore += 1;
  const currentEmptyRowScore = document.getElementById('empty-row-score');
  currentEmptyRowScore.outerHTML = template;

  const mySelect = this.parentElement.parentElement.previousElementSibling.previousElementSibling.querySelector('select');
  for(var i  =0 ; i<  productNames.length; i++){
    const currentOption = document.createElement('option');
    currentOption.value = productNames[i];
    currentOption.textContent = productNames[i];
    mySelect.appendChild(currentOption);
  }

}


// ========= SEND DATA TO PYTHON ============
dataTable.onsubmit = function(e){
  const form = e.srcElement;
  const fd = new FormData(form);
  fd.set('totalIngredientRows', currentRows);
  fetch('/', {
    method: "POST",
    body: fd
  }).then(res => res.json())
    .then(data => {
      // data = data dictionary dari flask.
      /*
        {
          'BobaA': 500,
          
        }
      */
      var template = "";

      console.log(data);
      const output = document.getElementById('output');
      Object.entries(data).forEach(entry => {
        template += '<li>' + entry[0] + ': ' + entry[1] + '</li>'
      })
      output.innerHTML = template;
    })
  e.preventDefault();
}