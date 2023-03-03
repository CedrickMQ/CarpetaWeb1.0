const $dialog = document.getElementById("dialog");
const $btnA = document.getElementById("btnA");
const $btnC = document.getElementById("btnC");

$btnA.addEventListener("click",() => 
{
    $dialog.showModal();
})

$btnC.addEventListener("click",() =>
{
    $dialog.close();
})
