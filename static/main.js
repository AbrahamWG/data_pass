const dataRows = document.getElementsByClassName('data-rows');
const addButton = document.getElementById('add-button');
const duplicate = document.getElementById('dup-button');

let currentRows = 2;

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
    <input class='col-sm-5' type='text' name='ingredientProductName[${currentIngredientRow}]' placeholder='product name...'/>
    <input class='col-sm-3' type='text' name='ingredientProductUnit[${currentIngredientRow}]' placeholder='product unit...'/>
  </li>
  <div id='empty-recipe-row'></div>
  `
  const currentEmptyRecipeRow = this.previousElementSibling;
  currentEmptyRecipeRow.outerHTML = template;
  const editButtons = document.getElementsByClassName('edit-button-recipe');
  Array.from(editButtons).forEach(button => {
    button.onclick = toggleInputDisabled;

  })


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
                <input class='col-sm-5' type='text' name='ingredientProductName[]' placeholder='product name...'/>
                <input class='col-sm-3' type='text' name='ingredientProductUnit[]' placeholder='product unit...'/>
            </li>
            <div id='empty-recipe-row'></div>
            <button  type="button" class="add-button-recipe btn btn-primary">Add product</button>
            <button type="button" class="edit-button-recipe col-sm-4 btn btn-secondary">Toggle Edit</button>
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
}


duplicate.onclick = function() {

  //dapatkan tbody
  const tbody = document.getElementsByTagName('tbody')[0];
  //dapatkan children row table terakhir, -3 karena index
  var childrenLength = tbody.children.length;
  var template = tbody.children[childrenLength-3].outerHTML + '<tr id="empty-row"></tr>';
  // id kolom NO last row, misal ke5, row-number-5, ubah jadi row-number-5 id nya
  template = template.replace('row-number-' + (currentRows - 1), 'row-number-' + currentRows);
  template = template.replace('ingredient-' + (currentRows - 1), 'ingredient-' + currentRows);
  
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
const editButtons = document.getElementsByClassName('edit-button-recipe');
Array.from(editButtons).forEach(button => {
  button.onclick = toggleInputDisabled;
})

const addButtonsRecipe = document.getElementsByClassName('add-button-recipe');
Array.from(addButtonsRecipe).forEach(button => {
  button.onclick = addRecipeRow;
})

