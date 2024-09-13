document.addEventListener('DOMContentLoaded', function() {
    const addFormBtns = document.querySelectorAll('.add-form-btn');
    
    addFormBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const formset = this.closest('.mb-8');
            const totalForms = formset.querySelector('[name$=TOTAL_FORMS]');
            const newForm = formset.querySelector('.formset-form').cloneNode(true);
            const formNum = parseInt(totalForms.value);
            
            newForm.innerHTML = newForm.innerHTML.replace(/-\d+-/g, `-${formNum}-`);
            newForm.querySelectorAll('input:not([type=hidden]), select, textarea').forEach(input => {
                input.value = '';
            });
            
            this.insertAdjacentElement('beforebegin', newForm);
            totalForms.value = formNum + 1;
        });
    });
});