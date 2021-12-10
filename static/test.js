// let nameOfPerson = prompt("Hey there! Welcome to the checkup, let us know your name!!");
// if(nameOfPerson!=null) {
//     document.getElementById("user-name").innerHTML = "Hello " + nameOfPerson + " !";
// }

const modal = document.querySelector('.modal');
const overlay = document.querySelector('.overlay');
const btnCloseModal = document.querySelector('.btn--close-modal');
const submitButton = document.querySelector('.btn--submit');
const fName = document.querySelector('.fname');
const userName = document.getElementById('user-name');

// const finalSubmitButton = document.querySelector('.btn-secondary')
// finalSubmitButton.addEventListener('click', reset);

const closeModal = function(){
    modal.classList.add('hidden');
    overlay.classList.add('hidden');
}

btnCloseModal.addEventListener('click', closeModal)
overlay.addEventListener('click', closeModal)
submitButton.addEventListener('click', function(e){
    e.preventDefault();
    userName.innerHTML = "Hello " + fName.textContent + " !";
    closeModal();
})
document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !modal.classList.contains('hidden')) {
      closeModal();
    }
});