const dataRows = document.getElementsByClassName('data-rows');
const addButton = document.getElementById('add-button');
const duplicate = document.getElementsByClassName('dup-button');

let currentRows = 2;
let currentRecipeRows = 1;

function toggleInputDisabled(currentRecipeRows){
  for(let i = 0; i<currentRecipeRows; i++){
    var inputUnit = this.previousElementSibling.previousElementSibling.previousElementSibling.children[0];
    var inputName = inputUnit.previousElementSibling;

    if (inputUnit.disabled){
      inputName.disabled = false;
      inputUnit.disabled = false;
    }
    else {
     inputName.disabled = true;
     inputUnit.disabled = true;
    }
  }
  
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
  currentRecipeRows += 1;
  })


}

addButton.onclick = function(){ 
  const template = `
  <tr id='ingredient-${currentRows}'>    
    <td>1</td>
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

duplicate.onclick = function{
  //TODO
}

const editButtons = document.getElementsByClassName('edit-button-recipe');
Array.from(editButtons).forEach(button => {
  button.onclick = toggleInputDisabled;
})

const addButtonsRecipe = document.getElementsByClassName('add-button-recipe');
Array.from(addButtonsRecipe).forEach(button => {
  button.onclick = addRecipeRow;
})

