const dataRows = document.getElementById('data-rows');
const addButton = document.getElementById('add-button');

let currentRows = 2;

function toggleInputDisabled(){
  const inputUnit = this.previousElementSibling;
  const inputName = inputUnit.previousElementSibling;

  if (inputUnit.disabled){
    inputName.disabled = false;
    inputUnit.disabled = false;
  }
  else {
    inputName.disabled = true;
    inputUnit.disabled = true;
  }
}

function addRecipeRow(){
  // disable product terakhir
  this.previousElementSibling.previousElementSibling.children[0].disabled = true;
  this.previousElementSibling.previousElementSibling.children[1].disabled = true;
  
  //add new row for product
  const currentIngredientRow = this.parentElement.parentElement.parentElement.id;
  const template = `
  <li>
    <input class='col-sm-5' type='text' name='ingredientProductName[${currentIngredientRow}]' placeholder='product name...'/>
    <input class='col-sm-3' type='text' name='ingredientProductUnit[${currentIngredientRow}]' placeholder='product unit...'/>
    <button type="button" class="edit-button-recipe col-sm-3 btn btn-secondary">Toggle Edit</button>
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
                <button type="button" class="edit-button-recipe col-sm-3 btn btn-secondary">Toggle Edit</button>
            </li>
            <div id='empty-recipe-row'></div>
            <button  type="button" class="add-button-recipe d-block btn btn-primary">Add product</button>
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

const editButtons = document.getElementsByClassName('edit-button-recipe');
Array.from(editButtons).forEach(button => {
  button.onclick = toggleInputDisabled;
})

const addButtonsRecipe = document.getElementsByClassName('add-button-recipe');
Array.from(addButtonsRecipe).forEach(button => {
  button.onclick = addRecipeRow;
})
